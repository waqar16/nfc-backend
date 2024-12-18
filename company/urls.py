from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.company_profile_list, name='company_list'),
    path('companies/<str:username>/', views.company_detail, name='company_detail'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<str:identifier>/', views.employee_detail, name='employee_detail'),
    path('employees/complete-registration/<uuid:token>/<str:email>/<str:first_name>/<str:last_name>', views.complete_registration, name='complete-registration'),
    path('employees/delete/<str:email>/', views.delete_employee_profile, name='delete_employee_profile'),
]
