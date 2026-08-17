from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ResourceLimitViewSet, history, summary

router = DefaultRouter()
router.register("limits", ResourceLimitViewSet, basename="resource-limit")

urlpatterns = [
    path("summary/", summary, name="resource-summary"),
    path("history/", history, name="resource-history"),
    path("", include(router.urls)),
]
