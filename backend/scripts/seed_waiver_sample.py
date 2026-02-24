from django.utils import timezone
from django.conf import settings

from events.models import Event
from registrations.models import (
    Registration,
    WaiverTemplate,
    WaiverAcceptance,
)

def ensure_event():
    evt = Event.objects.order_by("start").first()
    if evt is None:
        evt = Event.objects.create(
            title="Test-Event",
            start=timezone.now(),
            location="Steinbruch I",
            description="Seeded test event",
            capacity=0,
        )
        print(f"[seed] Created Event id={evt.id}")
    else:
        print(f"[seed] Using Event id={evt.id}")
    return evt

def ensure_template():
    tmpl = WaiverTemplate.objects.filter(is_active=True).order_by("-version").first()
    if tmpl is None:
        tmpl = WaiverTemplate.objects.create(
            slug="event-waiver",
            version=1,
            title="Haftungsausschluss",
            body="Ich bestätige, dass ich auf eigene Gefahr teilnehme.",
            is_active=True,
        )
        print(f"[seed] Created WaiverTemplate v{tmpl.version}")
    else:
        print(f"[seed] Using WaiverTemplate v{tmpl.version}")
    return tmpl

def ensure_registration(evt):
    reg = Registration.objects.filter(waiver__isnull=True).first()
    if reg is None:
        reg = Registration.objects.create(
            event=evt,
            first_name="Test",
            last_name="User",
            # email ist im Registration-Modell optional – Waiver bekommt eigene Email
        )
        print(f"[seed] Created Registration id={reg.id}")
    else:
        print(f"[seed] Using Registration id={reg.id} (no waiver yet)")
    return reg

def ensure_waiver_acceptance(reg, tmpl):
    # Falls schon ein Waiver existiert, zurückgeben
    if hasattr(reg, "waiver"):
        acc = reg.waiver
        print(f"[seed] Existing WaiverAcceptance id={acc.id}")
        return acc

    # Neue Acceptance erzeugen → generiert PDF
    acc = WaiverAcceptance.objects.create(
        registration=reg,
        template=tmpl,
        name=f"{(reg.first_name or 'Vorname')} {(reg.last_name or 'Nachname')}".strip(),
        email="test@example.com",
    )
    print(f"[seed] Created WaiverAcceptance id={acc.id}")
    return acc

def main():
    evt = ensure_event()
    tmpl = ensure_template()
    reg = ensure_registration(evt)
    acc = ensure_waiver_acceptance(reg, tmpl)

    # Ausgabe
    media_root = getattr(settings, "MEDIA_ROOT", None)
    print(f"[seed] MEDIA_URL: {getattr(settings, 'MEDIA_URL', '/media/')}")
    if acc.pdf_file:
        print(f"[seed] PDF URL : {acc.pdf_file.url}")
        print(f"[seed] PDF PATH: {acc.pdf_file.path}")
    else:
        print("[seed] WARN: No pdf_file present")

if __name__ == "__main__":
    main()
