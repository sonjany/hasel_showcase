from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

# from django.http import JsonResponse
from .views import EventViewSet

router = DefaultRouter()
router.register(r"", EventViewSet, basename="event")
#router.register(r"schedule-items", ScheduleItemViewSet, basename="schedule-items")
#router.register(r"registrations", RegistrationViewSet, basename="registrations")

urlpatterns = router.urls


"""[
    path("", views.events_list),
    path("ping/", ping),
    path("", include(router.urls)),
]"""
