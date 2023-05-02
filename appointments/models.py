from django.db import models
from django.conf import settings
from .models_invoice import Invoice
from datetime import date

class Service(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, default=None, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True)

    def __str__(self):
        return self.name

class Pharmacy(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.name

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()
    email_address = models.EmailField(max_length=254, null=True, blank=True)
    notes = models.TextField(blank=True)

class Appointment(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
        (COMPLETED, 'Completed'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    staff_member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f'{self.patient} - {self.service} - {self.date_time}'

class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, default=1)  # Add default value
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# class Staff(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     availability = models.BooleanField(default=True)

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'

#     class Meta:
#         verbose_name_plural = "Staff"

# class Availability(models.Model):
#     staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='staff_availability')
#     date = models.DateField(default=date.today)
#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     def __str__(self):
#         return f'{self.staff} - {self.date} - {self.start_time} - {self.end_time}'

class StaffAvailability(models.Model):
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='availabilities')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.staff} available from {self.start_time} to {self.end_time}"
