from django.db import models
from datetime import date

class Patient(models.Model):
    
    
    # Auto-generated unique patient ID, 5 digits with leading zeros
    patient_id = models.CharField(
        max_length=5,
        unique=True,
        editable=False
    )

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    DIAGNOSIS_CHOICES = [
        ('Pending', 'Pending'),
        ('No Findings', 'No Findings'),
        ('PTB', 'PTB'),
    ]
    
    diagnosis      = models.CharField(
        max_length=20,
        choices=DIAGNOSIS_CHOICES,
        default='Pending'
    )
    confidence     = models.FloatField(
        null=True,
        blank=True,
        help_text="Model confidence (0–1) for the last diagnosis"
    )
    

    first_name     = models.CharField(max_length=100)
    middle_name    = models.CharField(max_length=100, blank=True, null=True)
    last_name      = models.CharField(max_length=100)
    gender         = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthdate      = models.DateField()
    age            = models.PositiveIntegerField(editable=False)
    contact_number = models.CharField(max_length=20)
    diagnosis      = models.CharField(
        max_length=20,
        choices=DIAGNOSIS_CHOICES,
        default='Pending'
    )

    def save(self, *args, **kwargs):
        # Generate patient_id on first save
        if not self.patient_id:
            # Get the last patient ordered by patient_id
            last = Patient.objects.order_by('-patient_id').first()
            if last and last.patient_id.isdigit():
                next_int = int(last.patient_id) + 1
            else:
                next_int = 0
            # Format as 5-digit string with leading zeros
            self.patient_id = f"{next_int:05d}"

        # Calculate age from birthdate
        today = date.today()
        self.age = (
            today.year - self.birthdate.year
            - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.patient_id}] {self.first_name} {self.last_name}"


