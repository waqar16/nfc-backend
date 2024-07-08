from djoser.serializers import UserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser
import random
from django.core.mail import send_mail
# from .models import Profile

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    company_name = serializers.CharField(max_length=100, required=False)
    admin_name = serializers.CharField(max_length=100, required=False)
    profile_type = serializers.ChoiceField(choices=[('individual', 'Individual'), ('employee', 'Employee'), ('company', 'Company')])

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'company_name', 'admin_name', 'profile_type')

    # def create(self, validated_data):
    #     verification_code = str(random.randint(100000, 999999))
    #     validated_data['verification_code'] = verification_code
        
    #     # Create user
    #     user = super().create(validated_data)
        
    #     # Send verification code via email
    #     self.send_verification_email(user)
    #     print(f"Verification email sent to {user.email}")  # Add logging here for debugging
        
    #     return user

    # def send_verification_email(self, user):
    #     subject = 'Your Verification Code'
    #     message = f'Hi {user.first_name},\n\nYour verification code is {user.verification_code}.\n\nThank you!'
    #     from_email = 'wa4752928@gmail.com'
    #     to_email = user.email

    #     send_mail(subject, message, from_email, [to_email])
    #     print(f"Email sent to {to_email}")  # Add logging here for debugging



class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'company_name', 'admin_name', 'profile_type')


# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'