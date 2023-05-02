from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ServiceSearchForm
from .models import Appointment, Service, Staff, StaffAvailability, Pharmacy
from datetime import date
from .forms import AppointmentForm, StaffForm, StaffAvailabilityForm
from django.views.generic import ListView
from .models import Patient
from .forms import PatientForm
from django.http import HttpResponse
from django.contrib import messages
from .forms import PatientForm, UserUpdateForm
from .models import Patient, Appointment
from authentication.models import CustomUser
from .forms import AppointmentBookingForm
from .models import Staff
from .models import Invoice
from .models import Appointment, Invoice
from django.utils import timezone
from datetime import timedelta
from .models import Staff, StaffAvailability
from appointments.forms import RescheduleAppointmentForm

# ... (your existing views)

def test(request):
    return HttpResponse("Test view")

def staff_management(request):
    staff_members = Staff.objects.all()
    context = {'staff_members': staff_members}
    return render(request, 'appointments/staff_management.html', context)

def appointment_management(request):
    appointments = Appointment.objects.all()
    context = {'appointments': appointments}
    return render(request, 'appointments/appointment_management.html', context)

def calendar_view(request):
    appointments = Appointment.objects.all()
    context = {'appointments': appointments}
    return render(request, 'appointments/calendar_view.html', context)

def staff_availability(request):
    staff_members = Staff.objects.all()
    availabilities = Availability.objects.all()  # Add this line to define availabilities
    return render(request, 'appointments/staff_availability.html', {'availabilities': availabilities, 'staff_members': staff_members})

def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments:appointment_management')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/create_appointment.html', {'form': form})

def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments:appointment_management')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/edit_appointment.html', {'form': form, 'appointment': appointment})

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('appointments:appointment_management')

def create_staff(request):
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments:staff_management')
    else:
        form = StaffForm()
    return render(request, 'appointments/create_staff.html', {'form': form})

def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('appointments:staff_management')
    else:
        form = StaffForm(instance=staff)
    return render(request, 'appointments/edit_staff.html', {'form': form, 'staff': staff})

def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    staff.delete()
    return redirect('appointments:staff_management')

def add_availability(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == "POST":
        form = StaffAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.staff = staff
            availability.save()
            return redirect('appointments:staff_availability')
    else:
        form = StaffAvailabilityForm()
    return render(request, 'appointments/add_availability.html', {'form': form, 'staff': staff})

def edit_availability(request, availability_id):
    availability = get_object_or_404(StaffAvailability, pk=availability_id)
    if request.method == 'POST':
        form = StaffAvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            return redirect('appointments:staff_availability')
    else:
        form = StaffAvailabilityForm(instance=availability)
    return render(request, 'appointments/edit_availability.html', {'form': form})

def delete_availability(request, availability_id):
    availability = get_object_or_404(StaffAvailability, id=availability_id)
    availability.delete()
    return redirect('appointments:staff_management')

def patient_detail(request, pk):
    patient = get_object_or_404(Patient, user_id=pk)
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, 'appointments/patient_detail.html', {'patient': patient, 'appointments': appointments})

def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments:patient_list')
    else:
        form = PatientForm()
    return render(request, 'appointments/patient_create.html', {'form': form})

def patient_update(request, pk):
    patient = get_object_or_404(Patient, user__id=pk)
    user = patient.user

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        patient_form = PatientForm(request.POST, instance=patient)

        if user_form.is_valid() and patient_form.is_valid():
            user_form.save()
            patient_form.save()
            messages.success(request, 'Patient updated successfully.')
            return HttpResponseRedirect(reverse('appointments:patient_list'))

    else:
        user_form = UserUpdateForm(instance=user)
        patient_form = PatientForm(instance=patient)

    return render(request, 'appointments/patient_update.html', {'user_form': user_form, 'patient_form': patient_form})

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, user_id=pk)
    if request.method == "POST":
        Appointment.objects.filter(patient=patient).delete()
        patient.delete()
        return redirect("appointments:patient_list")
    return render(request, "appointments/patient_delete.html", {"patient": patient})

