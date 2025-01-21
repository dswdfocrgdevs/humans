
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from rsp.models import LibNeopActivities, NewlyHiredStaff, StaffNeopActivities, StaffNeopInfo, LibCosGuidelinesActivities
from datetime import datetime
import json
from django.utils.timezone import localtime
from django.utils.timezone import now

@csrf_exempt
def LibrariesCosWithGuidelines(request):
    try:
        # Get query params for pagination and search
        page = int(request.GET.get('page', 1))  # Default page is 1
        per_page = int(request.GET.get('length', 10))  # Default length is 10
        search_value = request.GET.get('search[value]', '').strip()  # Get search query

        # Fetch data and apply search filter if search term exists
        newly_hired_data = NewlyHiredStaff.objects.filter(onboarding_type_id=1)

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
        data = []
        for item in paginated_data:
            # Fetch related StaffNeopInfo data for each NewlyHiredStaff
            try:
                staff_neop_info = StaffNeopInfo.objects.get(staff_id=item.id)
                assumption_date = staff_neop_info.assumption_date
                date_end_third = staff_neop_info.date_end_third
                date_end_sixth = staff_neop_info.date_end_sixth
            except StaffNeopInfo.DoesNotExist:
                assumption_date = None
                date_end_third = None
                date_end_sixth = None

            data.append({
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
                'assumption_date': assumption_date,  # Add assumption_date
                'date_end_third': date_end_third,    # Add date_end_third
                'date_end_sixth': date_end_sixth    # Add date_end_sixth
            })
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
def LibrariesNeop(request):
    try:
        # Get query params for pagination and search
        page = int(request.GET.get('page', 1))  # Default page is 1
        per_page = int(request.GET.get('length', 10))  # Default length is 10
        search_value = request.GET.get('search[value]', '').strip()  # Get search query

        # Fetch data and apply search filter if search term exists
        lib_data = LibNeopActivities.objects.filter().order_by('-id')

        if search_value:
            lib_data = lib_data.filter(
                name__icontains=search_value
            )

        # Total records (before pagination)
        total = lib_data.count()

        # Paginate data
        start = (page - 1) * per_page
        paginated_data = lib_data[start:start + per_page]

        # Prepare data for response
        data = []
        for item in paginated_data:
            data.append({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'milestone': item.milestone,
                'created_at': localtime(item.created_at).strftime('%B %d, %Y %I:%M %p'),
                'updated_at': localtime(item.updated_at).strftime('%B %d, %Y %I:%M %p')
            })
        return JsonResponse({
            'data': data,
            'recordsTotal': total,
            'recordsFiltered': total,
        })

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({
            'data': [],
            'recordsTotal': 0,
            'recordsFiltered': 0,
        }, status=200)
    
@csrf_exempt
def LibrariesAddNeop(request):
    neop_name = request.POST.get('add_neop_name')
    neop_description = request.POST.get('add_neop_description')
    neop_milestone = request.POST.get('add_neop_milestone')

    if LibNeopActivities.objects.filter(name=neop_name).exists():
            return JsonResponse({'status': 'error', 'message': 'Neop Name already Exists'})
    else:
        neop = LibNeopActivities(name=neop_name,description=neop_description, milestone = neop_milestone, created_at = localtime)
        neop.save()
        return JsonResponse({'data': 'success'})
    
@csrf_exempt
def LibrariesUpdateNeop(request):
    neop_id = request.POST.get('neop_id')
    neop_name = request.POST.get('update_neop_name')
    neop_description = request.POST.get('update_neop_description')
    neop_milestone = request.POST.get('update_neop_milestone')
    LibNeopActivities.objects.filter(id=neop_id).update(
        name=neop_name,
        description=neop_description,
        milestone=neop_milestone,
        updated_at = now())
    return JsonResponse({'data': 'success'})