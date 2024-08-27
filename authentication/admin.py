from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    # Fields to be displayed in the list view
    list_display = ['username', 'company_name', 'admin_name', 'profile_type', 'authentication_type']
    
    # Fields to enable searching
    search_fields = ['username', 'company_name', 'admin_name']
    
    # Fields to filter by in the sidebar
    list_filter = ['profile_type', 'authentication_type']

    # Ordering of records in the list view
    ordering = ['username']

    # Add a date hierarchy if there's a relevant date field, e.g., `date_joined`
    # date_hierarchy = 'date_joined'

# Register the CustomUser model with the customized admin class
admin.site.register(CustomUser, CustomUserAdmin)
