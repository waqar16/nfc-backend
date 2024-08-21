from django.contrib import admin
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Event
from nfc_backend.settings import EMAIL_HOST_USER

User = get_user_model()


class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_date', 'event_time', 'event_location')
    search_fields = ('event_name', 'event_location')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if not change:  # Check if this is a new object
            # Notify attendees about the new event
            for user in obj.attendees.all():
                send_mail(
                    subject=f'Invitation: {obj.event_name}',
                    message=(
                        f'Hello {user.username},\n\n'
                        f'You are invited to our event "{obj.event_name}".\n\n'
                        f'Details:\n'
                        f'Location: {obj.event_location}\n'
                        f'Date: {obj.event_date}\n'
                        f'Time: {obj.event_time}\n'
                        f'Description: {obj.event_description}\n\n'
                        f'We hope to see you there!'
                    ),
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
            self.message_user(request, 'Event created and attendees notified.')
        else:
            self.message_user(request, 'Event updated.')

admin.site.register(Event, EventAdmin)
