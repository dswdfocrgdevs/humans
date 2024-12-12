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


# @csrf_exempt
# def list_newly_hired_staff(request):
#     url = os.getenv("IRIS_API_NEWLY_HIRED")
#     iris_token = os.getenv("IRIS_API_TOKEN")
#     headers = {"Authorization": "Token " + iris_token}

#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         api_data = response.json()
#         data = []

#         print(api_data)
#         print("testttaaa")
#         for item in api_data.get('results', []):
#             data.append({
#                 'id': item.get('id'),
#                 'app_id': item.get('app_id'),
#                 'full_name': item.get('full_name'),
#                 'position': item.get('position'),
#                 'former_incumbent': item.get('former_incumbent'),
#                 'salary': item.get('salary'),
#                 'effectivity_of_contract': item.get('effectivity_of_contract'),
#                 'end_of_contract': item.get('end_of_contract'),
#                 'emp_status': item.get('emp_status'),
#                 'nature': item.get('nature'),
#                 'area_of_assignment': item.get('area_of_assignment'),
#                 'requirements_ok': item.get('requirements_ok'),
#                 'remarks': item.get('remarks')
#             })

#         total = len(data)
#         page = int(request.GET.get('page', 1))
#         per_page = int(request.GET.get('length', 10))
#         start = (page - 1) * per_page
#         end = start + per_page
#         paginated_data = data[start:end]

#         return JsonResponse({
#             'data': paginated_data,
#             'recordsTotal': total,
#             'recordsFiltered': total,
#         })

#     except (requests.RequestException, ValueError) as e:
#         print(f"Error fetching API data: {e}")
#         return JsonResponse({
#             'data': [],
#             'recordsTotal': 0,
#             'recordsFiltered': 0,
#         }, status=200)



@csrf_exempt
def list_newly_hired_staff(request):
    url = os.getenv("IRIS_API_NEWLY_HIRED")
    iris_token = os.getenv("IRIS_API_TOKEN")
    headers = {"Authorization": "Token " + iris_token}
    try:
        all_data = []
        page = 1

        while True:
            response = requests.get(url, headers=headers, params={'page': page})
            response.raise_for_status()
            api_data = response.json()

            if 'results' not in api_data:
                raise ValueError("Invalid API response: missing 'results' key")
            all_data.extend(api_data['results'])
            if api_data.get('next') is None:
                break

            page += 1
        data = []
        for item in all_data:
            data.append({
                'id': item.get('id'),
                'app_id': item.get('app_id'),
                'full_name': item.get('full_name'),
                'position': item.get('position'),
                'former_incumbent': item.get('former_incumbent'),
                'salary': item.get('salary'),
                'effectivity_of_contract': item.get('effectivity_of_contract'),
                'end_of_contract': item.get('end_of_contract'),
                'emp_status': item.get('emp_status'),
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

        # Return the response with paginated data
        return JsonResponse({
            'data': paginated_data,
            'recordsTotal': total,
            'recordsFiltered': total,
        })

    except (requests.RequestException, ValueError) as e:
        # Log the error for debugging purposes
        print(f"Error fetching API data: {e}")
        return JsonResponse({
            'data': [],
            'recordsTotal': 0,
            'recordsFiltered': 0,
        }, status=200)


# @csrf_exempt
# def list_newly_hired_staff(request):
#     url = os.getenv("IRIS_API_NEWLY_HIRED")
#     iris_token = os.getenv("IRIS_API_TOKEN")
#     headers = {"Authorization": "Token " + iris_token}

#     try:
#         # Fetch the data from the API
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()

#         # Parse the API response JSON
#         api_data = response.json()
        
#         if 'results' not in api_data:
#             raise ValueError("Invalid API response: missing 'results' key")

#         data = []
        
#         # Populate the data list from the API response
#         for item in api_data['results']:
#             data.append({
#                 'id': item.get('id'),
#                 'app_id': item.get('app_id'),
#                 'full_name': item.get('full_name'),
#                 'position': item.get('position'),
#                 'former_incumbent': item.get('former_incumbent'),
#                 'salary': item.get('salary'),
#                 'effectivity_of_contract': item.get('effectivity_of_contract'),
#                 'end_of_contract': item.get('end_of_contract'),
#                 'emp_status': item.get('emp_status'),
#                 'nature': item.get('nature'),
#                 'area_of_assignment': item.get('area_of_assignment'),
#                 'requirements_ok': item.get('requirements_ok'),
#                 'remarks': item.get('remarks')
#             })

#         # Pagination logic
#         total = len(data)
#         print("total hereee")
#         print(total)
#         page = int(request.GET.get('page', 1))
#         per_page = int(request.GET.get('length', 50))
#         start = (page - 1) * per_page
#         end = start + per_page
#         paginated_data = data[start:end]

#         # Return the response
#         return JsonResponse({
#             'data': paginated_data,
#             'recordsTotal': total,
#             'recordsFiltered': total,
#         })

#     except (requests.RequestException, ValueError) as e:
#         # Log the error for debugging purposes
#         print(f"Error fetching API data: {e}")
#         return JsonResponse({
#             'data': [],
#             'recordsTotal': 0,
#             'recordsFiltered': 0,
#         }, status=200)

    
