from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings
from django.urls import resolve
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from pprint import pprint
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from rsp.models import NewlyHiredStaff
from ..utils import search_employees

def dashboard(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'rsp/Dashboard.html', context)

def onboarding_forms(request):
    context = {
        'title': 'Onboarding Forms'
    }
    return render(request, 'rsp/OnBoardingForms.html', context)

def newly_hired_staff(request):
    context = {
        'title': 'Newly Hired Staff'
    }
    return render(request, 'rsp/NewlyHiredStaff/index.html', context)

def neop(request):

    context = {
        'title': 'NEOP'
    }
    return render(request, 'rsp/Neop.html', context)

def cos_with_guidelines(request):
    context = {
        'title': 'COS with Guidelines'
    }
    return render(request, 'rsp/CosWithGuidelines.html', context)

def reports_generation(request):
    context = {
        'title': 'Reports Generation'
    }
    return render(request, 'rsp/ReportsGeneration.html', context)


@csrf_exempt
def list_newly_hired_staff(request):
    try:
        # Get query params for pagination and search
        page = int(request.GET.get('page', 1))  # Default page is 1
        per_page = int(request.GET.get('length', 10))  # Default length is 10
        search_value = request.GET.get('search[value]', '').strip()  # Get search query

        # Fetch data and apply search filter if search term exists
        newly_hired_data = NewlyHiredStaff.objects.all()

        if search_value:
            newly_hired_data = newly_hired_data.filter(
                full_name__icontains=search_value
            )

        # Total records (before pagination)
        total = newly_hired_data.count()

        # Paginate data
        start = (page - 1) * per_page
        paginated_data = newly_hired_data[start:start + per_page]

        # Prepare data for response
        data = [{
            'id': item.id,
            'app_id': item.id,
            'full_name': item.full_name,
            'position': item.position,
            'former_incumbent': item.former_incumbent,
            'salary': item.salary,
            'effectivity_of_contract': item.effectivity_of_contract,
            'end_of_contract': item.end_of_contract,
            'emp_status': item.emp_status,
            'nature': item.nature,
            'area_of_assignment': item.area_of_assignment,
            'requirements_ok': item.requirements_ok,
            'remarks': item.remarks,
        } for item in paginated_data]

        return JsonResponse({
            'data': data,
            'recordsTotal': total,  # Total records without filtering
            'recordsFiltered': total,  # Total filtered records after search
        })

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({
            'data': [],
            'recordsTotal': 0,
            'recordsFiltered': 0,
        }, status=200)


def employee_search_data(request):
    query = request.GET.get('query', '')
    
    # Use the utility function to get the employee data
    employee_data = search_employees(query)
    
    # Return the data as a JSON response
    return JsonResponse({'results': employee_data})