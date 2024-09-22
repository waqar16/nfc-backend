from django.urls import path
from . import views

urlpatterns = [
    path('auth/users/', views.CustomUserCreateView.as_view(), name='user-create'),
    path('auth/delete-user/', views.DeleteGoogleAccountView.as_view(), name='delete_user_account'),
    path('auth/custom-google-login/', views.CustomGoogleLogin.as_view(), name='custom_google_login'),
    path('auth/custom/token/login/', views.CustomTokenCreateView.as_view(), name='token_login'),
]
