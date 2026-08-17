from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SecurityEventViewSet, SecurityStateViewSet

router = DefaultRouter()
router.register("events", SecurityEventViewSet, basename="security-event")
router.register("states", SecurityStateViewSet, basename="security-state")
urlpatterns = [path("", include(router.urls))]
