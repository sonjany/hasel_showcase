# from django.shortcuts import render
# from rest_framework.response import Response
#from django.db import IntegrityError
from django.db.models import Count, Q

#from django.http import JsonResponse
from rest_framework import filters, viewsets
#from rest_framework.decorators import api_view, permission_classes
#from rest_framework.exceptions import ValidationError
#from rest_framework.permissions import AllowAny, IsAdminUser
#from rest_framework.response import Response
#from rest_framework.throttling import ScopedRateThrottle

from .models import Event
from registrations.models import Registration
from .serializers import (
    EventDetailSerializer,
    EventListSerializer
)

"""@api_view(["GET"])
@permission_classes([AllowAny])
def ping(_request):
    return Response({"status": "ok", "pong": True})"""

REL = "registrations"

class EventViewSet(viewsets.ModelViewSet):
    def get_queryset(self): 
        qs = Event.objects.annotate(
            going_attendees=Count(
                REL,
                filter=Q(
                    **{
                        f"{REL}__status": Registration.Status.GOING,
                        f"{REL}__role": Registration.Role.ATTENDEE,
                    }
                ),
                distinct=True,
            ),
            going_guides=Count(
                REL,
                filter=Q(
                    **{
                        f"{REL}__role": Registration.Role.GUIDE,
                        f"{REL}__status": Registration.Status.GOING,
                    }
                ),
                distinct=True,
            ),
        )
        return qs
    
    def get_serializer_class(self):
        return EventDetailSerializer if self.action == "retrieve" else EventListSerializer


    # sortieren und suchen
    """filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["start", "title"]
    search_fields = ["title", "location", "description"]

    # lese- und schreibberechtigungen->schreiben nur Admin
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

    # listen,erstellen, update+registrierung/Schedule
    def get_serializer_class(self):
        if self.action in ["list", "create", "update", "partial_update"]:
            return EventListSerializer
        return EventDetailSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.select_related("event").all()
    serializer_class = RegistrationSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["created_at"]
    search_fields = ["first_name", "last_name", "email", "organisation"]

    # anzahl der Anfragen steuern->Spamschutz
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "registrations-create"

    # Schreibberechtigung User->anmelden/Rest nur Admin
    def get_permissions(self):
        if self.action in ["create"]:
            return [AllowAny()]
        return [IsAdminUser()]

    # zusätzliche Filter->API fexibel ohne Endpunkte für jeden Filter
    def get_queryset(self):
        qs = super().get_queryset()
        event_id = self.request.query_params.get("event")
        role = self.request.query_params.get("role")
        status_param = self.request.query_params.get("status")
        if event_id:
            qs = qs.filter(event_id=event_id)
        if role:
            qs = qs.filter(role=role)
        if status_param:
            qs = qs.filter(status=status_param)
        return qs
    
    def events_list(request):
        return JsonResponse({"events": []})


    # Status bei anlegen von Teilnehmern automatisch berechnen
    def perform_create(self, serializer):
        event = serializer.validated_data["event"]
        role = serializer.validated_data.get("role", RegistrationRole.ATTENDEE)

        # Kapazitätsprüfung->begrenzte anzahl Teilnehmer
        if role == RegistrationRole.ATTENDEE and event.capacity:
            going_attendees = event.registrations.filter(
                role=RegistrationRole.ATTENDEE, status=RegistrationStatus.GOING
            ).count()
            status_value = (
                RegistrationStatus.GOING
                if going_attendees < event.capacity
                else RegistrationStatus.WAITLISTED
            )
        # Sponsoren/Helfer aus capacity rausnehmen
        else:
            status_value = RegistrationStatus.GOING
        # keine doppelte anmeldung für event
        try:
            serializers.save(status=status_value)
        except IntegrityError:
            raise ValidationError({"email": "Du bist bereits registriert"})


class ScheduleItemViewSet(viewsets.ModelViewSet):
    queryset = ScheduleItem.objects.select_related("event").all()
    serializer_class = ScheduleItemSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["start", "order"]
    search_fields = ["title", "description"]

    # leseberechtigungen->ändern nur Admin
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]"""
