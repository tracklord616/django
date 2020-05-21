from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class InDjangoUserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None,
                    last_name=None, gender=None, date_of_birth=None,
                    country=None, rules_accept=None):
        if not email:
            raise ValueError("Email is required")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            country=country,
            rules_accept=rules_accept
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name=None,
                         last_name=None, gender=None, date_of_birth=None,
                         country=None, rules_accept=None):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            country=country,
            rules_accept=rules_accept
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class InDjangoUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', unique=True, max_length=60)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
    last_login = models.DateTimeField(auto_now=True, verbose_name='last login')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    gender = models.BooleanField(null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    rules_accept = models.BooleanField(null=False, blank=False)
    avatar = models.FileField(upload_to='avatars', default='avatars/anon.png', blank=True)
    follows = models.ManyToManyField('InDjangoUser', related_name='followers', null=True, blank=True)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'date_of_birth', 'country', 'rules_accept']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Post(models.Model):
    created_at = models.DateTimeField(auto_now=datetime.now)
    text = models.TextField(max_length=1000, null=True, blank=True)
    author = models.ForeignKey(InDjangoUser, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(InDjangoUser, related_name='post_likes', null=True, blank=True)
    attachment = models.FileField(upload_to='attachments', null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.text is not None or self.attachment is not None:
            super().save(force_insert, force_update, using, update_fields)
        else:
            raise ValueError('Please type in text or add an attachment')

    def __str__(self):
        return '\'' + self.author.get_full_name() + '\' posted ' + self.text[:50] + '...'


class Comment(models.Model):
    reply_on = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now=datetime.now)
    text = models.TextField(max_length=1000, null=True, blank=True)
    author = models.ForeignKey(InDjangoUser, on_delete=models.CASCADE, related_name='comments')
    attachment = models.FileField(upload_to='attachments', null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.text is not None or self.attachment is not None:
            super().save(force_insert, force_update, using, update_fields)
        else:
            raise ValueError('Please type in text or add an attachment')


class Story(models.Model):
    created_at = models.DateTimeField(auto_now=datetime.now)
    author = models.ForeignKey(InDjangoUser, on_delete=models.CASCADE, related_name='stories')
    file = models.FileField(upload_to='stories', null=False, blank=False)
    views_count = models.IntegerField(default=0)


class Group(models.Model):
    created_at = models.DateTimeField(auto_now=datetime.now)
    owner = models.ForeignKey(InDjangoUser, on_delete=models.CASCADE, related_name='own_groups')
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    subscribers = models.ManyToManyField(InDjangoUser, related_name='groups', null=True, blank=True)

    def __str__(self):
        return self.title


class GroupPost(models.Model):
    created_at = models.DateTimeField(auto_now=datetime.now)
    text = models.TextField(max_length=1000, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(InDjangoUser, related_name='group_post_likes', null=True, blank=True)
    attachment = models.FileField(upload_to='attachments', null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.text is not None or self.attachment is not None:
            super().save(force_insert, force_update, using, update_fields)
        else:
            raise ValueError('Please type in text or add an attachment')

    def __str__(self):
        return '\'' + self.group.title + '\' posted ' + self.text[:50] + '...'


class GroupComment(models.Model):
    reply_on = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now=datetime.now)
    text = models.TextField(max_length=1000, null=True, blank=True)
    author = models.ForeignKey(InDjangoUser, on_delete=models.CASCADE, related_name='group_comments')
    attachment = models.FileField(upload_to='attachments', null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.text is not None or self.attachment is not None:
            super().save(force_insert, force_update, using, update_fields)
        else:
            raise ValueError('Please type in text or add an attachment')
