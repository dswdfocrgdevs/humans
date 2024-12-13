
from django.shortcuts import render

def JobOffer (request):
    return render(request, 'rsp/CosJo/JobOffer.html', {})

def NoticeNewlyHired (request):
    return render(request, 'rsp/CosJo/NoticeNewlyHired.html', {})

def WelcomeLetter (request):
    return render(request, 'rsp/CosJo/WelcomeLetter.html', {})

def RequirementsList (request):
    return render(request, 'rsp/CosJo/RequirementsList.html', {})
