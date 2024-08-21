from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=255)
    event_description = models.TextField()
    event_longitute = models.FloatField()
    event_latitude = models.FloatField()
    attendees = models.ManyToManyField(User, related_name='events', blank=True)

    def __str__(self):
        return self.event_name