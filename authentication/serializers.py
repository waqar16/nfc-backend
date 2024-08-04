from djoser.serializers import UserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    company_name = serializers.CharField(max_length=100, required=False)
    admin_name = serializers.CharField(max_length=100, required=False)
    profile_type = serializers.ChoiceField(choices=[('individual', 'Individual'), ('employee', 'Employee'), ('company', 'Company')])
    authentication_type = serializers.ChoiceField(choices=[('manual', 'Manual'), ('google', 'Google')])

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'company_name', 'admin_name', 'profile_type', 'authentication_type')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value


class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'company_name', 'admin_name', 'profile_type', 'authentication_type')
