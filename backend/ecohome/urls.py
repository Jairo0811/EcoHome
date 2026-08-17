from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", include("apps.core.urls")),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.homes.urls")),
    path("api/v1/", include("apps.devices.urls")),
    path("api/v1/iot/", include("apps.iot.urls")),
    path("api/v1/resources/", include("apps.resources.urls")),
    path("api/v1/dashboard/", include("apps.dashboard.urls")),
]
