from itertools import chain
from operator import attrgetter

from django.urls import reverse

from . import forms
from . import models
from . import tasks

from django import http
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F


@login_required
def profile(request):
    posts = auth.get_user(request).posts.all().order_by('-created_at')
    if request.method == 'GET':
        context = {'posts': posts, 'form': forms.PostForm, 'comment_form': forms.PostCommentForm,
                   'page_title': 'Profile'}
        return render(request, 'my_profile.html', context)
    else:
        if request.POST.get('post-id'):
            text = request.POST.get('text')
            attachment = None
            if request.FILES:
                attachment = request.FILES['attachment']
            post_id = request.POST.get('post-id')
            post = models.Post.objects.get(id=post_id)
            models.Comment.objects.create(text=text, attachment=attachment, author=auth.get_user(request),
                                          reply_on=post)
            context = {'posts': posts, 'form': forms.PostForm, 'comment_form': forms.PostCommentForm,
                       'page_title': 'Profile'}
            return render(request, 'my_profile.html', context)
        else:
            text = request.POST.get('text')
            attachment = None
            if request.FILES:
                attachment = request.FILES['attachment']
            models.Post.objects.create(text=text, author=auth.get_user(request), attachment=attachment)
            context = {'posts': posts, 'form': forms.PostForm, 'comment_form': forms.PostCommentForm,
                       'page_title': 'Profile'}
            return render(request, 'my_profile.html', context)


@login_required
def user(request, id):
    user = models.InDjangoUser.objects.get(id=id)
    exist = user in auth.get_user(request).follows.all()
    if request.method == 'GET':
        if auth.get_user(request) == user:
            return redirect('site:my_profile')
        else:
            context = {'current_user': user, 'followed': exist, 'page_title': user.get_full_name(),
                       'posts': user.posts.all().order_by('-created_at'), 'comment_form': forms.PostCommentForm}
            return render(request, 'user_profile.html', context)
    else:
        if request.POST.get('title'):
            follow = True if request.POST.get('title') == 'Follow' else False
            if follow:
                user = auth.get_user(request)
                user.follows.add(models.InDjangoUser.objects.get(id=id))
                return http.HttpResponse()
            else:
                user = auth.get_user(request)
                user.follows.remove(models.InDjangoUser.objects.get(id=id))
                return http.HttpResponse(status=200)
        else:
            text = request.POST.get('text')
            attachment = None
            if request.FILES:
                attachment = request.FILES['attachment']
            post_id = request.POST.get('post-id')
            post = models.Post.objects.get(id=post_id)
            models.Comment.objects.create(text=text, attachment=attachment, author=auth.get_user(request),
                                          reply_on=post)
            context = {'current_user': user, 'followed': exist, 'page_title': user.get_full_name(),
                       'posts': user.posts.all().order_by('-created_at'), 'comment_form': forms.PostCommentForm}
            return render(request, 'user_profile.html', context)


@login_required
def sign_out(request):
    auth.logout(request)
    return redirect('site:authorization')


@login_required
def single_group(request, pk):
    if request.method == 'POST':
        follow = True if request.POST.get('title') == 'Follow' else False
        if follow:
            group = models.Group.objects.get(pk=pk)
            group.subscribers.add(auth.get_user(request))
            return http.HttpResponse(status=200)
        else:
            group = models.Group.objects.get(pk=pk)
            group.subscribers.remove(auth.get_user(request))
            return http.HttpResponse(status=200)
    else:
        group = models.Group.objects.get(pk=pk)
        if auth.get_user(request) == group.owner:
            context = {'group': group, 'owner': True, 'form': forms.GroupPostForm,
                       'comment_form': forms.GroupPostCommentForm, 'page_title': group.title}
            return render(request, 'single_group.html', context)
        else:
            exist = group.subscribers.filter(id=auth.get_user(request).id).exists()
            context = {'group': group, 'followed': exist, 'comment_form': forms.GroupPostCommentForm,
                       'page_title': group.title}
            return render(request, 'single_group.html', context)


@login_required
def create_group_post(request, id):
    if request.method == 'POST':
        text = request.POST.get('text')
        attachment = None
        if request.FILES:
            attachment = request.FILES['attachment']
        group = models.Group.objects.get(id=id)
        models.GroupPost.objects.create(text=text, attachment=attachment, group=group)
        return redirect('site:single_group', pk=group.id)


