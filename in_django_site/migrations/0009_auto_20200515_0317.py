# Generated by Django 3.0.6 on 2020-05-15 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('in_django_site', '0008_auto_20200515_0316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indjangouser',
            name='avatar',
            field=models.FileField(blank=True, default='avatars/anon.png', upload_to='avatars'),
        ),
    ]
