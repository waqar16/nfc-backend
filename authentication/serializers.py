from djoser.serializers import UserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser
from individual.models import UserProfile
from company.models import Company

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
    
    # def create(self, validated_data):
    #     # Create the user first
    #     user = CustomUser.objects.create_user(
    #         first_name=validated_data.get('first_name', ''),
    #         last_name=validated_data.get('last_name', ''),
    #         company_name=validated_data.get('company_name', ''),
    #         admin_name=validated_data.get('admin_name', ''),
    #         email=validated_data.get('email', ''),
    #         profile_type=validated_data.get('profile_type', ''),
    #         authentication_type=validated_data.get('authentication_type', ''),
    #         username=validated_data.get('username', ''),
    #         password=validated_data.get('password', ''),
    #     )
  
    #     if user.profile_type == 'individual':
    #         UserProfile.objects.create(
    #             user=user,
    #             first_name=validated_data.get('first_name', ''),
    #             last_name=validated_data.get('last_name', ''),
    #             email=validated_data.get('email', ''),
    #             username=validated_data.get('username', ''),
    #         )
            
    #     elif user.profile_type == 'company':
    #         Company.objects.create(
    #             user=user,
    #             company_name=validated_data.get('company_name', ''),
    #             admin_name=validated_data.get('admin_name', ''),
    #             email=validated_data.get('email', ''),
    #             username=validated_data.get('username', ''),
    #         )
        
    #     # Automatically create the user profile
    #     UserProfile.objects.create(
    #         user=user,
    #         first_name=validated_data.get('first_name', ''),
    #         last_name=validated_data.get('last_name', ''),
    #         email=validated_data.get('email', ''),
    #         username=validated_data.get('username', ''),
    #         # Add any other fields from UserProfile as needed
    #     )

    #     return user


class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'company_name', 'admin_name', 'profile_type', 'authentication_type')
