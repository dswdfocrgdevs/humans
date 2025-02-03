
from django.shortcuts import render
from rsp.models import NewlyHiredStaff, StaffOnboardingInfo
import os

def GetProfile(request, id):
    try:
        newly_hired_data = NewlyHiredStaff.objects.get(id=id)
        onboarding_info = StaffOnboardingInfo.objects.filter(staff_id=newly_hired_data).first()  # Assuming you want the first matching record
    except NewlyHiredStaff.DoesNotExist:
        return render(request, 'rsp/NewlyHiredStaff/not_found.html', {})
    
    IRIS_URL = os.getenv('IRIS_URL', 'default_value')
    
    # Pass both newly_hired_data and onboarding_info to the template
    return render(request, 'rsp/NewlyHiredStaff/view.html', {
        'data': newly_hired_data,
        'onboarding_info': onboarding_info,
        'IRIS_URL': IRIS_URL
    })

