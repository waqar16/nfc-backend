from rest_framework import serializers
from .models import UserProfile, UpdateProfilePic, ShareProfile, Receivedprofile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user', 'first_name', 'last_name', 'email', 'phone', 'address', 'bio',
            'facebook', 'instagram', 'linkedin'
        ]


class UpdateProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateProfilePic
        fields = '__all__'


class ShareProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareProfile
        fields = '__all__'

class ReceivedprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receivedprofile
        fields = '__all__'
