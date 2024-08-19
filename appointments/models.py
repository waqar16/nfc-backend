from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host')
    host_email = models.EmailField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    datetime = models.DateTimeField()
    google_event_id = models.CharField(max_length=255)
    meeting_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    def __str__(self):
        return f"Appointment with {self.host_email} on {self.datetime}"
    
    def update_status(self):
        # Ensure that datetime is a datetime object
        if isinstance(self.datetime, str):
            self.datetime = timezone.datetime.fromisoformat(self.datetime)
        
        # Use Django's timezone.now() to get the current time
        if self.datetime < timezone.now():
            self.meeting_status = 'completed'

    def save(self, *args, **kwargs):
        self.update_status()
        super().save(*args, **kwargs)
