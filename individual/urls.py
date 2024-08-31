from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
# from .views import google_calendar_init_view, google_calendar_redirect_view, google_calendar_events_view, google_calendar_create_event_view, google_calendar_callback


urlpatterns = [
    path('profiles/', views.user_profile_list, name='user_profile_list'),
    path('profiles/<int:pk>/', views.user_profile_detail, name='user_profile_detail'),
    # path('update-profile-pic/', views.update_profile_pic, name='update-profile-pic'),
    path('nfc-write/', views.nfc_write, name='nfc_write'),
    path('nfc-read/', views.nfc_read, name='nfc_read'),
    path('share-profile-url/', views.share_profile_url, name='share-profile-url'),
    path('share-profile/', views.share_profile, name='share-profile'),
    path('received-cards/', views.share_profile, name='received_profiles'),
    path('share-back-profile/', views.share_back_profile, name='share_back_profile'),
    # path('schedule-meeting/', views.ScheduleMeetingView.as_view(), name='ScheduleMeetingView'),

    # path('rest/v1/calendar/init/', google_calendar_init_view, name='google_calendar_init'),
    # path('google/callback/', google_calendar_callback, name='google_calendar_callback'),
    # path('rest/v1/calendar/redirect/', google_calendar_redirect_view, name='google_calendar_redirect'),
    # path('rest/v1/calendar/events/', google_calendar_events_view, name='google_calendar_events'),
    # path('rest/v1/calendar/create_event/', google_calendar_create_event_view, name='google_calendar_create_event'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)