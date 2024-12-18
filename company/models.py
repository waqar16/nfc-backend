from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255 , null=True, blank=True)
    admin_name = models.CharField(max_length=255, null=True, blank=True)
    company_logo = models.URLField(blank=True, null=True)
    email = models.EmailField()
    display_email = models.EmailField(blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    company_description = models.TextField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    receive_marketing_emails = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name
 
    def delete(self, *args, **kwargs):
        # Delete associated user when the company is deleted
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)


class Employee(models.Model):
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    display_email = models.EmailField(blank=True, null=True, unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
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
    registration_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"

    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)
