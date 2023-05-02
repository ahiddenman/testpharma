from django.db import models
from django.utils import timezone

class Invoice(models.Model):
    appointment = models.OneToOneField('appointments.Appointment', on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_due = models.DateTimeField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.pk} for Appointment {self.appointment.pk}"
