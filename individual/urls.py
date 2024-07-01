from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.user_profile_list, name='user_profile_list'),
    path('profiles/<int:pk>/', views.user_profile_detail, name='user_profile_detail'),
]