# xray_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required, user_passes_test

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
    return render(
        request,
        'staff_dashboard.html',
        {'active_page': 'dashboard'}  # Add the active page to context
    )