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
    iris_api_token = os.getenv('IRIS_API_TOKEN')
    url = "https://caraga-iris.dswd.gov.ph/api/hired-applicants/"
    headers = {"Authorization": "Token 9c1a7ec45beaa34c3059e9c6e226142fe4606741"}
    response = requests.get(url, headers=headers)

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
    print("aaaaa")
    print(response.json())
    # Pass on the JSON data from the external API
    return JsonResponse(response.json())


    
