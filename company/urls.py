from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.company_profile_list, name='company_list'),
    path('companies/<int:pk>/', views.company_detail, name='company_detail'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
]
