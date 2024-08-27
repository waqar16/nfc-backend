from django.db import models


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=255)
    event_description = models.TextField()
    event_longitude = models.FloatField()
    event_latitude = models.FloatField()

    def __str__(self):
        return self.event_name
