from django.db import models
import uuid, os

def photo_upload_path(instance, filename):
    # discard original name, keep only extension
    ext = filename.split('.')[-1].lower()
    # generate a short uuid filename, e.g. "a3f1b2c4d5e6f7g8h9i0.jpg"
    name = uuid.uuid4().hex
    return os.path.join('employees', f"{name}.{ext}")
class Employee(models.Model):
    STATUS_CHOICES = [
        ('On Duty', 'On Duty'),
        ('On Leave', 'On Leave'),
        ('Absent',   'Absent'),
    ]
    


    # auto-increment integer PK by default; but we want a custom 5-digit code:
    employee_id = models.CharField(max_length=5, unique=True, editable=False)
    first_name  = models.CharField(max_length=50)
    middle_name = models.CharField(
    max_length=50,
    blank=True,
    default=''   # ensure the DB and Django agree on an empty-string default
)
    last_name   = models.CharField(max_length=50)
    email       = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    position    = models.CharField(max_length=100)
    department  = models.CharField(max_length=100)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='On Duty')
    photo       = models.ImageField(upload_to='employees/photos/',max_length=255, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # On first save, generate 00001, 00002, …:
        if not self.employee_id:
            last = Employee.objects.order_by('-id').first()
            num  = int(last.employee_id) + 1 if last else 1
            self.employee_id = f"{num:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} – {self.first_name} {self.last_name}"
