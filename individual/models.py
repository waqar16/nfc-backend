from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    display_email = models.EmailField(blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.URLField(blank=True, null=True)
    receive_marketing_emails = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"


class ShareProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_to')
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} shared profile to {self.shared_to}"


class Receivedprofile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_from')
    shared_from_email = models.EmailField(blank=True, null=True)
    shared_from_username = models.CharField(max_length=50, blank=True, null=True)
    shared_at = models.DateTimeField(auto_now_add=True)
    profile_type_who_shared = models.CharField(max_length=50, choices=[('individual', 'Individual'), ('employee', 'Employee'), ('company', 'Company')])
    shared_from_company_logo = models.URLField(blank=True, null=True)
    shared_from_profile_pic = models.URLField(blank=True, null=True)
    shared_from_first_name = models.CharField(max_length=255, blank=True, null=True)
    shared_from_last_name = models.CharField(max_length=255, blank=True, null=True)
    shared_from_position = models.CharField(max_length=255, blank=True, null=True)
    shared_from_company_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user} received profile from {self.shared_from}"
