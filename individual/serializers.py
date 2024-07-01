from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user', 'phone', 'address', 'bio',
            'facebook', 'instagram', 'linkedin', 'profile_pic'
        ]


