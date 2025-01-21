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
from rsp.models import NewlyHiredStaff, RspOnboardingLayout, NewlyHiredStaffStreamline, StaffEndorsementActivities, EndorsementActivities, HiredreqCompliance, OnboardingStatus, OnboardingStatusNewlyhired
from ..utils import search_employees
from django.db.models import Count, Case, When, Value, CharField
from django.db.models import Q
from django.template import Context, Template
import json
from django.db import connection
from rsp.views.rsp.functions import safe_decode
from datetime import date
import subprocess
import logging

logger = logging.getLogger(__name__)

def check_activities_exist(endorsed, staff_id):
    """Check if all activities for a given staff member exist based on the endorsement, 
       and return progress (completed/total)."""
    with connection.cursor() as cursor:
        query = """
        SELECT 
            CASE 
                WHEN NOT EXISTS (
                    SELECT 1
                    FROM rsp_endorsementactivities lib
                    WHERE lib.endorsed = %s
                    AND NOT EXISTS (
                        SELECT 1
                        FROM rsp_staffendorsementactivities staff
                        WHERE staff.staff_id_id = %s
                        AND staff.lib_endorsed_id_id = lib.id
                    )
                ) THEN 'TRUE'
                ELSE 'FALSE'
            END AS all_activities_exist,
            
            CONCAT(
                (SELECT COUNT(1) 
                 FROM rsp_staffendorsementactivities staff 
                 WHERE staff.staff_id_id = %s 
                 AND EXISTS (
                    SELECT 1 
                    FROM rsp_endorsementactivities lib 
                    WHERE lib.id = staff.lib_endorsed_id_id 
                    AND lib.endorsed = %s
                )),
                '/', 
                (SELECT COUNT(1) 
                 FROM rsp_endorsementactivities lib 
                 WHERE lib.endorsed = %s)
            ) AS progress;
        """
        cursor.execute(query, [endorsed, staff_id, staff_id, endorsed, endorsed])
        result = cursor.fetchone()

    return {
        'all_activities_exist': True if result and result[0] == 'TRUE' else False,
        'progress': safe_decode(result[1]) if result and result[1] else '0/0'  # Decode and default to '0/0'
    }

def dashboard(request):
    today = date.today()
    count_hired_emp_status = NewlyHiredStaff.objects.values('emp_status').annotate(count=Count('id')).order_by('-count')
    count_hired_nature = (
        NewlyHiredStaff.objects.annotate(
            grouped_nature=Case(
                When(nature__isnull=True, then=Value('N/A')),
                When(nature='N/A', then=Value('N/A')),
                default='nature',
                output_field=CharField()
            )
        )
        .values('grouped_nature')
        .annotate(count=Count('id'))
        .order_by('grouped_nature')
        .order_by('-count')
    )
    count_onboardstaff_today = OnboardingStatusNewlyhired.objects.filter(datetime_created__date=today).count()
    count_onboardstaff_neop_today = OnboardingStatusNewlyhired.objects.filter(onboarding_type_id=1, datetime_created__date=today).count()
    count_onboardstaff_cosguide_today = OnboardingStatusNewlyhired.objects.filter(onboarding_type_id=2, datetime_created__date=today).count()
    count_onboardstaff_internal_today = OnboardingStatusNewlyhired.objects.filter(onboarding_type_id=3, datetime_created__date=today).count()
    context = {
        'title': 'Dashboard',
        'count_hired_emp_status': count_hired_emp_status,
        'count_hired_nature' : count_hired_nature,
        'count_onboardstaff_today': count_onboardstaff_today,
        'count_onboardstaff_neop_today': count_onboardstaff_neop_today,
        'count_onboardstaff_cosguide_today': count_onboardstaff_cosguide_today,
        'count_onboardstaff_internal_today': count_onboardstaff_internal_today
    }

    return render(request, 'rsp/Dashboard.html', context)

def onboarding_forms(request):
    context = {
        'title': 'Onboarding Forms'
    }
    return render(request, 'rsp/OnBoardingForms.html', context)

@csrf_exempt
def newly_hired_staff(request):
    if request.method == "POST":
        try:
            chck = NewlyHiredStaff.objects.filter(id=request.POST.get('id')).first()
            chck.remarks = request.POST.get('remarks')
            chck.save()
            return JsonResponse({'data': 'success'})
        except Exception as e:
            return JsonResponse({'data': 'error', 'msg': str(e)})
    context = {
        'title': 'Newly Hired Staff',
        'status': OnboardingStatus.objects.filter(status=1).all()
    }
    return render(request, 'rsp/NewlyHiredStaff/index.html', context)