# I have updated the imports and the book_appointment function below
@login_required
def book_appointment(request, pharmacy_id, service_id, staff_id):
    service = get_object_or_404(Service, id=service_id)
    staff_member = get_object_or_404(User, id=staff_id)
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)

    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.staff_member = staff_member
            appointment.service = service
            appointment.pharmacy = pharmacy
            
            # Combine date and time fields from the form
            appointment_date = form.cleaned_data['date']
            appointment_time = form.cleaned_data['time']
            appointment.date_time = datetime.combine(appointment_date, appointment_time)
            
            appointment.save()

            # Create an invoice for the booked appointment
            invoice = Invoice(
                appointment=appointment,
                date_due=timezone.now() + timedelta(days=14),
                amount_due=100,  # Replace this with the actual amount due
            )
            invoice.save()

            return HttpResponseRedirect(reverse('appointments:book_appointment_success', kwargs={'invoice_id': invoice.id}))
    else:
        form = AppointmentBookingForm()

    context = {
        'form': form,
        'staff': staff,
        'service': service,
    }
    return render(request, 'appointments/book_appointment.html', context)

def book_appointment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    return render(request, 'appointments/book_appointment_success.html', {'appointment': appointment})

def index(request):
    return render(request, 'appointments/index.html')

class PatientListView(ListView):
    model = Patient
    queryset = Patient.objects.all()
    template_name = 'appointments/patient_list.html'
    context_object_name = 'patients'

@login_required
def list_staff(request):
    staff_list = Staff.objects.all()
    return render(request, 'staff_list.html', {'staff_list': staff_list})

def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'appointments/invoice_list.html', {'invoices': invoices})

def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'appointments/invoice_detail.html', {'invoice': invoice})

@login_required
def upcoming_appointments(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    appointments = Appointment.objects.filter(patient=patient, date_time__gte=timezone.now()).order_by('date_time')
    return render(request, 'appointments/upcoming_appointments.html', {'appointments': appointments})

@login_required
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if the appointment belongs to the logged-in user
    if request.user.patient != appointment.patient:
        messages.error(request, "You can only reschedule your own appointments.")
        return redirect('appointments:upcoming_appointments')

    if request.method == 'POST':
        form = RescheduleAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Your appointment has been rescheduled.")
            return redirect('appointments:upcoming_appointments')
    else:
        form = RescheduleAppointmentForm(instance=appointment)

    context = {'form': form, 'appointment': appointment}
    return render(request, 'appointments/reschedule_appointment.html', context)

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient__user=request.user)
    appointment.delete()
    messages.success(request, 'Appointment successfully canceled.')
    return HttpResponseRedirect(reverse('appointments:upcoming_appointments'))

def search_services(request):
    query = request.GET.get('query', '')
    services = Service.objects.filter(name__icontains=query)
    return render(request, 'appointments/search_services.html', {'services': services, 'query': query})

def select_pharmacy(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    pharmacies = Pharmacy.objects.all()  # Assuming you have a Pharmacy model
    return render(request, 'appointments/select_pharmacy.html', {'service': service, 'pharmacies': pharmacies})

def index(request):
    if request.method == 'POST':
        form = ServiceSearchForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            category = form.cleaned_data['category']
            
            search_results = Service.objects.all()
            
            if keyword:
                search_results = search_results.filter(name__icontains=keyword)
                
            if category:
                search_results = search_results.filter(category__icontains=category)
        else:
            search_results = None
    else:
        form = ServiceSearchForm()
        search_results = None

    popular_services = Service.objects.all()[:5]  # Adjust this query to fetch popular services as needed

    context = {
        'form': form,
        'search_results': search_results,
        'popular_services': popular_services,
    }
    return render(request, 'appointments/index.html', context)

def services_list(request, pharmacy_id):
    pharmacy = get_object_or_404(Pharmacy, id=pharmacy_id)
    services = pharmacy.services.all()
    context = {'services': services, 'pharmacy_id': pharmacy_id}
    return render(request, 'appointments/services_list.html', context)


    