from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WaiverAcceptanceViewSet
from .views import RegistrationViewSet


router = DefaultRouter()
router.register(r"registrations", RegistrationViewSet, basename="registration")
router.register(r"waivers", WaiverAcceptanceViewSet, basename="waivers")

urlpatterns = [
    path("", include(router.urls)),
    #path("waiver/status/", waiver_status),
]
