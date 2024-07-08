from django.db import models
from django.contrib.auth.models import User


class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    interaction_type = models.CharField(max_length=50)


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    followed_up = models.BooleanField(default=False)
    interaction = models.ForeignKey(Interaction, on_delete=models.CASCADE, related_name='contacts')
