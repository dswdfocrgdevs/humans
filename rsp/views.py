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


    
