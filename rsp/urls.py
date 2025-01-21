from django.urls import path
from django.conf import settings
from .views.views import dashboard, onboarding_forms, newly_hired_staff, neop, cos_with_guidelines, reports_generation, list_newly_hired_staff, employee_search_data, print_notice_of_appointed_applicants, print_onboarding_forms, \
    print_req_checklist, list_newly_hired_staff_streamline, newly_hired_staff_streamline, print_req_checklist_streamline,PatchNewlyHiredOnboarding, GetLibEndorsedActivities, PostLibEndorsedActivities, view_hired_requirements, \
    hiredreq_not_complete, hiredreq_complete, delete_hiredreq_compliance, lib_neop, lib_cos_guidelines_activities
from rsp.transmittal.views import list_endorse_applicants, list_endorse_applicants_data

from rsp.views.rsp.viewsPermanentContractual import CongratulatoryLetter as PermanentContractualCongratulatoryLetter, NoticeNewlyHired as PermanentContractualNoticeNewlyHired, WelcomeLetter as PermanentContractualWelcomeLetter
from rsp.views.rsp.viewsCosJo import JobOffer as CosJoJobOffer, NoticeNewlyHired as CosJoNoticeNewlyHired, WelcomeLetter as CosJoWelcomeLetter, RequirementsList as CosJoRequirementsList
from rsp.views.rsp.viewsNeop import Neop, GetLibNeopActivities, PostLibNeopActivities, ListNewlyHiredNeop, PostNeopStaffInfo

from rsp.views.rsp.viewsLibraries import LibrariesNeop, LibrariesCosWithGuidelines, LibrariesAddNeop, LibrariesUpdateNeop
from rsp.views.rsp.viewsCosGuidelines import GetCosGuideLines, GetCosGuideLinesStaffList, GetLibCosGuideLinesActivities, PostLibCostGuideLinesActivities, PostCosGuideLinesStaffInfo

from rsp.views.rsp.viewsInternalStaff import GetInternalStaff, ListNewlyHiredInternalStaff

app_name = 'rsp'

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('onboarding-forms', onboarding_forms, name='onboarding-forms'),
    path('newly-hired-staff', newly_hired_staff, name='newly-hired-staff'),
    path('newly-hired-staff-streamline', newly_hired_staff_streamline, name='newly-hired-staff-streamline'),
    path('list-of-endorsement-title', list_endorse_applicants, name='list_endorse_applicants'),
    path('list/of/endorsed/applicants/data/<int:pk>', list_endorse_applicants_data, name='list_endorse_applicants_data'),
    path('cos-with-guidelines', cos_with_guidelines, name='cos-with-guidelines'),
    path('reports-generation', reports_generation, name='reports-generation'),
    path('list_newly_hired_staff', list_newly_hired_staff, name='list-newly-hired-staff'),
    path('list_newly_hired_staff_streamline', list_newly_hired_staff_streamline, name='list-newly-hired-staff-streamline'),
    path('print/notice-of-appointed-applicants/<int:pk>', print_notice_of_appointed_applicants, name='view_print_notice_of_appointed'),
    path('print/onboarding/form/<int:pk>/<str:ids>', print_onboarding_forms, name='view_print_notice_of_appointed'),
    path('print/requirements/checklist/form/<str:pk>', print_req_checklist, name='print_req_checklist'),
    path('print/requirements/checklist/streamline/form/<str:pk>', print_req_checklist_streamline, name='print_req_checklist_streamline'),
    path('endorse/lib/activities', GetLibEndorsedActivities, name="GetLibEndorsedActivities"),
    path('endorse/staff/activities/save', PostLibEndorsedActivities, name="PostLibEndorsedActivities"),
    path('view_hired_requirements/<int:pk>', view_hired_requirements, name='view_hired_requirements'),
    path('hiredreq_not_complete/', hiredreq_not_complete, name='hiredreq_not_complete'),
    path('hiredreq_complete/', hiredreq_complete, name='hiredreq_complete'),
    path('delete_hiredreq_compliance/', delete_hiredreq_compliance, name='delete_hiredreq_compliance'),

    #libraries
    path('lib_neop', lib_neop, name='lib-neop'),
    path('lib_cos_guidelines_activities', lib_cos_guidelines_activities, name='lib-cos-guidelines-activities'),

    path('employee_search_data', employee_search_data, name='employee_search_data'),

    path('permanent-contractual/congratulatory-letter', PermanentContractualCongratulatoryLetter, name='PermanentContractualCongratulatoryLetter'),
    path('permanent-contractual/notice-newly-hired', PermanentContractualNoticeNewlyHired, name='PermanentContractualNoticeNewlyHired'),
    path('permanent-contractual/welcome-letter', PermanentContractualWelcomeLetter, name='PermanentContractualWelcomeLetter'),

    path('cos-jo/job-offer', CosJoJobOffer, name='CosJoJobOffer'),
    path('cos-jo/notice-newly-hired', CosJoNoticeNewlyHired, name='CosJoNoticeNewlyHired'),
    path('cos-jo/welcome-letter', CosJoWelcomeLetter, name='CosJoWelcomeLetter'),
    path('cos-jo/requirements-list', CosJoRequirementsList, name='CosJoRequirementsList'),

    path('neop',Neop,name="Neop"),
    path('neop/lib/activities', GetLibNeopActivities, name="GetLibNeopActivities"),
    path('neop/staff/activities/save', PostLibNeopActivities, name="PostLibNeopActivities"),
    path('neop/staff/list', ListNewlyHiredNeop, name="ListNewlyHiredNeop"),
    path('neop/staff/save', PostNeopStaffInfo, name="PostNeopStaffInfo"),

    path('neop/staff/libraries/neop', LibrariesNeop, name="LibrariesNeop"),
    path('neop/staff/libraries/cos', LibrariesCosWithGuidelines, name="LibrariesCosWithGuidelines"),
    path('neop/staff/libraries/save', LibrariesAddNeop, name="LibrariesAddNeop"),
    path('neop/staff/libraries/update', LibrariesUpdateNeop, name="LibrariesUpdateNeop"),
    # path('neop/staff/libraries', LibrariesAddCosWithGuidelines, name="LibrariesAddCosWithGuidelines"),
    # path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),

    path('cos-guidelines', GetCosGuideLines, name="GetCosGuideLines"),
    path('cos-guidelines/lib/activities', GetLibCosGuideLinesActivities, name="GetLibCosGuideLinesActivities"),
    path('cos-guidelines/staff/activities/save', PostLibCostGuideLinesActivities, name="PostLibCostGuideLinesActivities"),
    path('cos-guidelines/staff/list', GetCosGuideLinesStaffList, name="GetCosGuideLinesStaffList"),
    path('cos-guidelines/staff/save', PostCosGuideLinesStaffInfo, name="PostCosGuideLinesStaffInfo"),

    path('list-of-newly-hired/oboarding-type/update', PatchNewlyHiredOnboarding, name="PatchNewlyHiredOnboarding"),

    path('internal-staff', GetInternalStaff, name="GetInternalStaff"),
    path('internal-staff/staff/list', ListNewlyHiredInternalStaff, name="ListNewlyHiredInternalStaff"),
    
    

]

