from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from kt_auth.models import CustomUser
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
import requests
import os
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model() 

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class AuthSigninView(TemplateView):
    template_name = 'auth/signin.html'

    def dispatch(self, request, *args, **kwargs):

        # Check if the session is active (e.g., 'user_id' exists in session)
        if request.user.is_authenticated:
            return redirect('/pillars')  # Redirect to home/dashboard if already signed in

        # Proceed with the normal dispatch method if no session is found
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/sign-in/general.js')

        # Define the layout for this module
        # _templates/layout/auth.html
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context


class TemporarySigninView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"detail": "Method 'GET' not allowed."}, status=405)

    def post(self, request, *args, **kwargs):
        validated_response = validate_signin(request)

        if validated_response.get("status_code") == 200:
            authenticate(request)
            user_data = signin_service(request, validated_response)
            return JsonResponse({"data": "Success", "user": user_data}, status=200)
        else:
            return JsonResponse({
                "msg": validated_response.get("message", "Invalid username and password.")
            }, status=validated_response.get("status_code", 400))



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, write_only=True)

def validate_signin(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            portal_api_login = f"{os.getenv('PORTAL_API_URL')}/api/rest-auth/login/"
            portal_api_employee_details = f"{os.getenv('PORTAL_API_URL')}/api/employee/list/search/?q="

            # Login API Request
            response = requests.post(portal_api_login, data={
                'username': username,
                'password': password
            })

            if response.status_code == 200:
                api_key = response.json().get('key')

                # Fetch Employee Details
                employee_response = requests.get(f"{portal_api_employee_details}{username}", headers={
                    'Authorization': f"Token {api_key}"
                })

                if employee_response.status_code == 200:
                    return {
                        'status_code': 200,
                        'status': 'success',
                        'data': {
                            'key': api_key,
                            'username': username,
                            'employee_details': employee_response.json()
                        }
                    }
                return {
                    'status_code': 404,
                    'status': 'error',
                    'message': 'Employee details not found.'
                }

            return {
                'status_code': response.status_code,
                'status': 'error',
                'message': 'Invalid username or password.'
            }

        except requests.exceptions.RequestException as e:
            return {
                'status_code': 500,
                'status': 'error',
                'message': f'Error connecting to API: {e}'
            }

    return {
        'status_code': 400,
        'status': 'error',
        'message': serializer.errors
    }

def signin_service(request, params):
    data = params['data']
    api_key = data['key']
    username = data['username']
    portal_api_employee_details = f"{os.getenv('PORTAL_API_URL')}/api/employee/list/search/?q="

    try:
        user = User.objects.get(username=username)
        user.last_login = timezone.now()
        user.save()
    except User.DoesNotExist:
        employee_response = requests.get(f"{portal_api_employee_details}{username}", headers={
            'Authorization': f"Token {api_key}"
        })
        
        if employee_response.status_code == 200:
            employee_details = employee_response.json()[0]

            user = CustomUser.objects.create(
                employee_id=employee_details['employee_id'],
                id_number=employee_details['id_number'],
                last_login=timezone.now(),
                username=employee_details['username'],
                first_name=employee_details['first_name'],
                middle_name=employee_details['middle_name'],
                last_name=employee_details['last_name'],
                contact=employee_details['contact'],
                account_number=employee_details['account_number'],
                position=employee_details['position'],
                division=employee_details['division'],
                section=employee_details['section'],
                area_of_assignment=employee_details['area_of_assignment'],
                gender=employee_details['gender'],
                birthdate=employee_details['birthdate'],
                image_path=employee_details['image_path'],
                status=employee_details['status'],
            )
        else:
            return {
                "status_code": 404,
                "message": "Unable to fetch employee details."
            }

    # Authenticate and manage session
    auth_login(request, user)
    request.session['user_id'] = user.id
    request.session['user_first_name'] = user.first_name
    request.session['user_middle_name'] = user.middle_name
    request.session['user_last_name'] = user.last_name
    request.session['user_position'] = user.position
    request.session['user_image'] = user.image_path

    return {
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'image_path': user.image_path,
        'position': user.position,
        'division': user.division,
        'section': user.section,
    }

def signout(request):
    request.session.flush()

    auth_logout(request)
    return HttpResponseRedirect('/signin')