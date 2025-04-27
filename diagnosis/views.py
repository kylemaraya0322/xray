from django.shortcuts       import render, redirect, get_object_or_404
from django.contrib         import messages
from patient.models         import Patient
from .forms                 import DiagnosisForm
from .ml                    import run_ai_model
from .models                import DiagnosisRecord

def diagnosis_list(request):
    # 1) Load all patients and attach an empty form to each
    patients = list(Patient.objects.order_by('last_name'))
    forms    = {p.id: DiagnosisForm(prefix=str(p.id)) for p in patients}
    for p in patients:
        p.form = forms[p.id]
        # preload history
        p.history_list = p.history.all()  # requires related_name='history'

    # 2) Handle new diagnosis submissions
    if request.method == 'POST' and 'diagnose_patient' in request.POST:
        pid  = request.POST.get('patient_id')
        pat  = get_object_or_404(Patient, pk=pid)
        form = DiagnosisForm(request.POST, request.FILES, prefix=str(pid))

        if form.is_valid():
            img         = form.cleaned_data['xray_image']
            label, conf = run_ai_model(img)

            # Update Patient
            pat.diagnosis  = label
            pat.confidence = conf
            pat.save()

            # Record in history (saving the exact uploaded image)
            record = DiagnosisRecord(
                patient    = pat,
                label      = label,
                confidence = conf,
                xray_image = img
            )
            record.save()

            messages.success(
                request,
                f"Diagnosed {pat.first_name} {pat.last_name}: {label} ({conf*100:.1f}%)"
            )
            return redirect('diagnosis_list')

        # if invalid, rebind form and re-render
        forms[pat.id] = form
        pat.form      = form

    return render(request, 'diagnosis/index.html', {
        'patients'   : patients,
        'active_page': 'diagnosis',
    })
