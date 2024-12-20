from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os

def list_endorse_applicants(request):
    try:
        base_url = os.getenv("IRIS_API_TRANSMITTAL_SUBJECT")
        iris_token = os.getenv("IRIS_API_TOKEN")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {iris_token}"
        }
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            endorsement = response.json()
            endorsement['results'].sort(
                key=lambda x: x['datetime_created'], reverse=True)
        else:
            endorsement = []
    except Exception as e:
        endorsement = []
    context = {
        'endorsement': endorsement,
        'title': 'List of Created Endorsement'
    }
    return render(request, 'rsp/Transmittal/subject.html', context)

def list_endorse_applicants_data(request, pk):
	try:
		# Fetch the endorsement data
		url = f'https://caraga-iris.dswd.gov.ph/api/app/endorsement/?pk={pk}'
		response = requests.get(
			url,
			headers={
				'Content-Type': 'application/json',
				'Authorization': 'Token 9c1a7ec45beaa34c3059e9c6e226142fe4606741'
			}
		)
		if response.status_code == 200:
			endorsement_data = response.json()
		else:
			endorsement_data = {'results': []}
	except Exception as e:
		endorsement_data = {'results': []}

	try:
		# Fetch the transmittal title data
		url_transmittal = f'https://caraga-iris.dswd.gov.ph/api/transmittal/title/details/?pk={pk}'
		transmittal_response = requests.get(
			url_transmittal,
			headers={
				'Content-Type': 'application/json',
				'Authorization': 'Token 9c1a7ec45beaa34c3059e9c6e226142fe4606741'
			}
		)
		if transmittal_response.status_code == 200:
			applicants = transmittal_response.json()
			# Fetch the first result
			applicant = applicants['results'][0] if applicants['results'] else None
		else:
			applicant = None
	except Exception as e:
		applicant = None

	# Combine endorsement data and transmittal title data into the context
	context = {
		'endorsement_data': endorsement_data['results'],
		'applicant': applicant,  # Add applicants data here
		'title': 'Endorsement Applicants',
	}
	return render(request, 'rsp/Transmittal/list_endorse_applicants_data.html', context)