from rest_framework import serializers
from .models import Event, ScheduleItem, FoodServiceWindow, ScheduleSlot


#Programmpunkte-> Felder aus Model übernehmen
class ScheduleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleItem
        fields = [
            "id",
            "start",
            "end",
            "title",
            "description",
            "order"
        ]


class EventListSerializer(serializers.ModelSerializer):
    going_attendees = serializers.IntegerField(
        read_only=True
    )
    going_guides = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "start",
            "end",
            "location",
            "capacity",
            "going_attendees",
            "going_guides",
        ]


"""class EventDetailSerializer(serializers.ModelSerializer):
    schedule_items = ScheduleItemSerializer(
        many=True, 
        read_only=True
    )

    class Meta(EventListSerializer.Meta):
        fields = EventListSerializer.Meta.fields + [
            "description",
            "schedule_items"
        ]"""


class FoodServiceWindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodServiceWindow
        fields = [
            "id",
            "kind",
            "vendor",
            "start",
            "end",
            "location"
        ]

class ScheduleSlotSerializer(serializers.ModelSerializer):
    #quarry_name = serializers.CharField(source="quarry.name", read_only=True)
    quarry_name = serializers.SerializerMethodField()
    quarry_gpx_url = serializers.SerializerMethodField()

    class Meta:
        model = ScheduleSlot
        fields = [
            "id",
            "group",
            "quarry",
            "quarry_name",
            "quarry_gpx_url",
            "kind",
            "start",
            "end"
        ]

    def get_quarry_name(self, obj):
        return obj.quarry.name if obj.quarry else None
    
    def get_quarry_gpx_url(self, obj):
        return getattr(obj.quarry, "gpx_url", None) if obj.quarry else None


class EventDetailSerializer(EventListSerializer):
    schedule_items = ScheduleItemSerializer(many=True, read_only=True)
    food_windows = FoodServiceWindowSerializer(many=True, read_only=True)
    schedule_slots = ScheduleSlotSerializer(many=True, read_only=True)

    class Meta(EventListSerializer.Meta):
        fields = EventListSerializer.Meta.fields + [
            "description",
            "schedule_items",
            "food_windows",
            "schedule_slots",
        ]
