from django.urls import path
from . import views

urlpatterns = [
    path('profile_type/', views.profile_type, name='profile_type'),
    # path('auth/custom_register/', views.custom_register, name='custom_register'),
]
