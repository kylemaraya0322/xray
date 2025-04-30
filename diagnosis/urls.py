from django.urls import path
from . import views

urlpatterns = [
    path('', views.diagnosis_list, name='diagnosis_list'),
    path('report/<int:pk>/', views.report_view, name='diagnosis_report'),

]
 