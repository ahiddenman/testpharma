# patient_management/urls.py
from django.urls import path
from . import views

app_name = 'patient_management'

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
]
