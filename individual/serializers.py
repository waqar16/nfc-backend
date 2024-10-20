from rest_framework import serializers
from .models import UserProfile, ShareProfile, Receivedprofile


class UserProfileSerializer(serializers.ModelSerializer):
    facebook = serializers.URLField(required=False, allow_null=True)
    instagram = serializers.URLField(required=False, allow_null=True)
    website = serializers.URLField(required=False, allow_null=True)
    linkedin = serializers.URLField(required=False, allow_null=True)
    github = serializers.URLField(required=False, allow_null=True)
    whatsapp = serializers.IntegerField(required=False, allow_null=True)
    profile_pic = serializers.URLField(required=False, allow_null=True)
    display_email = serializers.EmailField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class ShareProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareProfile
        fields = '__all__'


class ReceivedprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receivedprofile
        fields = '__all__'
