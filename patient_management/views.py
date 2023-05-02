# patient_management/views.py
from django.shortcuts import render
from .models import Patient
from .forms import PatientSearchForm

def patient_list(request):
    search_query = request.GET.get('search_query', '')
    patients = Patient.objects.all()

    if search_query:
        patients = patients.filter(first_name__icontains=search_query) | patients.filter(last_name__icontains=search_query)

    form = PatientSearchForm(request.GET)

    context = {
        'patients': patients,
        'form': form,
    }
    return render(request, 'patient_list.html', context)

def home(request):  # Add this function
    return render(request, 'home.html')
