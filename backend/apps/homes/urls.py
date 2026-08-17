from rest_framework.routers import DefaultRouter

from .views import HomeViewSet, RoomViewSet

router = DefaultRouter()
router.register("homes", HomeViewSet, basename="home")
router.register("rooms", RoomViewSet, basename="room")

urlpatterns = router.urls
