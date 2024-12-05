from django.urls import path
from django.conf import settings
from .views import DashboardsView

app_name = 'rsp'

urlpatterns = [
    path('dashboard', DashboardsView.as_view(template_name = 'pages/rsp/Dashboard.html'), name='dashboard'),
    path('onboarding-forms', DashboardsView.as_view(template_name = 'pages/rsp/OnBoardingForms.html'), name='onboarding-forms'),
    path('newly-hired-staff', DashboardsView.as_view(template_name = 'pages/rsp/NewlyHiredStaff.html'), name='newly-hired-staff'),
    path('neop', DashboardsView.as_view(template_name = 'pages/rsp/Neop.html'), name='neop'),
    path('cos-with-guidelines', DashboardsView.as_view(template_name = 'pages/rsp/CosWithGuidelines.html'), name='cos-with-guidelines'),
    path('reports-generation', DashboardsView.as_view(template_name = 'pages/rsp/ReportsGeneration.html'), name='reports-generation'),
    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]

