from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics, status

from in_django_site.models import InDjangoUser
from .serializers import UserSerializer, UserCreateSerializer


class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCreateSerializer
    queryset = InDjangoUser.objects.all()

    @swagger_auto_schema(
        operation_summary="User Creation",
        responses={
            status.HTTP_200_OK: 'User Created',
            status.HTTP_400_BAD_REQUEST: 'Unresolved Data',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Something Went Wrong'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserGetAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = InDjangoUser.objects.all()
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_summary="User retrieve",
        responses={
            status.HTTP_200_OK: 'User retrieved',
            status.HTTP_404_NOT_FOUND: 'User not found',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Something Went Wrong'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = InDjangoUser.objects.all()
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_summary='User update',
        responses={
            status.HTTP_200_OK: 'User updated',
            status.HTTP_400_BAD_REQUEST: 'Unresolved Data',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Something Went Wrong'
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='User update',
        responses={
            status.HTTP_200_OK: 'User updated',
            status.HTTP_400_BAD_REQUEST: 'Unresolved Data',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Something Went Wrong'
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class UserDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer
    queryset = InDjangoUser.objects.all()
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_summary='User delete',
        responses={
            status.HTTP_200_OK: 'Users deleted',
            status.HTTP_403_FORBIDDEN: 'You must be an administrator to do this',
            status.HTTP_404_NOT_FOUND: 'User not found',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Something Went Wrong'
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class UsersListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = InDjangoUser.objects.all()

    @swagger_auto_schema(
        operation_summary='List of users',
        responses={
            status.HTTP_200_OK: 'Users retrieved',
            status.HTTP_204_NO_CONTENT: 'No users yet',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Something Went Wrong'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

