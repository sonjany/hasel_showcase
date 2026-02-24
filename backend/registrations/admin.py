from django.contrib import admin
from .models import Registration

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "first_name",
        "last_name",
        #"get_email",
        "role",
        "status",
        "created_at"
    )
    list_filter = (
        "role",
        "status",
        "event",
        "created_at",
    )
    search_fields = (
        "first_name",
        "last_name",
        #"email",
        "organization",
        "comment"
    )
    ordering = (
        "-created_at",
    )
    autocomplete_fields = (
        "event",
    )
    

    #def get_email(self,obj):
        #return getattr(obj, "email", "")
    #get_email.short_description = "Email"
    #get_email.admin_order_field = "email"