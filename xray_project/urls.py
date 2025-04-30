from django.urls               import path, include
from django.contrib.auth.views import LogoutView
from django.conf               import settings
from django.conf.urls.static   import static

from xray_app.views import (
    landing_view,
    AdminLoginView,
    StaffLoginView,
    admin_dashboard,
    staff_dashboard,
    home_redirect,
)

urlpatterns = [
    # 1) Landing & role selector
    path('',             landing_view,    name='landing'),

    # 2) Per-role login endpoints
    path('login/admin/', AdminLoginView.as_view(), name='admin_login'),
    path('login/staff/', StaffLoginView.as_view(), name='staff_login'),

    # 3) After login send everyone here → home_redirect will forward to the right dashboard
    path('dashboard/',   home_redirect,   name='dashboard'),

    # 4) The actual protected dashboards
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),

    # 5) Standard logout
    path('logout/', LogoutView.as_view(next_page='landing'), name='logout'),

    # 6) Your other apps
    path('employees/', include('employee.urls')),
    path('patients/',  include('patient.urls')),
    path("diagnosis/",         include("diagnosis.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
