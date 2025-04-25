from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from xray_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1) Root shows the landing page
    path('', views.landing_view, name='landing'),

    # 2) Login endpoints
    path('admin-login/', auth_views.LoginView.as_view(
        template_name='landing.html',
        authentication_form=AuthenticationForm,
        redirect_authenticated_user=False
    ), name='admin_login'),
    path('staff-login/', auth_views.LoginView.as_view(
        template_name='landing.html',
        authentication_form=AuthenticationForm,
        redirect_authenticated_user=False
    ), name='staff_login'),

    # 3) Dashboards (only reachable after login)
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    path(
      'logout/',
      auth_views.LogoutView.as_view(next_page='landing'),
      name='logout'
    ),
    path('employees/', include('employee.urls')),
    path('patients/', include('patient.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)