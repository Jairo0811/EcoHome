from django.contrib import admin

from .models import Device, Telemetry

admin.site.register(Device)
admin.site.register(Telemetry)
