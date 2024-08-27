from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ['event_name', 'event_date', 'event_location']
    
    # Fields to enable searching
    search_fields = ['event_name', 'event_location', 'event_description']
    
    # Fields to filter by in the sidebar
    list_filter = ['event_date', 'event_location']
    
    # Ordering of records in the list view
    ordering = ['event_date', 'event_time']
    
    # Add a date hierarchy for easy navigation
    date_hierarchy = 'event_date'
