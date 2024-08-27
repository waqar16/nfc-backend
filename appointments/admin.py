from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ['title', 'host', 'attendee', 'datetime', 'meeting_status']
    
    # Fields to enable searching
    search_fields = ['title', 'host__username', 'attendee__username', 'host_email', 'attendee_email']
    
    # Fields to filter by in the sidebar
    list_filter = ['meeting_status', 'datetime', 'host', 'attendee']
    
    # Ordering of records in the list view
    ordering = ['-datetime']
    
    # Add a date hierarchy for easy navigation
    date_hierarchy = 'datetime'
