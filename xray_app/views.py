import logging
from datetime      import date, timedelta
from django.db.models import Count

from django.shortcuts               import render, redirect
from django.urls                    import reverse
from django.contrib.auth.forms      import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views      import LoginView

from employee.models    import Employee
from patient.models     import Patient
from diagnosis.models   import DiagnosisRecord

logger = logging.getLogger(__name__)


# ─── Role‐check helpers ────────────────────────────────────────────────────────

def is_admin(user):
    return user.is_authenticated and user.is_superuser

def is_staff_user(user):
    # allow true staff or superusers into the staff dashboard
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# ─── Landing & role‐specific LoginViews ───────────────────────────────────────

def landing_view(request):
    """
    /?role=admin or ?role=staff shows the appropriate login form.
    No role → show selector.
    """
    role = request.GET.get('role')  # None, 'admin', or 'staff'
    return render(request, 'landing.html', {
        'role': role,
        'form': AuthenticationForm(),
    })


class AdminLoginView(LoginView):
    template_name               = 'landing.html'
    authentication_form         = AuthenticationForm
    redirect_authenticated_user = False
    extra_context               = {'role': 'admin'}

    def form_valid(self, form):
        user = form.get_user()
        if not (user.is_active and user.is_superuser):
            form.add_error(None, "You must be an active superuser to log in here.")
            return self.form_invalid(form)
        logger.info(f"Admin user '{user.username}' logged in")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin_dashboard')


class StaffLoginView(LoginView):
    template_name               = 'landing.html'
    authentication_form         = AuthenticationForm
    redirect_authenticated_user = False
    extra_context               = {'role': 'staff'}

    def form_valid(self, form):
        user = form.get_user()
        if not (user.is_active and (user.is_staff or user.is_superuser)):
            form.add_error(None, "You must be an active staff user to log in here.")
            return self.form_invalid(form)
        logger.info(f"Staff user '{user.username}' logged in")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('staff_dashboard')


# ─── Post‐login redirect ───────────────────────────────────────────────────────

@login_required(login_url='landing')
def home_redirect(request):
    # superuser → admin, else → staff
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    return redirect('staff_dashboard')


# ─── Utility for 7-day trends ─────────────────────────────────────────────────

def _get_last_n_days_counts(model, date_field, n=7):
    today = date.today()
    labels = []
    data   = []
    for i in range(n-1, -1, -1):
        d = today - timedelta(days=i)
        labels.append(d.strftime("%b %d"))
        data.append(model.objects.filter(**{f"{date_field}__date": d}).count())
    return labels, data


# ─── Admin Dashboard ──────────────────────────────────────────────────────────

@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_dashboard(request):
    # Summary cards
    summary_cards = [
        {
          'title': 'Employees',
          'count': Employee.objects.count(),
          'color': 'green',
          'url':   'employee_list'
        },
        {
          'title': 'Patients',
          'count': Patient.objects.count(),
          'color': 'yellow',
          'url':   'patient_list'
        },
        {
          'title': 'Pending Diagnoses',
          'count': Patient.objects.filter(diagnosis='Pending').count(),
          'color': 'red',
          'url':   'diagnosis_list'
        },
        {
          'title': 'Completed Diagnoses',
          'count': DiagnosisRecord.objects.count(),
          'color': 'teal',
          'url':   'diagnosis_list'
        },
    ]

    # 7-day trend
    diag_labels, diag_data = _get_last_n_days_counts(
        DiagnosisRecord, 'diagnosed_at', n=7
    )

    # Diagnosis distribution
    diag_dist_qs = Patient.objects.values('diagnosis').annotate(count=Count('diagnosis'))
    diag_dist_labels = [r['diagnosis'] for r in diag_dist_qs]
    diag_dist_data   = [r['count']     for r in diag_dist_qs]

    # ─── Employee status distribution (fixed labels) ────────────────────────────
    EMPLOYEE_STATUSES = ['On Duty','On Leave','Absent']

    emp_status_labels = EMPLOYEE_STATUSES
    emp_status_data   = [
        Employee.objects.filter(status=stat).count()
        for stat in EMPLOYEE_STATUSES
    ]

    # Recent activity
    recent_emps  = Employee.objects.order_by('-id')[:5]
    recent_pats  = Patient.objects.order_by('-id')[:5]
    recent_diags = DiagnosisRecord.objects.order_by('-diagnosed_at')[:5]

    return render(request, 'admin_dashboard.html', {
        'active_page'        : 'dashboard',
        'summary_cards'      : summary_cards,
        'diag_labels'        : diag_labels,
        'diag_data'          : diag_data,
        'diag_dist_labels'   : diag_dist_labels,
        'diag_dist_data'     : diag_dist_data,
        'emp_status_labels'  : emp_status_labels,
        'emp_status_data'    : emp_status_data,
        'recent_emps'        : recent_emps,
        'recent_pats'        : recent_pats,
        'recent_diags'       : recent_diags,
    })

# ─── Staff Dashboard ──────────────────────────────────────────────────────────

@login_required(login_url='staff_login')
@user_passes_test(is_staff_user, login_url='staff_login')
def staff_dashboard(request):
    summary_cards = [
        {
          'title': 'Total Patients',
          'count': Patient.objects.count(),
          'color': 'yellow',
          'url':   'patient_list'
        },
        {
          'title': 'Pending Diagnoses',
          'count': Patient.objects.filter(diagnosis='Pending').count(),
          'color': 'red',
          'url':   'diagnosis_list'
        },
        {
          'title': 'My Diagnoses',
          'count': DiagnosisRecord.objects.count(),
          'color': 'teal',
          'url':   'diagnosis_list'
        },
    ]

    # 7-day trend
    diag_labels, diag_data = _get_last_n_days_counts(
        DiagnosisRecord, 'diagnosed_at', n=7
    )

    # Recent activity
    recent_pats  = Patient.objects.order_by('-id')[:5]
    recent_diags = DiagnosisRecord.objects.order_by('-diagnosed_at')[:5]

    return render(request, 'staff_dashboard.html', {
        'active_page'   : 'dashboard',
        'summary_cards' : summary_cards,
        'diag_labels'   : diag_labels,
        'diag_data'     : diag_data,
        'recent_pats'   : recent_pats,
        'recent_diags'  : recent_diags,
    })
