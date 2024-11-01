from django.contrib import admin
from .models import UserProfile, ShareProfile, Receivedprofile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ['user', 'first_name', 'last_name', 'position', 'email']
    
    # Fields to enable searching
    search_fields = ['user__username', 'first_name', 'last_name', 'email']
    
    # Fields to filter by in the sidebar
    list_filter = ['receive_marketing_emails', 'position']
    
    # Ordering of records in the list view
    ordering = ['user']

# @admin.register(ShareProfile)
# class ShareProfileAdmin(admin.ModelAdmin):
#     # Fields to display in the list view
#     list_display = ['user', 'shared_to', 'shared_at']
    
#     # Fields to enable searching
#     search_fields = ['user__username', 'shared_to__username']
    
#     # Fields to filter by in the sidebar
#     list_filter = ['shared_at']
    
#     # Ordering of records in the list view
#     ordering = ['-shared_at']

# @admin.register(Receivedprofile)
# class ReceivedprofileAdmin(admin.ModelAdmin):
#     # Fields to display in the list view
#     list_display = ['user', 'shared_from', 'shared_from_email', 'profile_type_who_shared', 'shared_at']
    
#     # Fields to enable searching
#     search_fields = ['user__username', 'shared_from__username', 'shared_from_email']
    
#     # Fields to filter by in the sidebar
#     list_filter = ['profile_type_who_shared', 'shared_at']
    
#     # Ordering of records in the list view
#     ordering = ['-shared_at']
