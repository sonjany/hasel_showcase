#from django.shortcuts import render
from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from .models import WaiverAcceptance
from .serializers import WaiverAcceptanceSerializer
from .models import Registration
from .serializers import RegistrationSerializer

class WaiverAcceptanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WaiverAcceptance.objects.select_related("registration", "template").order_by("-accepted_at")
    serializer_class = WaiverAcceptanceSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params
        if "event" in q:
            qs = qs.filter(registration__event_id=q["event"])
        if "email" in q:
            qs = qs.filter(email__icontains=q["email"])
        if "name" in q:
            qs = qs.filter(name__icontains=q["name"])
        if "date_from" in q:
            dt = parse_datetime(q["date_from"])
            if dt: qs = qs.filter(accepted_at__gte=dt)
        if "date_to" in q:
            dt = parse_datetime(q["date_to"])
            if dt: qs = qs.filter(accepted_at__lte=dt)
        return qs


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.select_related("event").order_by("-created_at")
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "first_name",
        "last_name",
        #"email",
        "organization",
        "comment"]
    ordering_fields = [
        "created_at"
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        event_id = self.request.query_params.get("event")
        if event_id:
            qs = qs.filter(event_id=event_id)
        status_ = self.request.query_params.get("status")
        if status_:
            qs = qs.filter(status=status_)
        role_ = self.request.query_params.get("role")
        if role_:
            qs = qs.filter(role=role_)
        return qs