
from django.shortcuts import render
from rsp.models import NewlyHiredStaff
import os

def GetProfile(request, id):
    try:
        newly_hired_data = NewlyHiredStaff.objects.get(id=id)
    except NewlyHiredStaff.DoesNotExist:
        return render(request, 'rsp/NewlyHiredStaff/not_found.html', {})
    IRIS_URL = os.getenv('IRIS_URL', 'default_value')
    return render(request, 'rsp/NewlyHiredStaff/view.html', {'data': newly_hired_data, 'IRIS_URL':IRIS_URL})
