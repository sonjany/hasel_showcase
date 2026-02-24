#from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Quarry
from .serializers import QuarrySerializer

class QuarryViewSet(viewsets.ModelViewSet):
    queryset = Quarry.objects.all()
    serializer_class = QuarrySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "name",
        "description"
    ]
    ordering_fields = [
        "name"
    ]
