from django.contrib import admin
from .models import Company, Employee

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ['company_name', 'admin_name', 'email', 'phone', 'website', 'receive_marketing_emails']
    
    # Fields to enable searching
    search_fields = ['company_name', 'admin_name', 'email', 'phone']
    
    # Fields to filter by in the sidebar
    list_filter = ['receive_marketing_emails']
    
    # Ordering of records in the list view
    ordering = ['company_name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ['first_name', 'last_name', 'email', 'position', 'company']
    
    # Fields to enable searching
    search_fields = ['first_name', 'last_name', 'email', 'position', 'company__company_name']
    
    # Fields to filter by in the sidebar
    list_filter = ['position', 'company']
    
    # Ordering of records in the list view
    ordering = ['last_name']
    
    # Optionally, you can add fieldsets to customize the form layout in the admin panel
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'position', 'company')
        }),
        ('Contact Information', {
            'fields': ('phone', 'address', 'bio', 'facebook', 'instagram', 'website', 'linkedin', 'github', 'whatsapp'),
            'classes': ('collapse',),
        }),
        ('Profile Information', {
            'fields': ('profile_pic', 'receive_marketing_emails'),
            'classes': ('collapse',),
        }),
    )
