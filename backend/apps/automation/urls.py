from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AlertViewSet, AutomationRuleViewSet

router = DefaultRouter()
router.register("alerts", AlertViewSet, basename="alert")
router.register("rules", AutomationRuleViewSet, basename="automation-rule")

urlpatterns = [path("", include(router.urls))]
