# patient_management/forms.py
from django import forms

class PatientSearchForm(forms.Form):
    search_query = forms.CharField(label='', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search patients...'}))
