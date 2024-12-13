
from django.shortcuts import render

def CongratulatoryLetter (request):
    return render(request, 'rsp/PemanentContractual/CongratulatoryLetter.html', {})

def NoticeNewlyHired (request):
    return render(request, 'rsp/PemanentContractual/NoticeNewlyHired.html', {})

def WelcomeLetter (request):
    return render(request, 'rsp/PemanentContractual/WelcomeLetter.html', {})
