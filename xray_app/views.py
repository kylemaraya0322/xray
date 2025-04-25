# xray_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts             import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils                 import timezone
from django.http                  import JsonResponse
from datetime                     import timedelta

from patient.models              import Patient


def landing_view(request):
    role = request.GET.get('role')  # 'admin' or 'staff' or None
    return render(request, 'landing.html', {'role': role, 'form': AuthenticationForm()})

# only superusers can access admin dashboard
def is_admin(user):
    return user.is_authenticated and user.is_superuser

# only non-superuser staff can access staff dashboard
def is_staff_user(user):
    return user.is_authenticated and not user.is_superuser

@login_required
def home_redirect(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    return redirect('staff_dashboard')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def admin_dashboard(request):
    return render(
        request,
        'admin_dashboard.html',
        {'active_page': 'dashboard'}  # Add the active page to context
    )

@login_required
@user_passes_test(is_staff_user)
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

def staff_dashboard(request):
    """
    Renders the staff dashboard, passing in the initial pending list.
    """
    my_pending = Patient.objects.filter(diagnosis='Pending').order_by('last_name')
    return render(request, 'staff_dashboard.html', {
        'active_page': 'dashboard',
        'my_pending': my_pending,
    })
    
@login_required
@user_passes_test(is_admin)
def api_admin_stats(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    total_patients       = Patient.objects.count()
    new_patients_week    = Patient.objects.filter(created_at__date__gte=week_ago).count()
    pending_diagnoses    = Patient.objects.filter(diagnosis='Pending').count()
    completed_diagnoses  = Patient.objects.exclude(diagnosis='Pending').count()
    ptb_count            = Patient.objects.filter(diagnosis='PTB').count()
    normals_count        = Patient.objects.filter(diagnosis='Normal').count()

    # example staff-on-duty placeholder: all staff marked on duty in the last hour
    # (replace with your real logic)
    one_hour_ago = timezone.now() - timedelta(hours=1)
    staff_on_duty = User.objects.filter(
        is_staff=True,
        last_login__gte=one_hour_ago
    ).values('id','username')[:5]

    # recent activity stub: you should replace this with your real audit log
    recent_activity = [
        {'when': '5m ago', 'who': 'Dr. Cruz', 'what': 'added new patient'},
        {'when': '12m ago','who': 'Nurse Anne','what': 'completed diagnosis'},
    ]

    return JsonResponse({
        'total_patients'      : total_patients,
        'new_patients_week'   : new_patients_week,
        'pending_diagnoses'   : pending_diagnoses,
        'completed_diagnoses' : completed_diagnoses,
        'ptb_count'           : ptb_count,
        'normals_count'       : normals_count,
        'staff_on_duty'       : list(staff_on_duty),
        'recent_activity'     : recent_activity,
    })
    
@login_required
@user_passes_test(is_staff_user)
def api_staff_stats(request):
    """
    Returns JSON with the live‐updating metrics for staff:
      - pending_diagnoses
      - completed_diagnoses
      - new_patients_week
    """
    today    = timezone.now().date()
    week_ago = today - timedelta(days=7)

    # All staff see the same pool since we don't have per-user assignment
    pending_cnt   = Patient.objects.filter(diagnosis='Pending').count()
    completed_cnt = Patient.objects.exclude(diagnosis='Pending').count()
    new_week_cnt  = Patient.objects.filter(created_at__date__gte=week_ago).count()

    return JsonResponse({
        'pending_diagnoses'   : pending_cnt,
        'completed_diagnoses' : completed_cnt,
        'new_patients_week'   : new_week_cnt,
    })