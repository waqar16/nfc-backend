"""
URL configuration for nfc_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from schema_graph.views import Schema
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def trigger_error(request):
    division_by_zero = 1 / 0


schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    path('sentry-debug/', trigger_error),

    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/social/', include('allauth.socialaccount.urls')),

    path("admin/", admin.site.urls),

    path("", include("authentication.urls")),

    path("api/", include("analytics.urls")),

    path("api/", include("individual.urls")),

    path("api/", include("company.urls")),

    # path("api/", include("nfc_management.urls")),

    path("", include("appointments.urls")),

    path("schema/", Schema.as_view()),

    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
