from django.contrib import admin
from .models import UserProfile, ShareProfile, Receivedprofile

admin.site.register(UserProfile)
admin.site.register(ShareProfile)
admin.site.register(Receivedprofile)
