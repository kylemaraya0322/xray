from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        # exclude employee_id (auto) and created_at
        fields = [
            'first_name','middle_name','last_name',
            'email','contact_number','position','department','status','photo'
        ]
        widgets = {
            'first_name':     forms.TextInput(attrs={'class':'w-full border rounded px-2 py-1'}),
            'middle_name':    forms.TextInput(attrs={'class':'w-full border rounded px-2 py-1'}),
            'last_name':      forms.TextInput(attrs={'class':'w-full border rounded px-2 py-1'}),
            'email':          forms.EmailInput(attrs={'class':'w-full border rounded px-2 py-1'}),
            'contact_number': forms.TextInput(attrs={'class':'w-full border rounded px-2 py-1'}),
            'position':       forms.TextInput(attrs={'class':'w-full border rounded px-2 py-1'}),
            'department':     forms.TextInput(attrs={'class':'w-full border rounded px-2 py-1'}),
            'status':         forms.Select(attrs={'class':'w-full border rounded px-2 py-1'}),
            'photo':          forms.ClearableFileInput(attrs={'class':'w-full'}),
        }
