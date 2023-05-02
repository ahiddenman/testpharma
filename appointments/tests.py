from django.test import TestCase
from django.urls import reverse
from .models import Appointment, Service, Staff, StaffAvailability, Pharmacy, Patient
from authentication.models import CustomUser

class ServiceModelTest(TestCase):
    def test_string_representation(self):
        service = Service(name="Test Service")
        self.assertEqual(str(service), service.name)

class IndexViewTest(TestCase):
    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('appointments:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/index.html')