@login_required
def group_post_like(request):
    id = request.POST.get('id')
    type = request.POST.get('type')
    if type == 'like':
        models.GroupPost.objects.get(id=id).likes.add(auth.get_user(request))
    elif type == 'unlike':
        models.GroupPost.objects.get(id=id).likes.remove(auth.get_user(request))
    return http.HttpResponse(status=200)


@login_required
def comment_group_post(request, id):
    if request.method == 'POST':
        text = request.POST.get('text')
        attachment = None
        if request.FILES:
            attachment = request.FILES['attachment']
        post_id = request.POST.get('post-id')
        post = models.GroupPost.objects.get(id=post_id)
        models.GroupComment.objects.create(text=text, attachment=attachment, author=auth.get_user(request),
                                           reply_on=post)
        if request.POST.get('from') == 'group':
            return redirect('site:single_group', pk=id)
        else:
            return redirect('site:feed')


@login_required
def comment_user_post(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        attachment = None
        if request.FILES:
            attachment = request.FILES['attachment']
        post_id = request.POST.get('post-id')
        post = models.Post.objects.get(id=post_id)
        models.Comment.objects.create(text=text, attachment=attachment, author=auth.get_user(request), reply_on=post)
        return redirect('site:feed')


@login_required
def user_groups(request):
    if request.method == 'POST':
        if request.POST.get('stmt'):
            stmt = request.POST.get('stmt')
            groups = auth.get_user(request).groups.all().filter(title__icontains=stmt)
            own_groups = auth.get_user(request).own_groups.all()
            return render(request, 'user_groups.html',
                          {'groups': groups, 'own_groups': own_groups, 'page_title': 'Groups'})
        else:
            stmt1 = request.POST.get('stmt1')
            groups = auth.get_user(request).groups.all()
            own_groups = auth.get_user(request).own_groups.all().filter(title__icontains=stmt1)
            return render(request, 'user_groups.html',
                          {'groups': groups, 'own_groups': own_groups, 'page_title': 'Groups'})
    else:
        groups = auth.get_user(request).groups.all()
        own_groups = auth.get_user(request).own_groups.all()
        return render(request, 'user_groups.html', {'groups': groups, 'own_groups': own_groups, 'page_title': 'Groups'})


@login_required
def post_like(request):
    id = request.POST.get('id')
    type = request.POST.get('type')
    if type == 'like':
        models.Post.objects.get(id=id).likes.add(auth.get_user(request))
    elif type == 'unlike':
        models.Post.objects.get(id=id).likes.remove(auth.get_user(request))
    return http.HttpResponse(status=200)


@login_required
def delete_group_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        models.GroupComment.objects.get(id=comment_id).delete()
        return http.HttpResponse(status=200)


@login_required
def delete_group_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        models.GroupPost.objects.get(id=post_id).delete()
        return http.HttpResponse(status=200)


@login_required
def delete_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        models.Comment.objects.get(id=comment_id).delete()
        return http.HttpResponse(status=200)


@login_required
def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        models.Post.objects.get(id=post_id).delete()
        return http.HttpResponse(status=200)


@login_required
def follows(request):
    if request.method == 'GET':
        return render(request, 'user_follows.html', context={'follows': auth.get_user(request).follows.all()})
    else:
        stmt = request.POST.get('stmt')
        follows = auth.get_user(request).follows.filter(Q(first_name__icontains=stmt) | Q(last_name__icontains=stmt))
        return render(request, 'user_follows.html', context={'follows': follows})


class RegistrationView(CreateView):
    template_name = 'signUp.html'
    form_class = forms.RegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Registration'
        return context

    def post(self, request, *args, **kwargs):
        context_form = forms.RegistrationForm
        form = forms.RegistrationForm(request.POST)
        errors = form.errors
        if form.is_valid():
            user = form.save(request.POST.copy())
            auth.login(request, user)
            return redirect('site:user_profile', id=user.id)
        else:
            return render(request, 'signUp.html', context={'form': context_form, 'errors': errors})


class AuthorizationView(FormView):
    template_name = 'signIn.html'
    form_class = forms.AuthorizationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Authorization'
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('site:user_profile', id=user.id)
        else:
            return render(request, 'signIn.html',
                          context={'form': forms.AuthorizationForm, 'error': 'Incorrect username or password'})


class RootView(LoginRequiredMixin, RedirectView):
    pattern_name = 'site:feed'
    permanent = False
    query_string = True


class SingleGroupView(LoginRequiredMixin, DetailView):
    model = models.Group
    template_name = 'single_group.html'


class FeedView(LoginRequiredMixin, ListView):
    template_name = 'feed.html'
    paginate_by = 10

    def get_queryset(self):
        user = auth.get_user(self.request)
        own_posts = user.posts.all()
        own_group_posts = models.GroupPost.objects.filter(group__owner__in=[user, ]).order_by('created_at').all()
        group_posts = models.GroupPost.objects.filter(group__subscribers__in=[user, ]).order_by('created_at').all()
        follows_posts = models.Post.objects.filter(author__followers__in=[user, ]).order_by('created_at').all()
        all_posts = sorted(chain(own_posts, own_group_posts, group_posts, follows_posts), key=attrgetter('created_at'),
                           reverse=True)
        return all_posts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['comment_form'] = forms.PostCommentForm
        context['page_title'] = 'Feed'
        return context


class CreateGroupView(LoginRequiredMixin, CreateView):
    model = models.Group
    fields = ['title', 'description']
    template_name = 'create_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Group'
        return context

    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        description = request.POST['description']
        owner = auth.get_user(request)
        group = models.Group.objects.create(title=title, description=description, owner=owner)
        return redirect('site:single_group', pk=group.id)


class ProfileSettingsView(LoginRequiredMixin, FormView):
    template_name = 'profile_settings.html'
    form_class = forms.ProfileSettingsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Profile Settings'
        return context

    def post(self, request, *args, **kwargs):
        user = auth.get_user(request)
        if request.POST.get('first_name'):
            first_name = request.POST.get('first_name')
            models.InDjangoUser.objects.filter(id=user.id).update(first_name=first_name)
        if request.POST.get('last_name'):
            last_name = request.POST.get('last_name')
            models.InDjangoUser.objects.filter(id=user.id).update(last_name=last_name)
        if request.POST.get('gender'):
            gender = request.POST.get('gender')
            models.InDjangoUser.objects.filter(id=user.id).update(gender=gender)
        if request.POST.get('date_of_birth'):
            date_of_birth = request.POST.get('date_of_birth')
            models.InDjangoUser.objects.filter(id=user.id).update(date_of_birth=date_of_birth)
        if request.POST.get('country'):
            country = request.POST.get('country')
            models.InDjangoUser.objects.filter(id=user.id).update(country=country)
        if request.FILES:
            avatar = request.FILES['avatar']
            user.avatar = avatar
            user.save()
        return redirect('site:my_profile')


def handle404(request, exception):
    context = {'page_title': 'Ooopppsss...'}
    return render(request, 'errors/404.html', context, status=404)


def handle500(request):
    context = {'page_title': 'Ooopppsss...'}
    return render(request, 'errors/404.html', context, status=500)


class StoryCreateView(CreateView):
    model = models.Story
    template_name = 'create_story.html'
    form_class = forms.StoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Story'
        return context

    def post(self, request, *args, **kwargs):
        if request.FILES['file']:
            file = request.FILES['file']
            story = models.Story.objects.create(author=auth.get_user(request), file=file)
            tasks.delete_story.apply_async(kwargs={'story_id': story.id}, countdown=24*60*60)
        return redirect('site:stories')


class DisplayStoriesView(ListView):
    model = models.Story
    template_name = 'stories.html'
    paginate_by = 10

    def get_queryset(self):
        models.Story.objects.filter(author__followers__in=[auth.get_user(self.request), ]).update(views_count=F('views_count') + 1)
        own_stories = models.Story.objects.filter(author=auth.get_user(self.request)).all()
        other_stories = models.Story.objects.filter(author__followers__in=[auth.get_user(self.request), ]).all()
        return own_stories.union(other_stories).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['page_title'] = 'Stories'
        return context


