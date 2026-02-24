from django.contrib import admin
from .models import Quarry

@admin.register(Quarry)
class QuarryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "latitude",
        "longitude",
        "gpx_url",
        "created_at"
    )
    search_fields = (
        "name",
        "description"
    )
