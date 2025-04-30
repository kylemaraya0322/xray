from django.shortcuts       import render, redirect, get_object_or_404
from django.contrib         import messages
from django.urls            import reverse
from datetime               import datetime
from .forms                 import DiagnosisForm
from .ml                    import run_ai_model
from patient.models         import Patient
from .models                import DiagnosisRecord

def diagnosis_list(request):
    # Attach a prefixed form + history + last_record to each patient
    patients = list(Patient.objects.order_by('last_name'))
    for p in patients:
        p.form         = DiagnosisForm(prefix=str(p.id))
        p.history_list = p.history.all()
        p.last_record  = p.history_list.first()  # newest, because your model orders by -diagnosed_at

    if request.method == 'POST' and 'diagnose_patient' in request.POST:
        pid  = request.POST['patient_id']
        pat  = get_object_or_404(Patient, pk=pid)
        form = DiagnosisForm(request.POST, request.FILES, prefix=str(pid))

        if form.is_valid():
            img         = form.cleaned_data['xray_image']
            label, conf = run_ai_model(img)

            # update patient
            pat.diagnosis  = label
            pat.confidence = conf
            pat.save()

            # record history
            record = DiagnosisRecord.objects.create(
                patient      = pat,
                label        = label,
                confidence   = conf,
                xray_image   = img,
                diagnosed_at = datetime.now()
            )

            messages.success(
                request,
                f"Diagnosed {pat.first_name} {pat.last_name}: {label} ({conf*100:.1f}%)"
            )
            return redirect('diagnosis_list')

        # rebind invalid form so errors show
        pat.form = form

    return render(request, 'diagnosis/index.html', {
        'patients':    patients,
        'active_page': 'diagnosis',
    })



def report_view(request, pk):
    """
    Render a printable report for a single DiagnosisRecord,
    with more detailed, TB‐specific language for effusion and cavity.
    """
    record  = get_object_or_404(DiagnosisRecord, pk=pk)
    patient = record.patient

    # Build a detailed findings list based on label
    if record.label == 'Effusion':
        findings = ["Pleural effusion"]
        impression = "Possible Pulmonary Tuberculosis"

    elif record.label == 'Cavity':
        findings = ["Cavity"]
        impression = "Possible Pulmonary Tuberculosis"

    else:  # 'No Findings' or other
        findings = ["No findings"]
        impression = "Normal"


    context = {
        'record':     record,
        'patient':    patient,
        'findings':   findings,
        'impression': impression,
        'generated':  datetime.now(),
    }
    return render(request, 'diagnosis/report.html', context)

