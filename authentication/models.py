from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    company_name = models.CharField(max_length=100, blank=True, null=True)
    admin_name = models.CharField(max_length=100, blank=True, null=True)
    profile_type = models.CharField(max_length=50, choices=[('individual', 'Individual'), ('employee', 'Employee'), ('company', 'Company')])
    # verification_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.username
