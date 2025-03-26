
from django.shortcuts import render
from rsp.models import NewlyHiredStaff, StaffOnboardingInfo
from rsp.functions import check_endorsement_activities_exist
import os

def GetProfile(request, id):
    try:
        newly_hired_data = NewlyHiredStaff.objects.get(id=id)
        onboarding_info = StaffOnboardingInfo.objects.filter(staff_id=newly_hired_data).first()  # Assuming you want the first matching record
    except NewlyHiredStaff.DoesNotExist:
        return render(request, 'rsp/NewlyHiredStaff/not_found.html', {})
    
    IRIS_URL = os.getenv('IRIS_URL', 'default_value')


    newly_hired_data.endorse_welfare = check_endorsement_activities_exist(1, id)['all_activities_exist'];
    newly_hired_data.endorse_welfareprogress = check_endorsement_activities_exist(1, id)['progress'];
    newly_hired_data.endorse_lds = check_endorsement_activities_exist(2, id)['all_activities_exist'];
    newly_hired_data.endorse_ldsprogress = check_endorsement_activities_exist(2, id)['progress'];
    newly_hired_data.endorse_pms = check_endorsement_activities_exist(3, id)['all_activities_exist'];
    newly_hired_data.endorse_pmsprogress = check_endorsement_activities_exist(3, id)['progress'];
    newly_hired_data.endorse_pas = check_endorsement_activities_exist(4, id)['all_activities_exist'];
    newly_hired_data.endorse_pasprogress = check_endorsement_activities_exist(4, id)['progress'];
    
    # Pass both newly_hired_data and onboarding_info to the template
    return render(request, 'rsp/NewlyHiredStaff/view.html', {
        'data': newly_hired_data,
        'onboarding_info': onboarding_info,
        'IRIS_URL': IRIS_URL
    })

