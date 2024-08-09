from django.urls import path
from .views import google_auth_request, google_auth_callback, schedule_meeting, get_meetings    

urlpatterns = [
    path('google/auth-request/', google_auth_request, name='google_auth_request'),
    path('google/callback/', google_auth_callback, name='google_auth_callback'),
    path('api/schedule-meeting/', schedule_meeting, name='schedule_meeting'),
    path('api/get-meetings/', get_meetings, name='get_meetings'),
]
