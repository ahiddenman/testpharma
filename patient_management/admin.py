# patient_management/admin.py
from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name',)
    list_display = ('first_name', 'last_name', 'date_of_birth', 'phone_number', 'email',)
