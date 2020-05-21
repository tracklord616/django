from django.urls import path, re_path
from rest_framework_simplejwt import views as jwt_views
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = 'api'

schema_view = get_schema_view(
   openapi.Info(
      title="InDjango API",
      default_version='v1',
      description="The first site-blog about Django",
      contact=openapi.Contact(email="in.django.site@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('users/', views.UsersListAPIView.as_view(), name='users_list'),
    path('users/<int:pk>/', views.UserGetAPIView.as_view(), name='single_user'),
    path('users/create/', views.UserCreateAPIView.as_view(), name='create_user'),
    path('users/<int:pk>/update/', views.UserUpdateAPIView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', views.UserDeleteAPIView.as_view(), name='delete_user'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


