from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.user_profile_list, name='user_profile_list'),
    path('profiles/<int:pk>/', views.user_profile_detail, name='user_profile_detail'),
    path('update-profile-pic/', views.update_profile_pic, name='update-profile-pic'),
    path('nfc-write/', views.nfc_write, name='nfc_write'),
    path('nfc-read/', views. nfc_read, name='nfc_read'),
    path('share-profile/', views.share_profile, name='share-profile'),
    path('received-cards/', views.share_profile, name='received_profiles'),
]