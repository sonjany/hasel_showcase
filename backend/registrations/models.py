from django.db import models
from django.utils import timezone
from hashlib import sha256
from io import BytesIO
from django.core.files.base import ContentFile
from events.models import Event
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

class Registration(models.Model):
    class Role(models.TextChoices):
        ATTENDEE = "ATTENDEE", "Teilnehmer"
        GUIDE = "GUIDE", "Guide"
        HELPER = "HELPER", "Helfer"
        SPONSOR = "SPONSOR", "Sponsor"

    class Status(models.TextChoices):
        GOING = "GOING", "Zusage"
        WAITLISTED = "WAITLISTED", "Warteliste"
        NOT_GOING = "NOT_GOING", "Absage"
        CANCELLED = "CANCELLED", "Storniert"

    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name="registrations"
    )

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)

    role = models.CharField(max_length=12, choices=Role.choices, default=Role.ATTENDEE)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.GOING)
    
    organization = models.CharField(max_length=200, blank=True)
    comment = models.TextField(blank=True)


    #email = models.EmailField()
    #name = models.CharField(max_length=120, blank=True)
    #phone = models.CharField(max_length=40, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event", "role", "status"]),
            models.Index(fields=["event", "created_at"]),
    ]
        

    def __str__(self):
        return f"{self.first_name} {self.last_name} @ {self.event.title}"
    
class WaiverTemplate(models.Model):
    slug = models.SlugField(default="event-waiver")
    version = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("slug", "version")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.slug} v{self.version}"


def _default_device_id():
    import uuid
    return uuid.uuid4()

class WaiverAcceptance(models.Model):
    registration = models.OneToOneField(
        "registrations.Registration",
        on_delete=models.CASCADE,
        related_name="waiver",
    )
    template = models.ForeignKey(
        "registrations.WaiverTemplate",
        on_delete=models.PROTECT,
        related_name="acceptances",
    )
    accepted_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    device_id = models.UUIDField(default=_default_device_id, editable=False)

    content_hash = models.CharField(max_length=64, editable=False)
    pdf_file = models.FileField(upload_to="waivers/", null=True, blank=True)

    class Meta:
        ordering = ["-accepted_at"]

    def __str__(self):
        return f"Waiver {self.template} by {self.email} @ {self.accepted_at:%Y-%m-%d %H:%M}"

    def calc_conent_hash(self):
        payload = (
            f"{self.template.slug}|{self.template.version}|{self.template.body}|"
            f"{self.name}|{self.email}|{self.registration_id}|"
            f"{self.accepted_at or timezone.now()}"
        )    
        return sha256(payload.encode("utf-8")).hexdigest()
    
    def build_pdf_bytes(self):
        from io import BytesIO
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        try:
            pdfmetrics.registerFont(TTFont("DejaVu", "assets/fonts/DejaVuSans.ttf"))
            ase_font = "DejaVu"
        except Exception:
            base_font = "Helvetica"

        buf = BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=36, rightMargin=36, topMargin=48, bottomMargin=42,
            title=f"Waiver_{self.registration_id}_v{self.template.version}",
        )

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="TitleBig", parent=styles["Title"], fontName=base_font, fontSize=18, leading=22, spaceAfter=12))
        styles.add(ParagraphStyle(name="Body",     parent=styles["Normal"], fontName=base_font, fontSize=11, leading=15))
        styles.add(ParagraphStyle(name="Meta",     parent=styles["Normal"], fontName=base_font, fontSize=9,  textColor=colors.grey))
        styles.add(ParagraphStyle(name="MonoSmall",parent=styles["Normal"], fontName="Courier", fontSize=8,  leading=10))

        story = []
        story.append(Paragraph(self.template.title or "Haftungsausschluss", styles["TitleBig"]))
        story.append(Paragraph(f"Version: <b>{self.template.version}</b> &nbsp;•&nbsp; Slug: <b>{self.template.slug}</b>", styles["Meta"]))
        story.append(Spacer(1, 6))

        body = (self.template.body or "").strip()
        if body:
            for para in body.split("\n\n"):
                story.append(Paragraph(para.replace("\n", "<br/>"), styles["Body"]))
                story.append(Spacer(1, 4))
        else:
            story.append(Paragraph("— Kein Text hinterlegt —", styles["Meta"]))

        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=0.6, color=colors.black, spaceBefore=6, spaceAfter=6))
        story.append(Spacer(1, 4))

        data = [
            ["Name:", self.name or "—"],
            ["Email:", self.email or "—"],
            ["Registration ID:", str(self.registration_id)],
            ["Accepted at:", self.accepted_at.strftime("%Y-%m-%d %H:%M:%S") if self.accepted_at else "—"],
            ["IP:", (self.ip_address or "—") + "   UA: " + (self.user_agent or "—")],
            ["Device ID:", str(self.device_id)],
        ]
        tbl = Table(data, colWidths=[90, None])
        tbl.setStyle(TableStyle([
            ("FONTNAME", (0,0), (-1,-1), base_font),
            ("FONTSIZE", (0,0), (-1,-1), 10),
            ("VALIGN",   (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING",(0,0),(-1,-1),2),
            ("RIGHTPADDING",(0,0),(-1,-1),2),
            ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ]))
        story.append(Paragraph("Akzeptanz:", styles["Body"]))
        story.append(Spacer(1, 4))
        story.append(tbl)
        story.append(Spacer(1, 8))

        story.append(Paragraph("Hash (SHA-256):", styles["Body"]))
        story.append(Paragraph(self.content_hash or "—", styles["MonoSmall"]))

        def _footer(canvas, doc_):
            canvas.setFont(base_font, 8)
            canvas.setFillGray(0.5)
            w, h = A4
            canvas.drawRightString(w - 36, 28, f"Seite {doc_.page}")
            canvas.setFillGray(0)

        doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
        return buf.getvalue()

    
    def save(self, *args, **kwargs):
        creating = self._state.adding
        if not self.content_hash:
            if not self.accepted_at:
                self.accepted_at = timezone.now()
            self.content_hash = self.calc_content_hash()
        super().save(*args, **kwargs)
        if creating and not self.pdf_file:
            pdf_bytes = self.build_pdf_bytes()
            fname = f"waiver_{self.registration_id}_v{self.template.version}.pdf"
            self.pdf_file.save(fname, ContentFile(pdf_bytes), save=True)
