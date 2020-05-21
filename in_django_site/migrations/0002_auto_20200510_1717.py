# Generated by Django 3.0.6 on 2020-05-10 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('in_django_site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='indjangouser',
            name='follows',
            field=models.ManyToManyField(blank=True, null=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='stories')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(max_length=1000)),
                ('likes', models.IntegerField(default=0)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='attachments')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(max_length=1000)),
                ('likes', models.IntegerField(default=0)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='attachments')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='in_django_site.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(max_length=1000)),
                ('likes', models.IntegerField(default=0)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='attachments')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_comments', to=settings.AUTH_USER_MODEL)),
                ('reply_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='in_django_site.GroupPost')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='own_groups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='subscribers',
            field=models.ManyToManyField(blank=True, null=True, related_name='groups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(max_length=1000)),
                ('likes', models.IntegerField(default=0)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='attachments')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('reply_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='in_django_site.Post')),
            ],
        ),
    ]