def newly_hired_staff_streamline(request):
    context = {
        'title': 'Newly Hired Staff Streamline'
    }
    return render(request, 'rsp/NewlyHiredStaff/index-streamline.html', context)

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
    try:
        # Get query params for pagination and search
        page = int(request.GET.get('page', 1))  # Default page is 1
        per_page = int(request.GET.get('length', 10))  # Default length is 10
        search_value = request.GET.get('search[value]', '').strip()  # Get search query

        # Fetch data and apply search filter if search term exists
        newly_hired_data = NewlyHiredStaff.objects.all()

        if search_value:
            newly_hired_data = newly_hired_data.filter(
                full_name__icontains=search_value
            )

        # Total records (before pagination)
        total = newly_hired_data.count()

        # Paginate data
        start = (page - 1) * per_page
        paginated_data = newly_hired_data[start:start + per_page]

        # Prepare data for response
        data = [{
            'id': item.id,
            'app_id': item.id,
            'full_name': item.full_name,
            'position': item.position,
            'former_incumbent': item.former_incumbent,
            'salary': item.salary,
            'effectivity_of_contract': item.effectivity_of_contract,
            'end_of_contract': item.end_of_contract,
            'emp_status': item.emp_status,
            'nature': item.nature,
            'area_of_assignment': item.area_of_assignment,
            'requirements_ok': item.requirements_ok,
            'remarks': item.remarks,
            'onboarding_type': (
                'NEOP' if item.onboarding_type_id == 1 else
                'COS with guidelines' if item.onboarding_type_id == 2 else
                'Internal Staff' if item.onboarding_type_id == 3 else
                item.onboarding_type_id
            ),
            'endorse_welfare': check_activities_exist(1, item.id)['all_activities_exist'],
            'endorse_welfareprogress': check_activities_exist(1, item.id)['progress'],
            'endorse_lds': check_activities_exist(2, item.id)['all_activities_exist'],
            'endorse_ldsprogress': check_activities_exist(2, item.id)['progress'],
            'endorse_pms': check_activities_exist(3, item.id)['all_activities_exist'],
            'endorse_pmsprogress': check_activities_exist(3, item.id)['progress'],
            'endorse_pas': check_activities_exist(4, item.id)['all_activities_exist'],
            'endorse_pasprogress': check_activities_exist(4, item.id)['progress'],
        } for item in paginated_data]

        return JsonResponse({
            'data': data,
            'recordsTotal': total,  # Total records without filtering
            'recordsFiltered': total,  # Total filtered records after search
        })

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({
            'data': [],
            'recordsTotal': 0,
            'recordsFiltered': 0,
        }, status=200)
    
