from rest_framework import serializers
from .models import Registration
from .models import Event
from .models import WaiverAcceptance



class WaiverAcceptanceSerializer(serializers.ModelSerializer):
    registration = serializers.SerializerMethodField()
    template_version = serializers.IntegerField(source="template.version", read_only=True)
    pdf_url = serializers.FileField(source="pdf-file", read_only=True)



    class Meta:
        model = WaiverAcceptance
        fields = [
            "id", "accepted_at",
            "name", "email",
            "registration", "template_version",
            "content_hash", "pdf_url",
        ]

    def get_registration(self, obj):
        r = obj.registration
        return {"id":r.id,
                "event": getattr(r.event, "title", None)
                }
    

class RegistrationSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Registration
        fields = [
            "id", "event",
            "first_name", "last_name", #"email",
            "role", "status",
            "organization", "comment",
            "created_at", "updatet_at",
        ]
        read_only_fields = ["id", "created_at", "updatet_at"]