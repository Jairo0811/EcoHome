from django.contrib import admin
from .models import SecurityEvent, SecurityState
admin.site.register(SecurityEvent)
admin.site.register(SecurityState)
