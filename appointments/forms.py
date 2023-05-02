from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Patient
from .models import Appointment, Staff, StaffAvailability, Patient  # Add Patient import

WEEKDAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]

# Add the PatientForm
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'phone',
            'date_of_birth',
            'address',
            'email_address',  # Update this field name
            'notes',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'service', 'staff_member', 'date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['user']

class StaffAvailabilityForm(forms.ModelForm):
    class Meta:
        model = StaffAvailability
        fields = ['staff', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TextInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        help_text="Required.",
        error_messages={
            'unique': "A user with this email address already exists.",
        }
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

class AppointmentBookingForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'placeholder': 'yyyy-mm-dd',
            'type': 'date',
        }),
    )
    time = forms.TimeField(
        input_formats=['%H:%M'],
        widget=forms.TimeInput(attrs={
            'placeholder': 'hh:mm',
            'type': 'time',
        }),
    )

    class Meta:
        model = Appointment
        fields = ['date', 'time']

    def clean(self):
        cleaned_data = super().clean()
        staff_member = cleaned_data.get("staff_member")
        date_time = cleaned_data.get("date_time")

        if staff_member and date_time:
            conflicting_appointments = Appointment.objects.filter(
                staff_member=staff_member,
                date_time=date_time
            )

            if conflicting_appointments.exists():
                raise ValidationError("There is already an appointment scheduled for this staff member at this date and time.")

class RescheduleAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ServiceSearchForm(forms.Form):
    keyword = forms.CharField(label='Keyword', required=False)
    category = forms.CharField(label='Category', required=False)
