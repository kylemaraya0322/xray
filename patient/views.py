from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Patient
from .forms import PatientForm


def patient_list(request):
    # Fetch patients and convert to list to attach forms
    patients = list(Patient.objects.order_by('last_name'))

    # Initialize create form and edit forms dict
    create_form = PatientForm()
    edit_forms = {p.id: PatientForm(instance=p) for p in patients}

    # Attach form instance to each patient for template usage
    for p in patients:
        p.form = edit_forms[p.id]

    if request.method == 'POST':
        # CREATE
        if 'create_patient' in request.POST:
            form = PatientForm(request.POST)
            if form.is_valid():
                form.save()
                # Added alert message
                messages.success(request, "Patient added successfully!")
                return redirect('patient_list')
            create_form = form

        # UPDATE
        elif 'edit_patient' in request.POST:
            pid = request.POST.get('patient_id')
            pat = get_object_or_404(Patient, pk=pid)
            form = PatientForm(request.POST, instance=pat)
            if form.is_valid():
                form.save()
                # Added alert message
                messages.info(request, "Patient updated successfully!")
                return redirect('patient_list')
            # Rebind form with validation errors
            pat.form = form

        # DELETE
        elif 'delete_patient' in request.POST:
            pid = request.POST.get('patient_id')
            pat = get_object_or_404(Patient, pk=pid)
            pat.delete()
            # Added alert message
            messages.error(request, "Patient deleted successfully!")
            return redirect('patient_list')

    return render(request, 'patient/index.html', {
        'patients': patients,
        'create_form': create_form,
        'active_page': 'patients',
    })
