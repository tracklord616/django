from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView,\
                                      PasswordResetConfirmView, PasswordResetCompleteView
from in_django_site import forms

handler404 = 'in_django_site.views.handle404'
handler500 = 'in_django_site.views.handle500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('indjango/', include('in_django_site.urls', namespace='site')),
    path('indjango/api/', include('in_django_api.urls', namespace='api')),
    path('password-reset/',
         PasswordResetView.as_view(template_name='password_reset/password_reset.html',
                                   form_class=forms.PasswordResetForm
                                   ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

