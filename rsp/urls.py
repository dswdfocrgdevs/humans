from django.urls import path
from django.conf import settings
from .views import dashboard, onboarding_forms, newly_hired_staff, neop, cos_with_guidelines, reports_generation

app_name = 'rsp'

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('onboarding-forms', onboarding_forms, name='onboarding-forms'),
    path('newly-hired-staff', newly_hired_staff, name='newly-hired-staff'),
    path('neop', neop, name='neop'),
    path('cos-with-guidelines', cos_with_guidelines, name='cos-with-guidelines'),
    path('reports-generation', reports_generation, name='reports-generation'),
    # path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]

