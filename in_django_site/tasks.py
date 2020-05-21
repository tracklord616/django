from celery import shared_task
from in_django_site.models import Story, InDjangoUser
from django.contrib.auth.forms import PasswordResetForm


@shared_task
def delete_story(story_id):
    Story.objects.get(id=story_id).delete()
    return None


@shared_task
def send_mail(subject_template_name, email_template_name, context,
              from_email, to_email, html_email_template_name):
    context['user'] = InDjangoUser.objects.get(pk=context['user'])

    PasswordResetForm.send_mail(
        None,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name
    )
    return 'Password reset link has been sent!'
