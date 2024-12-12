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
        return JsonResponse({"detail": "Method \"GET\" not allowed."})

    def post(self, request, *args, **kwargs):
        validated_response = validate_signin(request)
        if validated_response['status_code'] == 200 :
            authenticate(request)
            results = signin_service(request, validated_response)
            return JsonResponse({'data': 'Success'})
        else:
            return render(request, 'pages/auth/signin.html')
            return JsonResponse({'msg': 'Invalid username and password.'})


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, write_only=True)

def validate_signin(request):
        # Initialize the serializer with the request data
        serializer = LoginSerializer(data=request.data)

        # Validate the data
        if serializer.is_valid():
            # Extract the validated data
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                # Get the external API URLs from environment variables
                portal_api_login = f"{os.getenv('PORTAL_API_URL')}/api/rest-auth/login/"
                portal_api_employee_details = f"{os.getenv('PORTAL_API_URL')}/api/employee/list/search/?q="

                # Perform login request to external API
                response = requests.post(portal_api_login, data={
                    'username': username,
                    'password': password
                })

                if response.status_code == 200:
                    results = response.json()
                    api_key = results['key']

                    # Fetch employee details using the token received
                    response_employee_details = requests.get(f"{portal_api_employee_details}{username}", headers={
                        'Authorization': f"Token {api_key}"
                    })

                    if response_employee_details.status_code == 200:
                        # Return successful response with the employee details

                        breakpoint()
                        return {
                            'status_code': 200,
                            'status': 'success',
                            'data': {
                                'key': api_key,
                                'username': username,
                                'employee_details': response_employee_details.json()
                            }
                        }
                    else:
                        # Handle case when no employee details are found
                        return {
                            'status_code': 422,
                            'status': 'error',
                            'message': 'No user found in portal'
                        }

                else:
                    # Handle login failure
                    return {
                        'status_code': response.status_code,
                        'status': 'error',
                        'message': 'Invalid username or password'
                    }

            except requests.exceptions.RequestException as e:
                # Handle errors with external API communication
                return {
                    'status_code': 500,
                    'status': 'error',
                    'message': f'Error connecting to external API: {str(e)}'
                }

        # Handle validation failure from serializer
        return {
            'status_code': 400,
            'status': 'error',
            'message': serializer.errors
        }

def signin_service(request, params):
        data = params['data']
        api_key = data['key']
        portal_api_employee_details = f"{os.getenv('PORTAL_API_URL')}/api/employee/list/search/?q="
        username = data['username']
        try:
            user = User.objects.get(username=username)
            user.last_login = timezone.now()
            user.save()
        except User.DoesNotExist:
            response_employee_details = requests.get(f"{portal_api_employee_details}{username}", headers={
                'Authorization': f"Token {api_key}"
            })
            api_response_employee_details_data = response_employee_details.json()
            employee_details_data = api_response_employee_details_data[0]
            user = CustomUser.objects.create(
                employee_id=employee_details_data['employee_id'],
                id_number=employee_details_data['id_number'],
                last_login=timezone.now(),
                username=employee_details_data['username'],
                first_name=employee_details_data['first_name'],
                middle_name=employee_details_data['middle_name'],
                last_name=employee_details_data['last_name'],
                contact=employee_details_data['contact'],
                account_number=employee_details_data['account_number'],
                position=employee_details_data['position'],
                division=employee_details_data['division'],
                section=employee_details_data['section'],
                area_of_assignment=employee_details_data['area_of_assignment'],
                gender=employee_details_data['gender'],
                birthdate=employee_details_data['birthdate'],
                image_path=employee_details_data['image_path'],
                status=employee_details_data['status'],
            )

        auth_login(request, user)

        request.session['user_id'] = user.id
        request.session['user_id_number'] = user.id_number
        request.session['user_first_name'] = user.first_name
        request.session['user_middle_name'] = user.middle_name
        request.session['user_last_name'] = user.last_name
        request.session['user_position'] = user.position
        request.session['user_image'] = user.image_path
        

        user_data = {
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'image_path': user.image_path,
            'position': user.position,
            'division': user.division,
            'section': user.section,
        }
        return user_data

def signout(request):
    request.session.flush()

    auth_logout(request)
    return HttpResponseRedirect('/signin')