
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
        lib_data = LibCosGuidelinesActivities.objects.filter().order_by('-id')

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
                'is_email_notify': item.is_email_notify,
                'description': item.description,
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
                'is_email_notify': item.is_email_notify,
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
def LibrariesAddCos(request):
    try:
        name = request.POST.get('add_cos_name')
        description = request.POST.get('add_cos_description')
        email_notify = request.POST.get('cos_email_notify')
        email_notify = 1 if email_notify == "true" else 0

        if LibCosGuidelinesActivities.objects.filter(name=name).exists():
            return JsonResponse({'data': 'error', 'message': f'{name} Name already exists'})
        else:
            cos = LibCosGuidelinesActivities(name=name,description=description, is_email_notify = email_notify, created_at = localtime)
            cos.save()
            return JsonResponse({'data': 'success','message': name,'title': 'Success'})
    except Exception as e:
        return JsonResponse({'data': 'error', 'message': e})
    
@csrf_exempt
def LibrariesUpdateCos(request):
    try:
        id = request.POST.get('cos_id')
        name = request.POST.get('update_cos_name')
        description = request.POST.get('update_cos_description')
        email_notify = request.POST.get('cos_email_notify')
        email_notify = 1 if email_notify == "true" else 0
        LibCosGuidelinesActivities.objects.filter(id=id).update(
            name=name,
            description=description,
            is_email_notify = email_notify,
            updated_at = now())
        return JsonResponse({'data': 'success','message': name,'title': 'Success'})
    except Exception as e:
        return JsonResponse({'data': 'error', 'message': e})

@csrf_exempt
def LibrariesAddNeop(request):
    try:
        name = request.POST.get('add_neop_name')
        description = request.POST.get('add_neop_description')
        milestone = request.POST.get('add_neop_milestone')
        email_notify = request.POST.get('neop_email_notify')
        email_notify = 1 if email_notify == "true" else 0

        if LibNeopActivities.objects.filter(name=name).exists():
                return JsonResponse({'data': 'error', 'message': name + ' Name already Exists'})
        else:
            neop = LibNeopActivities(name=name,description=description, is_email_notify = email_notify, milestone = milestone, created_at = localtime)
            neop.save()
            return JsonResponse({'data': 'success','message': name,'title': 'Success'})
    except Exception as e:
        return JsonResponse({'data': 'error', 'message': e})
    
@csrf_exempt
def LibrariesUpdateNeop(request):
    try:
        neop_id = request.POST.get('neop_id')
        name = request.POST.get('update_neop_name')
        description = request.POST.get('update_neop_description')
        milestone = request.POST.get('update_neop_milestone')
        email_notify = request.POST.get('neop_email_notify')
        email_notify = 1 if email_notify == "true" else 0
        LibNeopActivities.objects.filter(id=neop_id).update(
            name=name,
            description=description,
            milestone=milestone,
            is_email_notify = email_notify,
            updated_at = now())
        return JsonResponse({'data': 'success','message': name,'title': 'Success'})
    except Exception as e:
        return JsonResponse({'data': 'error', 'message': e})