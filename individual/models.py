from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    whatsapp = models.IntegerField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)



# class UpdateProfilePic(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)



class ShareProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_to')
    shared_at = models.DateTimeField(auto_now_add=True)


class Receivedprofile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_from')
    shared_at = models.DateTimeField(auto_now_add=True)

