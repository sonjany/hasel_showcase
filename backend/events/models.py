from django.db import models


# Hauptevent anlegen
class Event(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    capacity = models.PositiveBigIntegerField(default=0)  # 0 -> unbegrenzt, später ändern
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Klasse Meta erlaubt zusätzliche Optionen für das Verhalten von Models
    # ordering->Standardsortierung Datenbankabfrage->aufsteigend
    class Meta:
        ordering = ["start"]

    def __str__(self):
        return self.title
    
#Event Programm anlegen
class ScheduleItem(models.Model):
    event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, related_name="schedule_items")
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ["start", "order"]

    def __str__(self):
        return f"{self.title} ({self.event.title})"
    

class FoodServiceWindow(models.Model):
    class Kind(models.TextChoices):
        FOODTRUCK = "FOODTRUCK", "Foodtruck"
        LUNCH = "LUNCH", "Mittagessen"
        DINNER = "DINNER", "Abendessen"
        BREAKFAST = "BREAKFAST", "Frühstück"
        SNACK = "SNACK", "Snack"
    
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="food_windows")
    vendor = models.CharField(max_length=200, blank=True)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.FOODTRUCK)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = [
            "start"
        ]
    

    def __str__(self):
        return f"{self.get_kind_display()} @ {self.event.title}"
    

class ScheduleSlot(models.Model):
    class SlotKind(models.TextChoices):
        DRIVING = "DRIVING", "Fahren"
        BREAK = "BREAK", "Pause"

    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="schedule_slots")
    group = models.CharField(max_length=50)
    quarry = models.ForeignKey("quarries.Quarry", null=True, blank=True, on_delete=models.SET_NULL, related_name="slots")
    kind = models.CharField(max_length=10, choices=SlotKind.choices, default=SlotKind.DRIVING)
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        ordering = [
            "start",
            "group"
        ]

    def __str__(self):
        base = f"{self.group}: {self.start:%Y-%m-%d %H:%M}"
        return f"[{self.get_kind_display()}] {base}"
        #return f"{self.group} -> {self.quarry.name} ({self.event.title})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.kind == self.SlotKind.DRIVING and not self.quarry:
            raise ValidationError("Für Slots muss ein Steinbruch angegeben sein!")
        



#Klassen der jeweiligen Rollen und dem Status der Registrierung anlegen
"""class RegistrationRole(models.TextChoices):
    ATTENDEE = "ATTENDEE", "Teilnehmer"
    HELPER = "HELPER", "Helfer"
    SPONSOR = "SPONSOR", "Sponsor"


class RegistrationStatus(models.TextChoices):
    GOING = "GOING", "Zusage"
    WAITLISTED = "WAITLISTED", "Warteliste"
    NOT_GOING = "NOT_GOING", "Absage"""


# Anmeldung für bestimmtes Event
"""class Registration(models.Model):
    event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, related_name="registrations"
    )
    role = models.CharField(
        max_length=10,
        choices=RegistrationRole.choices,
        default=RegistrationRole.ATTENDEE,
    )
    status = models.CharField(
        max_length=12,
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.GOING,
    )
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField()

    # zusatzinfos->Sponsoren, Organisationen
    organization = models.CharField(max_length=200, blank=True)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # neueste Registrierungen zuerst

    # selbe email kann sich nur einmal anmelden
    constraints = [
        models.UniqueConstraint(fields=["event", "email"], name="uniq_event_email"),
    ]

    indexes = [
        models.Index(fields=["event", "role", "status"]),
        models.Index(fields=["event", "created_at"]),
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role}) @ {self.event.title}"""


