from django.urls import path, re_path

from . import forms
from . import views

app_name = 'site'

urlpatterns = [
    re_path(r'^$', views.RootView.as_view(), name='root'),
    re_path(r'^id(?P<id>[0-9]{1,6})/$', views.user, name='user_profile'),
    re_path(r'^group(?P<pk>[0-9]{1,6})/$', views.single_group, name='single_group'),
    re_path(r'^group(?P<id>[0-9]{1,6})/create-post/', views.create_group_post, name='create_group_post'),
    re_path(r'^group(?P<id>[0-9]{1,6})/create-comment/', views.comment_group_post, name='comment_group_post'),
    path('profile/', views.profile, name='my_profile'),
    path('profile/settings/', views.ProfileSettingsView.as_view(), name='profile_settings'),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('signUp/', views.RegistrationView.as_view(), name='registration'),
    path('signIn/', views.AuthorizationView.as_view(), name='authorization'),
    path('signOut/', views.sign_out, name='logout'),
    path('groups/', views.user_groups, name='user_groups'),
    path('group/create/', views.CreateGroupView.as_view(), name='create_group'),
    path('like-group-post/', views.group_post_like, name='group_post_like'),
    path('like-post/', views.post_like, name='post_like'),
    path('delete-group-comment/', views.delete_group_comment, name='delete_group_comment'),
    path('delete-group-post/', views.delete_group_post, name='delete_group_post'),
    path('delete-comment/', views.delete_comment, name='delete_comment'),
    path('delete-post/', views.delete_post, name='delete_post'),
    path('comment-user-post/', views.comment_user_post, name='comment_user_post'),
    path('follows/', views.follows, name='follows'),
    path('stories/', views.DisplayStoriesView.as_view(), name='stories'),
    path('stories/create', views.StoryCreateView.as_view(), name='create_story'),

]
