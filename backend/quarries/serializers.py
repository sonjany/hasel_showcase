from rest_framework import serializers
from .models import Quarry

class QuarrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarry
        fields = [
            "id",
            "name",
            "latitude",
            "longitude",
            "gpx_url",
            "description"
        ]