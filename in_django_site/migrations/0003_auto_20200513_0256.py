# Generated by Django 3.0.6 on 2020-05-12 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('in_django_site', '0002_auto_20200510_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='groupcomment',
            name='text',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='grouppost',
            name='text',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
