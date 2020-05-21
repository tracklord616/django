from in_django_site.models import InDjangoUser

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    follows = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)

    class Meta:
        model = InDjangoUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'country',
            'rules_accept',
            'follows',
            'followers',
        )


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InDjangoUser
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'country',
            'rules_accept',
        )