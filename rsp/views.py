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

# def newly_hired_staff(request):
#     iris_url = os.getenv('IRIS_URL')
#     iris_api_token = os.getenv('IRIS_API_TOKEN')
#     url = iris_url+"/api/hired-applicants/"
#     headers = {"Authorization": "Token " + iris_api_token}
#     response = requests.get(url, headers=headers)

#     print("NEWWTESTAAAA")
#     print(response.json())

#     context = {
#         'title': 'Newly Hired Staff'
#     }
#     return render(request, 'rsp/NewlyHiredStaff.html', context)

def newly_hired_staff(request):
    context = {
        'title': 'Newly Hired Staff'
    }
    return render(request, 'rsp/NewlyHiredStaff.html', context)

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
    url = "https://caraga-iris.dswd.gov.ph/api/hired-applicants/"
    headers = {"Authorization": "Token 9c1a7ec45beaa34c3059e9c6e226142fe4606741"}
    response = requests.get(url, headers=headers)

    # Parse JSON response
    if response.status_code == 200:
        api_data = response.json()  # Ensure the response is parsed as JSON
        data = []
        
        print("newdataa")
        # Process each item in the response
        for item in api_data.get('results', []):
            data.append({
                'id': item.get('id'),
                'app_id': item.get('app_id'),
                'full_name': item.get('full_name'),
                'position': item.get('position'),
                'former_incumbent': item.get('former_incumbent'),
                'salary': item.get('salary'),
                'effectivity_of_contract': item.get('effectivity_of_contract'),
                'end_of_contract': item.get('end_of_contract'),
                'emp_status_id': item.get('emp_status_id'),
                'nature': item.get('nature'),
                'area_of_assignment': item.get('area_of_assignment'),
                'requirements_ok': item.get('requirements_ok'),
                'remarks': item.get('remarks')
            })
        total = len(data)
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('length', 10))
        start = (page - 1) * per_page
        end = start + per_page
        paginated_data = data[start:end]


        return JsonResponse({
            'data': paginated_data,
            'recordsTotal': total,
            'recordsFiltered': total,
        })

    return JsonResponse({'error': 'Failed to fetch data from the API'}, status=500)

# @csrf_exempt
# def list_newly_hired_staff(request):
#     data = []
#     url = "https://caraga-iris.dswd.gov.ph/api/hired-applicants/"
#     headers = {"Authorization": "Token 9c1a7ec45beaa34c3059e9c6e226142fe4606741"}
#     response = requests.get(url, headers=headers)

#     # Pass on the JSON data from the external API
#     for item in response:
#         item = {
#             'app_id': item.app_id,
#             'emp_status_id': item.emp_status_id,
#             'full_name': item.full_name,
#             'position': item.position,
#             'former_incumbent': item.staformer_incumbenttus,
#             'salary': item.status,
#             'effectivity_of_contract': item.effectivity_of_contract,
#             'end_of_contract': item.end_of_contract,
#             'status_of_employment': item.status_of_employment,
#             'nature': item.nature,
#             'area_of_assignment': item.area_of_assignment,
#             'requirements_ok': item.requirements_ok,
#             'remarks': item.remarks,
#         }

#     data.append(item)

#     response = {
#         'data': data,
#         'page': page,
#         'per_page': per_page,
#         'recordsTotal': total,
#         'recordsFiltered': total,
#     }

#     return JsonResponse(response)


    
