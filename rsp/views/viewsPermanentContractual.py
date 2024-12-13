
from django.shortcuts import render

def CongratulatoryLetter (request):
    return render(request, 'rsp/PemanentContractual/index.html', {})
