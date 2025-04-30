from django import forms
from .models import Patient
from django.utils import timezone

class PatientForm(forms.ModelForm):
    # Display-only fields for auto-generated data
    patient_id = forms.CharField(
        label='Patient ID',
        disabled=True,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full border rounded px-2 py-1 bg-gray-100'
        })
    )
    age = forms.IntegerField(
        label='Age',
        disabled=True,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full border rounded px-2 py-1 bg-gray-100'
        })
    )

    class Meta:
        model = Patient
        fields = [
            'first_name', 'middle_name', 'last_name',
            'gender', 'birthdate', 'contact_number', 'diagnosis'
        ]
        widgets = {
            'first_name':     forms.TextInput(attrs={'class':'w-full border rounded px-2 py-1'}),
            'middle_name':    forms.TextInput(attrs={'class':'w-full border rounded px-2 py-1'}),
            'last_name':      forms.TextInput(attrs={'class':'w-full border rounded px-2 py-1'}),
            'gender':         forms.Select(attrs={'class':'w-full border rounded px-2 py-1'}),
            'birthdate':      forms.DateInput(attrs={'type':'date','max': timezone.localdate().isoformat(), 'class':'w-full border rounded px-2 py-1'}),
            'contact_number': forms.TextInput(attrs={'class':'w-full border rounded px-2 py-1'}),
            'diagnosis':      forms.Select(attrs={'class':'w-full border rounded px-2 py-1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize read-only fields
        if self.instance and self.instance.pk:
            self.fields['patient_id'].initial = self.instance.patient_id
            self.fields['age'].initial = self.instance.age

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        today = timezone.localdate()
        if dob and dob > today:
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return dob