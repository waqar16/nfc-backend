from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('profiles/', views.user_profile_list, name='user_profile_list'),
    path('profiles/<int:pk>/', views.user_profile_detail, name='user_profile_detail'),
    # path('update-profile-pic/', views.update_profile_pic, name='update-profile-pic'),
    path('nfc-write/', views.nfc_write, name='nfc_write'),
    path('nfc-read/', views. nfc_read, name='nfc_read'),
    path('share-profile-url/', views.share_profile_url, name='share-profile-url'),
    path('share-profile/', views.share_profile, name='share-profile'),
    path('received-cards/', views.share_profile, name='received_profiles'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)