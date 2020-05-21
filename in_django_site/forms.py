from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm as PasswordResetFormCore
from django.forms import SelectDateWidget, RadioSelect, Select, PasswordInput
from . import models
from . import tasks


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    gender = forms.BooleanField(widget=RadioSelect(
        choices=(
            (True, 'Man'),
            (False, 'Woman')
        )
    )
    )
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=[y for y in range(1930, 2020)]))
    country = forms.CharField(widget=Select(
        choices=(
            ('Russia', 'Russia'),
            ('Ukraine', 'Ukraine'),
            ('Belarus', 'Belarus'),
            ('Kazakhstan', 'Kazakhstan')
        )
    )
    )
    rules_accept = forms.BooleanField()

    class Meta:
        model = models.InDjangoUser
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'gender',
            'date_of_birth',
            'country',
            'rules_accept',
        )
        exclude = ('username',)


class AuthorizationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=PasswordInput())


class GroupPostForm(forms.ModelForm):
    class Meta:
        model = models.GroupPost
        fields = ('text', 'attachment')
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 30})
        }


class GroupPostCommentForm(forms.ModelForm):
    class Meta:
        model = models.GroupComment
        fields = ('text', 'attachment')
        widgets = {
            'text': forms.Textarea(attrs={'rows': 1, 'cols': 20})
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('text', 'attachment')
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 30})
        }


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('text', 'attachment')
        widgets = {
            'text': forms.Textarea(attrs={'rows': 1, 'cols': 20})
        }


class ProfileSettingsForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.BooleanField(widget=RadioSelect(
        choices=(
            (True, 'Man'),
            (False, 'Woman')
        )
    ), required=False
    )
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=[y for y in range(1930, 2020)]))
    country = forms.CharField(widget=Select(
        choices=(
            ('Russia', 'Russia'),
            ('Ukraine', 'Ukraine'),
            ('Belarus', 'Belarus'),
            ('Kazakhstan', 'Kazakhstan')
        )
    ), required=False
    )
    avatar = forms.FileField(required=False)

    class Meta:
        model = models.InDjangoUser
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'country',
            'avatar',
        )
        exclude = ('username',)


class StoryForm(forms.ModelForm):
    class Meta:
        model = models.Story
        fields = ('file',)


class PasswordResetForm(PasswordResetFormCore):
    email = forms.EmailField(max_length=100, widget=forms.TextInput(
        attrs={
            'id': 'email',
            'placeholder': 'Email'
        }
    ))

    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):
        context['user'] = context['user'].id
        tasks.send_mail.delay(subject_template_name=subject_template_name,
                              email_template_name=email_template_name,
                              context=context, from_email=from_email, to_email=to_email,
                              html_email_template_name=html_email_template_name)