@csrf_exempt
def view_hired_requirements(request, pk):
    print(pk)
    app = NewlyHiredStaff.objects.filter(id=pk).first()
    if request.method == "POST":
        try:
            req_ids = request.POST.getlist('req_id[]')
            app_ids = request.POST.getlist('app_id[]')
            date_compliance = request.POST.getlist('date_compliance[]')
            date_remarkscompliance = request.POST.getlist('date_remarkscompliance[]')

            data = [
                {'req_id': req_ids[i], 'app_id': app_ids[i], 
                'date_compliance': date_compliance[i], 'date_remarkscompliance': date_remarkscompliance[i]}
                for i in range(len(req_ids))
                if date_compliance[i] and date_remarkscompliance[i]
            ]

            existing_compliances = HiredreqCompliance.objects.filter(app_id=app.app_id)
            existing_ids = {str(compliance.hired_req_id): compliance.id for compliance in existing_compliances}

            for row in data:
                req_id = str(row['req_id'])  # Ensure the req_id is compared as a string
                if req_id in existing_ids:
                    # Update existing record
                    compliance_id = existing_ids[req_id]
                    HiredreqCompliance.objects.filter(id=compliance_id).update(
                        app_id=row['app_id'],
                        hired_req_id=row['req_id'],
                        remarks=row['date_remarkscompliance'],
                        datetime=row['date_compliance'],
                    )
                else:
                    # Create new record
                    HiredreqCompliance.objects.create(
                        app_id=row['app_id'],
                        hired_req_id=row['req_id'],
                        remarks=row['date_remarkscompliance'],
                        datetime=row['date_compliance'],
                    )

            # # Delete records that are no longer in the submitted data
            # OasHiredreqCompliance.objects.filter(hired_req_id__in=to_delete_ids).delete()
            return JsonResponse({'data': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    app_hired = NewlyHiredStaff.objects.filter(id = pk, requirements_ok='Done').first()
    context = {
        'app': app,
        'app_hired' : app_hired,
        'total_compliance': HiredreqCompliance.objects.filter(app_id=pk).count(),
        # 'files': ApplicantsFile.objects.filter(app_id=pk),
        'pk': pk
    }
    return render(request, 'rsp/NewlyHiredStaff/view_hired_requirements.html', context)


@csrf_exempt
def hiredreq_complete(request):
    if request.method == "POST":
        try:
            check_hired = NewlyHiredStaff.objects.filter(id = request.POST.get('app_id')).first()
            if not check_hired:
                NewlyHiredStaff.objects.create(
                    id = request.POST.get('app_id'),
                    remarks ='Requirements Done',
                    requirements_ok = 'Done',
                    )
            else:
                check_hired.requirements_ok = 'Done'
                check_hired.remarks = 'Requirements Done'
                check_hired.save()
                    
            if check_hired:
                message = 'Dear {}, We would like to confirm that we have received all \
                            your required documents for the onboarding process. After a thorough review and \
                            verification, we are pleased to inform you that all the submitted documents are in \
                            order. Thank you for your prompt submission.'.format(check_hired.full_name)
            # checkhistory = OasApplicantsSchedHistory.objects.filter(Q(app_id=request.POST.get('app_id')) & Q(workflow_status_id=5)).first()
            # if checkhistory:
            # 	OasApplicantsSchedHistory.objects.create(
            # 		app_id=request.POST.get('app_id'),
            # 		details = 'Requirements Completed: {}'.format(datetime.now()),
            # 		workflow_status_id=8,
            # 		remarks=message)
            print(message)
            # send_notification(request.user.id , message, app.pi.mobile_no)
            # if app.pi.mobile_no_two:
            # 	send_notification(request.user.id , message, app.pi.mobile_no_two)
            return JsonResponse({'data': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@csrf_exempt
def hiredreq_not_complete(request):
    if request.method == "POST":
        try:
            chck = NewlyHiredStaff.objects.filter(id = request.POST.get('app_id')).first()
            chck.remarks = request.POST.get('remarks')
            chck.save()
            # send_notification(request.user.id , message, app.pi.mobile_no)
            # if app.pi.mobile_no_two:
            # 	send_notification(request.user.id , message, app.pi.mobile_no_two)
            return JsonResponse({'data': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def delete_hiredreq_compliance(request):
        HiredreqCompliance.objects.filter(
                Q(app_id=request.POST.get('emp_id')) & Q(hired_req_id=request.POST.get('req_id'))).delete()
        return JsonResponse({'data': 'success'})


def GetLibEndorsedActivities(request):
    endorsed = request.GET.get('endorsed')
    staff_id = request.GET.get('staff_id')

    staff_endorsed_activities = StaffEndorsementActivities.objects.filter(staff_id_id=staff_id)

    if endorsed:
        lib_endorsed_activities = EndorsementActivities.objects.filter(endorsed=endorsed)
    else:
        lib_endorsed_activities = EndorsementActivities.objects.all()

    activities_data = list(lib_endorsed_activities.values('id', 'name', 'description', 'endorsed'))

    for activity in activities_data:
        activity['test'] = 1

        staff_activity = staff_endorsed_activities.filter(lib_endorsed_id=activity['id']).first()
        
        if staff_activity:
            activity['date'] = staff_activity.date  # Assuming `date` is a field in StaffNeopActivities
            activity['remarks'] = staff_activity.remarks  # Assuming `remarks` is a field in StaffNeopActivities

    return JsonResponse({
        'lib_endorsed_activities': activities_data
    }, status=200)


@csrf_exempt
def PostLibEndorsedActivities(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)  # Deserialize JSON data
            
            # If your data has a `data` key as in the JavaScript payload
            activities = data.get('data', [])

            for activity in activities:
                staff = NewlyHiredStaff.objects.get(id=activity.get('user_id'))  # Fetch the staff object
                lib_endorsed_activity = EndorsementActivities.objects.get(id=activity.get('id'))  # Get the LibNeopActivities object
                StaffEndorsementActivities.objects.update_or_create(
                    staff_id=staff,
                    lib_endorsed_id=lib_endorsed_activity,
                    defaults={
                        'date': activity.get('date'),
                        'remarks': activity.get('remarks')
                    }
                )

            return JsonResponse({"message": "Activities saved successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def list_newly_hired_staff_streamline(request):
    try:
        # Get query params for pagination and search
        page = int(request.GET.get('page', 1))  # Default page is 1
        per_page = int(request.GET.get('length', 10))  # Default length is 10
        search_value = request.GET.get('search[value]', '').strip()  # Get search query

        # Fetch data and apply search filter if search term exists
        newly_hired_data = NewlyHiredStaffStreamline.objects.all()

        if search_value:
            newly_hired_data = newly_hired_data.filter(
                full_name__icontains=search_value
            )

        # Total records (before pagination)
        total = newly_hired_data.count()

        # Paginate data
        start = (page - 1) * per_page
        paginated_data = newly_hired_data[start:start + per_page]

        # Prepare data for response
        data = [{
            'id': item.id,
            'app_id': item.id,
            'full_name': item.full_name,
            'position': item.position,
            'former_incumbent': item.former_incumbent,
            'salary': item.salary,
            'effectivity_of_contract': item.effectivity_of_contract,
            'end_of_contract': item.end_of_contract,
            'emp_status': item.emp_status,
            'nature': item.nature,
            'area_of_assignment': item.area_of_assignment,
            'requirements_ok': item.requirements_ok,
            'remarks': item.remarks,
        } for item in paginated_data]

        return JsonResponse({
            'data': data,
            'recordsTotal': total,  # Total records without filtering
            'recordsFiltered': total,  # Total filtered records after search
        })

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({
            'data': [],
            'recordsTotal': 0,
            'recordsFiltered': 0,
        }, status=200)


def employee_search_data(request):
    query = request.GET.get('query', '')
    
    # Use the utility function to get the employee data
    employee_data = search_employees(query)
    
    # Return the data as a JSON response
    return JsonResponse({'results': employee_data})


def print_notice_of_appointed_applicants(request, pk):
    app = NewlyHiredStaff.objects.filter(Q(id=pk)).first()
    context = {
        'applicants': app,
    }
    return render(request, 'rsp/NewlyHiredStaff/print_notice_of_appointed.html', context)

def print_onboarding_forms(request, pk, ids=None):
    id_list = ids.split(',')
    app = NewlyHiredStaff.objects.filter(Q(id__in=id_list))
    context = {
        'app': app,
        'pk': pk
    }
    return render(request, 'rsp/NewlyHiredStaff/print_onboarding_forms.html', context)


@csrf_exempt
def print_req_checklist(request, pk=None):
    if pk != '0':
        ids = pk.split(',')
        all = NewlyHiredStaff.objects.filter(Q(id__in=ids))
        context = {
            'pk': pk,
            'all': all,
        }
    return render(request, 'rsp/NewlyHiredStaff/print_requirements_checklist.html', context)


@csrf_exempt
def print_req_checklist_streamline(request, pk=None):
    if pk != '0':
        ids = pk.split(',')
        all = NewlyHiredStaffStreamline.objects.filter(Q(id__in=ids))
        context = {
            'pk': pk,
            'all': all,
        }
    return render(request, 'rsp/NewlyHiredStaff/print_requirements_checklist_streamline.html', context)

@csrf_exempt
def PatchNewlyHiredOnboarding(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body)

        # Extract the relevant data from the payload
        staff_ids = data.get("data", {}).get("staffIds", [])
        onboarding_type = data.get("data", {}).get("type", None)

        # Validate that required data is present
        if not staff_ids or onboarding_type is None:
            return JsonResponse({"error": "Missing required fields: staffIds or type"}, status=400)

        # Iterate over the staff IDs and update their onboarding_type
        updated_count = 0
        not_found_ids = []
        for staff_id in staff_ids:
            staff_neop_info = NewlyHiredStaff.objects.filter(id=staff_id).first()
            if staff_neop_info:
                staff_neop_info.onboarding_type_id = onboarding_type
                staff_neop_info.save()
                updated_count += 1
                check = OnboardingStatusNewlyhired.objects.filter(app_id = staff_id).first()
                if not check:
                    OnboardingStatusNewlyhired.objects.create(app_id = staff_id, onboarding_type_id = onboarding_type)
                else:
                    check.onboarding_type_id = onboarding_type
                    check.save()
            else:
                not_found_ids.append(staff_id)

        # Build the response message
        response_message = {
            "updated_count": updated_count,
            "not_found_ids": not_found_ids,
        }

        return JsonResponse(response_message, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def SyncIris(request):
    try:
        # Run the Python script to execute the seeder command and capture error output
        result = subprocess.run(
            ['python', 'manage.py', 'fetch_hired_applicants'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Check the script output
        logger.info(f"Script Output: {result.stdout}")
        
        return JsonResponse({
            'status': 'success'
        }, status=200)
    
    except subprocess.CalledProcessError as e:
        # Log the error output from the script
        logger.error(f"Error running script: {e.stderr}")
        
        return JsonResponse({
            'status': 'error',
            'message': f"An error occurred: {e.stderr}"
        }, status=400)