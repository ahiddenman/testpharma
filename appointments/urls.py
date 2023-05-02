from django.urls import path
from . import views
from .views import book_appointment

app_name = 'appointments'

urlpatterns = [
    path('staff_management/', views.staff_management, name='staff_management'),
    path('appointment_management/', views.appointment_management, name='appointment_management'),
    path('calendar_view/', views.calendar_view, name='calendar_view'),
    path('staff_availability/', views.staff_availability, name='staff_availability'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),

    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('edit_appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('book/', views.list_staff, name='list_staff'),
    path('', views.index, name='index'),
    path('book_appointment/<int:pharmacy_id>/<int:service_id>/<int:staff_id>/', views.book_appointment, name='book_appointment'),
    path('book_appointment_success/<int:appointment_id>/', views.book_appointment_success, name='book_appointment_success'),
    path('services/<int:pharmacy_id>/', views.services_list, name='services_list'),
    path('upcoming_appointments/', views.upcoming_appointments, name='upcoming_appointments'),
    path('reschedule_appointment/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),

    path('create_staff/', views.create_staff, name='create_staff'),
    path('edit_staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('delete_staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),

    path('add_availability/<int:staff_id>/', views.add_availability, name='add_availability'),
    path('edit_availability/<int:availability_id>/', views.edit_availability, name='edit_availability'),
    path('delete_availability/<int:availability_id>/', views.delete_availability, name='delete_availability'),

    # Patient management
    path('patient/create/', views.patient_create, name='patient_create'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patient/<int:pk>/update/', views.patient_update, name='patient_update'),
    path('patient/<int:pk>/delete/', views.patient_delete, name='patient_delete'),

    # Use the PatientListView
    path('patient/list/', views.PatientListView.as_view(), name='patient_list'),
]
