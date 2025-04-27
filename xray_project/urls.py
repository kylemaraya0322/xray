# xray_project/urls.py

from django.urls            import path, include, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from xray_app               import views
from django.conf            import settings
from django.conf.urls.static import static

# —————————————————————————————————————————————
# Custom login views that carry “role” through errors
# —————————————————————————————————————————————
class AdminLoginView(LoginView):
    template_name           = 'landing.html'
    authentication_form     = AuthenticationForm
    redirect_authenticated_user = True
    extra_context           = {'role': 'admin'}
    def get_success_url(self):
        return reverse('admin_dashboard')

class StaffLoginView(LoginView):
    template_name           = 'landing.html'
    authentication_form     = AuthenticationForm
    redirect_authenticated_user = True
    extra_context           = {'role': 'staff'}
    def get_success_url(self):
        return reverse('staff_dashboard')


urlpatterns = [
    # 1) Landing page (choose role)
    path('', views.landing_view, name='landing'),

    # 2) Login endpoints
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('staff-login/', StaffLoginView.as_view(), name='staff_login'),

    # 3) Dashboards (post-login)
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),

    # 4) Logout
    path('logout/', LogoutView.as_view(next_page='landing'), name='logout'),

    # 5) App URLs
    path('employees/',  include('employee.urls')),
    path('patients/',   include('patient.urls')),
    path('diagnosis/',  include('diagnosis.urls')),
    
]
# Serve user‐uploaded media in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
