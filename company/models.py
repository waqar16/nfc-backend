from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    admin_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    company_description = models.TextField()
    website = models.URLField()
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.company_name


class Employee(models.Model):
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    email = models.EmailField(default='')
    phone = models.CharField(max_length=20, default='')
    position = models.CharField(max_length=255, default='')

    def __str__(self):
        return f"{self.name} ({self.position})"
