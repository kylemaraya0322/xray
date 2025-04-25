# diagnosis/views.py

from django.shortcuts      import render, redirect, get_object_or_404
from .forms                import DiagnosisForm
from patient.models        import Patient
from .ml                   import run_ai_model

def diagnosis_list(request):
    # 1) Load patients and attach a unique prefix form for each
    patients = list(Patient.objects.order_by('last_name'))
    forms    = {p.id: DiagnosisForm(prefix=str(p.id)) for p in patients}
    for p in patients:
        p.form = forms[p.id]

    # 2) Handle form submission
    if request.method == 'POST' and 'diagnose_patient' in request.POST:
        pid  = request.POST.get('patient_id')
        pat  = get_object_or_404(Patient, pk=pid)
        form = DiagnosisForm(request.POST, request.FILES, prefix=str(pid))

        if form.is_valid():
            img = form.cleaned_data['xray_image']
            # 3) Run your AI model
            result = run_ai_model(img)
            # 4) Update the Django Patient record
            pat.diagnosis = result
            pat.save()
            return redirect('diagnosis_list')

        # If invalid, re-bind form with errors
        forms[pat.id] = form
        pat.form      = form

    # 5) Render template, include active_page for nav highlighting
    return render(request, 'diagnosis/index.html', {
        'patients'   : patients,
        'active_page': 'diagnosis',
    })
