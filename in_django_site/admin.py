from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from . import models


class GroupPostInline(StackedInline):
    model = models.GroupPost
    extra = 1


class GroupInline(StackedInline):
    model = models.Group
    extra = 1


class PostInline(StackedInline):
    model = models.Post
    extra = 1


class GroupCommentInline(StackedInline):
    model = models.GroupComment
    extra = 1


class CommentInline(StackedInline):
    model = models.Comment
    extra = 1

class StoryInline(StackedInline):
    model = models.Story
    extra = 1


class GenderFilter(admin.SimpleListFilter):
    title = 'gender'
    parameter_name = 'gender'

    def lookups(self, request, model_admin):
        return (
            ('Male', 'Male'),
            ('Female', 'Female'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Male':
            users = []
            for user in queryset:
                if models.InDjangoUser.objects.get(id=user.id).gender:
                    users.append(user.id)
            return queryset.filter(id__in=users)
        elif value == 'Female':
            users = []
            for user in queryset:
                if not models.InDjangoUser.objects.get(id=user.id).gender:
                    users.append(user.id)
            return queryset.filter(id__in=users)
        return queryset


class CountryFilter(admin.SimpleListFilter):
    title = 'country'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        return (
            ('Russia', 'Russia'),
            ('Ukraine', 'Ukraine'),
            ('Belarus', 'Belarus'),
            ('Kazakhstan', 'Kazakhstan')
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Russia':
            users = []
            for user in queryset:
                if models.InDjangoUser.objects.get(id=user.id).country == 'Russia':
                    users.append(user.id)
            return queryset.filter(id__in=users)
        elif value == 'Ukraine':
            users = []
            for user in queryset:
                if models.InDjangoUser.objects.get(id=user.id).country == 'Ukraine':
                    users.append(user.id)
            return queryset.filter(id__in=users)
        elif value == 'Belarus':
            users = []
            for user in queryset:
                if models.InDjangoUser.objects.get(id=user.id).country == 'Belarus':
                    users.append(user.id)
            return queryset.filter(id__in=users)
        elif value == 'Kazakhstan':
            users = []
            for user in queryset:
                if models.InDjangoUser.objects.get(id=user.id).country == 'Kazakhstan':
                    users.append(user.id)
            return queryset.filter(id__in=users)
        return queryset


@admin.register(models.InDjangoUser)
class InDjangoUserAdmin(ModelAdmin):
    list_display = [
        'email',
        'first_name',
        'last_name',
        'gender',
        'date_of_birth',
        'country',
    ]

    search_fields = [
        'email',
        'first_name',
        'last_name',
    ]

    list_filter = [GenderFilter, CountryFilter]

    date_hierarchy = 'date_joined'

    readonly_fields = [
        'password',
    ]

    inlines = [StoryInline, GroupInline, PostInline]


@admin.register(models.Group)
class GroupAdmin(ModelAdmin):
    list_display = [
        'created_at',
        'owner_link',
        'title',
        'description',

    ]

    search_fields = [
        'title',
        'description',
    ]

    list_filter = []

    date_hierarchy = 'created_at'

    readonly_fields = [
        'owner',
    ]

    inlines = [GroupPostInline]

    def owner_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.owner._meta.model_name),
                    args=(obj.owner.pk,)), obj.owner.get_full_name()))

    owner_link.short_description = 'Owner'


@admin.register(models.Post)
class PostAdmin(ModelAdmin):
    list_display = [
        'created_at',
        'author_link',
        'text',

    ]

    search_fields = [
        'author',
        'text',
    ]

    list_filter = []

    date_hierarchy = 'created_at'

    readonly_fields = [
        'author',
    ]

    inlines = [CommentInline]

    def author_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.author._meta.model_name),
                    args=(obj.author.pk,)), obj.author.get_full_name()))

    author_link.short_description = 'Author'


class PostsByGroupFilter(admin.SimpleListFilter):
    title = 'group'
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        groups = ()
        for group in models.Group.objects.all():
            group_list = list(groups)
            group_list.append((group.title, group.title))
            groups = tuple(group_list)
        return groups

    def queryset(self, request, queryset):
        value = self.value()
        for group in models.Group.objects.all():
            if value == group.title:
                return queryset.filter(group=group)
        return queryset


@admin.register(models.GroupPost)
class GroupPostAdmin(ModelAdmin):
    list_display = [
        'created_at',
        'group_link',
        'text',

    ]

    search_fields = [
        'group',
        'text',
    ]

    list_filter = [PostsByGroupFilter]

    date_hierarchy = 'created_at'

    readonly_fields = [
        'group',
    ]

    inlines = [GroupCommentInline]

    def group_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.group._meta.model_name),
                    args=(obj.group.pk,)), obj.group.title))

    group_link.short_description = 'Group'


@admin.register(models.Comment)
class CommentAdmin(ModelAdmin):
    list_display = [
        'created_at',
        'author_link',
        'reply_on_link',
        'text',
        'attachment',

    ]

    search_fields = [
        'author',
        'text',
    ]

    list_filter = []

    date_hierarchy = 'created_at'

    readonly_fields = [
        'author',
        'text',
        'reply_on',
    ]

    def reply_on_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.reply_on._meta.model_name),
                    args=(obj.reply_on.pk,)), str(obj.reply_on)))

    reply_on_link.short_description = 'Reply on'

    def author_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.author._meta.model_name),
                    args=(obj.author.pk,)), obj.author.get_full_name()))

    author_link.short_description = 'Author'


@admin.register(models.GroupComment)
class GroupCommentAdmin(ModelAdmin):
    list_display = [
        'created_at',
        'author_link',
        'reply_on_link',
        'text',
        'attachment',

    ]

    search_fields = [
        'author',
        'text',
        'reply_on',
    ]

    list_filter = []

    date_hierarchy = 'created_at'

    readonly_fields = [
        'author',
        'reply_on',
    ]

    def reply_on_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.reply_on._meta.model_name),
                    args=(obj.reply_on.pk,)), str(obj.reply_on)))

    reply_on_link.short_description = 'Reply on'

    def author_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.author._meta.model_name),
                    args=(obj.author.pk,)), obj.author.get_full_name()))

    author_link.short_description = 'Author'


class StoryByAuthorFilter(admin.SimpleListFilter):
    title = 'author'
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        authors = ()
        for user in models.InDjangoUser.objects.all():
            group_list = list(authors)
            group_list.append((user.get_full_name(), user.get_full_name()))
            authors = tuple(group_list)
        return authors

    def queryset(self, request, queryset):
        value = self.value()
        for user in models.InDjangoUser.objects.all():
            if value == user.get_full_name():
                return queryset.filter(author=user)
        return queryset


@admin.register(models.Story)
class StoryAdmin(ModelAdmin):
    list_display = [
        'created_at',
        'author_link',
        'file',
        'views_count',
    ]

    search_fields = [
        'author',
    ]

    list_filter = [StoryByAuthorFilter]

    date_hierarchy = 'created_at'

    readonly_fields = [
        'author',
        'file',
    ]

    def author_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.author._meta.model_name),
                    args=(obj.author.pk,)), obj.author.get_full_name()))

    author_link.short_description = 'Author'