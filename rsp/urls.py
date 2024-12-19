from django.urls import path
from django.conf import settings
from .views.views import dashboard, onboarding_forms, newly_hired_staff, neop, cos_with_guidelines, reports_generation, list_newly_hired_staff, employee_search_data, print_notice_of_appointed_applicants, print_onboarding_forms, \
    print_req_checklist, list_newly_hired_staff_streamline, newly_hired_staff_streamline, print_req_checklist_streamline
from rsp.transmittal.views import list_endorse_applicants, list_endorse_applicants_data
from rsp.views.viewsPermanentContractual import CongratulatoryLetter as PermanentContractualCongratulatoryLetter, NoticeNewlyHired as PermanentContractualNoticeNewlyHired, WelcomeLetter as PermanentContractualWelcomeLetter

from rsp.views.viewsCosJo import JobOffer as CosJoJobOffer, NoticeNewlyHired as CosJoNoticeNewlyHired, WelcomeLetter as CosJoWelcomeLetter, RequirementsList as CosJoRequirementsList
app_name = 'rsp'

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('onboarding-forms', onboarding_forms, name='onboarding-forms'),
    path('newly-hired-staff', newly_hired_staff, name='newly-hired-staff'),
    path('newly-hired-staff-streamline', newly_hired_staff_streamline, name='newly-hired-staff-streamline'),
    path('list-of-endorsement-title', list_endorse_applicants, name='list_endorse_applicants'),
    path('list/of/endorsed/applicants/data/<int:pk>', list_endorse_applicants_data, name='list_endorse_applicants_data'),
    path('neop', neop, name='neop'),
    path('cos-with-guidelines', cos_with_guidelines, name='cos-with-guidelines'),
    path('reports-generation', reports_generation, name='reports-generation'),
    path('list_newly_hired_staff', list_newly_hired_staff, name='list-newly-hired-staff'),
    path('list_newly_hired_staff_streamline', list_newly_hired_staff_streamline, name='list-newly-hired-staff-streamline'),
    path('print/notice-of-appointed-applicants/<int:pk>', print_notice_of_appointed_applicants, name='view_print_notice_of_appointed'),
    path('print/onboarding/form/<int:pk>/<str:ids>', print_onboarding_forms, name='view_print_notice_of_appointed'),
    path('print/requirements/checklist/form/<str:pk>', print_req_checklist, name='print_req_checklist'),
    path('print/requirements/checklist/streamline/form/<str:pk>', print_req_checklist_streamline, name='print_req_checklist_streamline'),

    #
    path('employee_search_data', employee_search_data, name='employee_search_data'),

    path('permanent-contractual/congratulatory-letter', PermanentContractualCongratulatoryLetter, name='PermanentContractualCongratulatoryLetter'),
    path('permanent-contractual/notice-newly-hired', PermanentContractualNoticeNewlyHired, name='PermanentContractualNoticeNewlyHired'),
    path('permanent-contractual/welcome-letter', PermanentContractualWelcomeLetter, name='PermanentContractualWelcomeLetter'),

    path('cos-jo/job-offer', CosJoJobOffer, name='CosJoJobOffer'),
    path('cos-jo/notice-newly-hired', CosJoNoticeNewlyHired, name='CosJoNoticeNewlyHired'),
    path('cos-jo/welcome-letter', CosJoWelcomeLetter, name='CosJoWelcomeLetter'),
    path('cos-jo/requirements-list', CosJoRequirementsList, name='CosJoRequirementsList'),

    
    # path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]

