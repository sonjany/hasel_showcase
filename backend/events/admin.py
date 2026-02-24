from django.contrib import admin
from .models import Event, ScheduleItem, FoodServiceWindow, ScheduleSlot


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "start",
        "end",
        "location",
        "capacity",
        "created_at"
    )
    list_filter = (
        "title",
        "location",
        "description"
    )
    search_fields = (
        "start",
        "location"
    )
    ordering = (
        "start",
    )

@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "title",
        "start",
        "order"
    )
    list_filter = (
        "event",
    )
    search_fields = (
        "title",
        "description",
        "event__title"
    )
    ordering = (
        "event",
        "start",
        "order"
    )

@admin.register(FoodServiceWindow)
class FoodServiceWindowAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "kind",
        "vendor",
        "start",
        "end",
        "location"
    )
    list_filter = (
        "kind",
        "event",
    )
    search_fields = (
        "vendor",
        "location",
    )
    

@admin.register(ScheduleSlot)
class ScheduleSlotAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "group",
        "quarry",
        "kind",
        "start",
        "end",
    )
    list_filter = (
        "event",
        "quarry",
        "kind",
        "group"
    )
    search_fields = (
        "group",
        #"quarry__name",
        "event__title"
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.kind == ScheduleSlot.SlotKind.BREAK:
            form.base_fields["quarry"].required = False
        return form    


