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
from rsp.models import NewlyHiredStaff, RspOnboardingLayout, NewlyHiredStaffStreamline
from ..utils import search_employees
from django.db.models import Count, Case, When, Value, CharField
from django.db.models import Q
from django.template import Context, Template
import json

def dashboard(request):
    count_hired_emp_status = NewlyHiredStaff.objects.values('emp_status').annotate(count=Count('id')).order_by('-count')
    count_hired_nature = (
        NewlyHiredStaff.objects.annotate(
            grouped_nature=Case(
                When(nature__isnull=True, then=Value('N/A')),
                When(nature='N/A', then=Value('N/A')),
                default='nature',
                output_field=CharField()
            )
        )
        .values('grouped_nature')
        .annotate(count=Count('id'))
        .order_by('grouped_nature')
        .order_by('-count')
    )

    context = {
        'title': 'Dashboard',
        'count_hired_emp_status': count_hired_emp_status,
        'count_hired_nature' : count_hired_nature
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

def newly_hired_staff_streamline(request):
    context = {
        'title': 'Newly Hired Staff Streamline'
    }
    return render(request, 'rsp/NewlyHiredStaff/index-streamline.html', context)

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
            'onboarding_type': (
                'NEOP' if item.onboarding_type == 'neop' else
                'COS with guidelines' if item.onboarding_type == 'cos_with_guidelines' else
                'Internal Staff' if item.onboarding_type == 'internal_staff' else
                item.onboarding_type
            )
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
    

@csrf_exempt
def list_newly_hired_staff_streamline(request):
    try:
        # Get query params for pagination and search
        page = int(request.GET.get('page', 1))  # Default page is 1
        per_page = int(request.GET.get('length', 10))  # Default length is 10
        search_value = request.GET.get('search[value]', '').strip()  # Get search query

        # Fetch data and apply search filter if search term exists
        newly_hired_data = NewlyHiredStaffStreamline.objects.all()

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


def print_notice_of_appointed_applicants(request, pk):
    app = NewlyHiredStaff.objects.filter(Q(id=pk)).first()
    context = {
        'applicants': app,
    }
    return render(request, 'rsp/NewlyHiredStaff/print_notice_of_appointed.html', context)

def print_onboarding_forms(request, pk, ids=None):
    id_list = ids.split(',')
    app = NewlyHiredStaff.objects.filter(Q(id__in=id_list))
    context = {
        'app': app,
        'pk': pk
    }
    return render(request, 'rsp/NewlyHiredStaff/print_onboarding_forms.html', context)


@csrf_exempt
def print_req_checklist(request, pk=None):
    if pk != '0':
        ids = pk.split(',')
        all = NewlyHiredStaff.objects.filter(Q(id__in=ids))
        context = {
            'pk': pk,
            'all': all,
        }
    return render(request, 'rsp/NewlyHiredStaff/print_requirements_checklist.html', context)


@csrf_exempt
def print_req_checklist_streamline(request, pk=None):
    if pk != '0':
        ids = pk.split(',')
        all = NewlyHiredStaffStreamline.objects.filter(Q(id__in=ids))
        context = {
            'pk': pk,
            'all': all,
        }
    return render(request, 'rsp/NewlyHiredStaff/print_requirements_checklist_streamline.html', context)

@csrf_exempt
def PatchNewlyHiredOnboarding(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body)

        # Extract the relevant data from the payload
        staff_ids = data.get("data", {}).get("staffIds", [])
        onboarding_type = data.get("data", {}).get("type", None)

        # Validate that required data is present
        if not staff_ids or onboarding_type is None:
            return JsonResponse({"error": "Missing required fields: staffIds or type"}, status=400)

        # Iterate over the staff IDs and update their onboarding_type
        updated_count = 0
        not_found_ids = []
        for staff_id in staff_ids:
            staff_neop_info = NewlyHiredStaff.objects.filter(id=staff_id).first()
            if staff_neop_info:
                staff_neop_info.onboarding_type = onboarding_type
                staff_neop_info.save()
                updated_count += 1
            else:
                not_found_ids.append(staff_id)

        # Build the response message
        response_message = {
            "updated_count": updated_count,
            "not_found_ids": not_found_ids,
        }

        return JsonResponse(response_message, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)