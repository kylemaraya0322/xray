from django.db import models

# Create your models here.
from django.db import models
from datetime import date

class Employee(models.Model):
    STATUS_CHOICES = [
        ('On Duty', 'On Duty'),
        ('On Leave', 'On Leave'),
        ('Absent',  'Absent'),
    ]

    employee_id    = models.CharField(max_length=5, unique=True, editable=False)
    first_name     = models.CharField(max_length=100)
    middle_name    = models.CharField(max_length=100, blank=True, null=True)
    last_name      = models.CharField(max_length=100)
    email          = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    position       = models.CharField(max_length=100)
    department     = models.CharField(max_length=100)
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default='On Duty')
    photo          = models.ImageField(upload_to='employee_photos/', blank=True, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate employee_id on first save
        if not self.employee_id:
            last = Employee.objects.order_by('-employee_id').first()
            if last and last.employee_id.isdigit():
                new_id = int(last.employee_id) + 1
            else:
                new_id = 0
            self.employee_id = str(new_id).zfill(5)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} – {self.first_name} {self.last_name}"
