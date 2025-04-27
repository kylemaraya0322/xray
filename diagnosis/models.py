from django.db import models
from django.utils import timezone
from patient.models import Patient

class DiagnosisRecord(models.Model):
    patient       = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='history')
    diagnosed_at  = models.DateTimeField(default=timezone.now)
    label         = models.CharField(max_length=20)
    confidence    = models.FloatField()
    xray_image    = models.ImageField(
        upload_to='diagnosis_history/',
        blank=True,
        null=True,
        help_text="The exact X-ray image used for this diagnosis."
    )

    class Meta:
        ordering = ['-diagnosed_at']

    def __str__(self):
        return f"{self.diagnosed_at:%Y-%m-%d %H:%M} → {self.label} ({self.confidence*100:.1f}%)"
