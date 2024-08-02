from django.urls import path
from . import views

urlpatterns = [
    # path('profile_type/', views.profile_type, name='profile_type'),
    path('auth/users/', views.CustomUserCreateView.as_view(), name='user-create'),
    # path('auth/user/<int:pk>/', views.public_user_detail_view, name='user-detail'),
    # path('auth/social/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('auth/delete-user/', views.DeleteGoogleAccountView.as_view(), name='delete_user_account'),
    path('auth/custom-google-login/', views.CustomGoogleLogin.as_view(), name='custom_google_login'),
    # path('auth/verify/', views. VerifyCodeView.as_view(), name='verify-code'),
    # path('auth/custom_register/', views.custom_register, name='custom_register'),
]
