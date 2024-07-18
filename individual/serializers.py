from rest_framework import serializers
from .models import UserProfile, ShareProfile, Receivedprofile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


# class UpdateProfilePicSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UpdateProfilePic
#         fields = '__all__'


class ShareProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareProfile
        fields = '__all__'


class ReceivedprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receivedprofile
        fields = '__all__'
