from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    company_name = models.CharField(max_length=100, blank=True, null=True)
    admin_name = models.CharField(max_length=100, blank=True, null=True)
    profile_type = models.CharField(max_length=50, choices=[('individual', 'Individual'), ('employee', 'Employee'), ('company', 'Company')])
    authentication_type = models.CharField(
        max_length=50,
        choices=[('manual', 'Manual'), ('google', 'Google')],
        default='manual'
    )

    def __str__(self):
        return self.username
