from django.contrib import admin
from .models import Appointment, Invoice, Patient, Service, Staff, Pharmacy

admin.site.register(Appointment)
admin.site.register(Service)
admin.site.register(Patient)
admin.site.register(Staff)
admin.site.register(Invoice)
admin.site.register(Pharmacy)