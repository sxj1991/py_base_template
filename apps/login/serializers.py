from rest_framework import serializers

from apps.login.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(max_length=30, source="user_name")

    class Meta:
        model = UserModel
        exclude = ['user_name']
