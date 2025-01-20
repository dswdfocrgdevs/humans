
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from rsp.models import LibNeopActivities, NewlyHiredStaff, StaffNeopActivities, StaffNeopInfo
from datetime import datetime
import json
from rsp.views.rsp.functions import safe_decode

def GetInternalStaff (request):
    return render(request, 'rsp/InternalStaff/index.html', {
        'title': 'Internal Staff'
    })

def check_activities_exist(milestone, staff_id):
    """Check if all activities for a given staff member exist based on the milestone, 
       and return progress (completed/total)."""
    with connection.cursor() as cursor:
        query = """
        SELECT 
            CASE 
                WHEN NOT EXISTS (
                    SELECT 1
                    FROM rsp_libneopactivities lib
                    WHERE lib.milestone = %s
                    AND NOT EXISTS (
                        SELECT 1
                        FROM rsp_staffneopactivities staff
                        WHERE staff.staff_id_id = %s
                        AND staff.lib_neop_id_id = lib.id
                    )
                ) THEN 'TRUE'
                ELSE 'FALSE'
            END AS all_activities_exist,
            
            CONCAT(
                (SELECT COUNT(1) 
                 FROM rsp_staffneopactivities staff 
                 WHERE staff.staff_id_id = %s 
                 AND EXISTS (
                    SELECT 1 
                    FROM rsp_libneopactivities lib 
                    WHERE lib.id = staff.lib_neop_id_id 
                    AND lib.milestone = %s
                )),
                '/', 
                (SELECT COUNT(1) 
                 FROM rsp_libneopactivities lib 
                 WHERE lib.milestone = %s)
            ) AS progress;
        """
        cursor.execute(query, [milestone, staff_id, staff_id, milestone, milestone])  # Pass both `milestone` and `staff_id`
        result = cursor.fetchone()

    # Return a dictionary with both existence and progress
    return {
        'all_activities_exist': True if result and result[0] == 'TRUE' else False,
        'progress': safe_decode(result[1]) if result else '0/0'  # Default to '0/0' if no result
    }
    

@csrf_exempt
def ListNewlyHiredInternalStaff(request):
    try:
        # Get query params for pagination and search
        page = int(request.GET.get('page', 1))  # Default page is 1
        per_page = int(request.GET.get('length', 10))  # Default length is 10
        search_value = request.GET.get('search[value]', '').strip()  # Get search query

        # Fetch data and apply search filter if search term exists
        newly_hired_data = NewlyHiredStaff.objects.filter(onboarding_type_id=3)

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
                'milestone1': check_activities_exist(1, item.id)['all_activities_exist'],
                'milestone2': check_activities_exist(2, item.id)['all_activities_exist'],
                'milestone3': check_activities_exist(3, item.id)['all_activities_exist'],
                'milestone4': check_activities_exist(4, item.id)['all_activities_exist'],
                'milestone5': check_activities_exist(5, item.id)['all_activities_exist'],
                'milestone1progress': check_activities_exist(1, item.id)['progress'],
                'milestone2progress': check_activities_exist(2, item.id)['progress'],
                'milestone3progress': check_activities_exist(3, item.id)['progress'],
                'milestone4progress': check_activities_exist(4, item.id)['progress'],
                'milestone5progress': check_activities_exist(5, item.id)['progress'],
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