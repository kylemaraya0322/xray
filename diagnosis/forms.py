from django import forms

class DiagnosisForm(forms.Form):
    xray_image = forms.ImageField(
        label='Chest X-ray Image',
        widget=forms.ClearableFileInput(attrs={'class': 'bg-gray-700 text-white rounded-lg px-4 py-2'})
    )
