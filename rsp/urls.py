from django.urls import path
from django.conf import settings
from .views.views import dashboard, onboarding_forms, newly_hired_staff, neop, cos_with_guidelines, reports_generation, list_newly_hired_staff, employee_search_data

from rsp.views.viewsPermanentContractual import CongratulatoryLetter as PermanentContractualCongratulatoryLetter

from rsp.views.viewsCosJo import CongratulatoryLetter as CosJoCongratulatoryLetter

app_name = 'rsp'

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('onboarding-forms', onboarding_forms, name='onboarding-forms'),
    path('newly-hired-staff', newly_hired_staff, name='newly-hired-staff'),
    path('neop', neop, name='neop'),
    path('cos-with-guidelines', cos_with_guidelines, name='cos-with-guidelines'),
    path('reports-generation', reports_generation, name='reports-generation'),
    path('list_newly_hired_staff', list_newly_hired_staff, name='list-newly-hired-staff'),


    #
    path('employee_search_data', employee_search_data, name='employee_search_data'),

    path('permanent-contractual/congratulatory-letter', PermanentContractualCongratulatoryLetter, name='PermanentContractualCongratulatoryLetter'),

    path('cos-jo/congratulatory-letter', CosJoCongratulatoryLetter, name='CosJoCongratulatoryLetter'),

    
    # path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]

