from django import forms

class DiagnosisForm(forms.Form):
    xray_image = forms.ImageField(
        label='Chest X-ray Image',
        widget=forms.ClearableFileInput(attrs={'class':'w-full border rounded px-2 py-1'})
    )
