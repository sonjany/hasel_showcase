from rest_framework.routers import DefaultRouter
from .views import QuarryViewSet

router = DefaultRouter()
router.register(r"", QuarryViewSet, basename="quarry")

urlpatterns = router.urls