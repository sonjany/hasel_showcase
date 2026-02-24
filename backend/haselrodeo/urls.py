"""
URL configuration for haselrodeo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# from django.http import HttpResponse
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


#from rest_framework.routers import DefaultRouter
#from django.http import JsonResponse
#from events.views import EventViewSet
#from registrations.views import RegistrationViewSet
#from quarries.views import QuarryViewSet

#router = DefaultRouter()
#router.register(r"events", EventViewSet, basename="events")
#router.register(r"registrations", RegistrationViewSet, basename="registration")
#router.register(r"quarries", QuarryViewSet, basename="quarry")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/events/", include("events.urls")),
    path("api/registrations/", include("registrations.urls")),
    path("api/quarries/", include("quarries.urls"))
    #path("api/ping", lambda r:JsonResponse({"pong": True})),
    #path("api/", include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
