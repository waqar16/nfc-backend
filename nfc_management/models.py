from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Card(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    user = models.ForeignKey(User, related_name='cards', on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='inactive')

    def __str__(self):
        return f"Card {self.user} ({self.status})"
