
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from rsp.models import LibNeopActivities, NewlyHiredStaff, StaffNeopActivities, StaffNeopInfo
from datetime import datetime
import json

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
        cursor.execute(query, [milestone, staff_id, staff_id, milestone, milestone])
        result = cursor.fetchone()

    # Decode bytes if necessary and handle null cases
    def safe_decode(value):
        if isinstance(value, bytes):
            return value.decode('utf-8')
        return value

    return {
        'all_activities_exist': True if result and result[0] == 'TRUE' else False,
        'progress': safe_decode(result[1]) if result and result[1] else '0/0'  # Decode and default to '0/0'
    }

@csrf_exempt
def ListNewlyHiredNeop(request):
    try:
        # Get query params for pagination and search
        page = int(request.GET.get('page', 1))  # Default page is 1
        per_page = int(request.GET.get('length', 10))  # Default length is 10
        search_value = request.GET.get('search[value]', '').strip()  # Get search query

        # Fetch data and apply search filter if search term exists
        newly_hired_data = NewlyHiredStaff.objects.filter(onboarding_type='neop')

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
        
def Neop (request):
    return render(request, 'rsp/Neop/index.html', {
        'title': 'NEOP'
    })

def GetLibNeopActivities(request):
    # Get the 'milestone' and 'staff_id' parameters from the URL query string
    milestone = request.GET.get('milestone')
    staff_id = request.GET.get('staff_id')

    # Get the StaffNeopActivities for the provided staff_id
    staff_neop_activities = StaffNeopActivities.objects.filter(staff_id_id=staff_id)

    # Filter LibNeopActivities based on the provided milestone
    if milestone:
        lib_neop_activities = LibNeopActivities.objects.filter(milestone=milestone)
    else:
        lib_neop_activities = LibNeopActivities.objects.all()

    # Serialize the LibNeopActivities queryset
    activities_data = list(lib_neop_activities.values('id', 'name', 'description', 'milestone'))

    # Add the 'test' column with value 1 for each row
    for activity in activities_data:
        activity['test'] = 1

        # Check if there's a corresponding StaffNeopActivity
        staff_activity = staff_neop_activities.filter(lib_neop_id_id=activity['id']).first()
        
        if staff_activity:
            # Add 'date' and 'remarks' from StaffNeopActivities
            activity['date'] = staff_activity.date  # Assuming `date` is a field in StaffNeopActivities
            activity['remarks'] = staff_activity.remarks  # Assuming `remarks` is a field in StaffNeopActivities

    return JsonResponse({
        'lib_neop_activities': activities_data
    }, status=200)

@csrf_exempt
def PostLibNeopActivities(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)  # Deserialize JSON data
            
            # If your data has a `data` key as in the JavaScript payload
            activities = data.get('data', [])

            for activity in activities:
                staff = NewlyHiredStaff.objects.get(id=activity.get('user_id'))  # Fetch the staff object
                lib_neop_activity = LibNeopActivities.objects.get(id=activity.get('id'))  # Get the LibNeopActivities object
                StaffNeopActivities.objects.update_or_create(
                    staff_id=staff,
                    lib_neop_id=lib_neop_activity,
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
def PostNeopStaffInfo(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body)

        # Extract data
        staff_id = data.get('data', {}).get('staff_id')
        assumption_date = data.get('data', {}).get('assumption_date')
        date_end_third = data.get('data', {}).get('date_end_third')
        date_end_sixth = data.get('data', {}).get('date_end_sixth')

        # Helper function to safely parse date strings
        def parse_date(date_str):
            if date_str:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            return None

        # Safely convert the date strings to date objects
        assumption_date = parse_date(assumption_date)
        date_end_third = parse_date(date_end_third)
        date_end_sixth = parse_date(date_end_sixth)

        # Get the staff instance
        try:
            staff = NewlyHiredStaff.objects.get(id=staff_id)
        except NewlyHiredStaff.DoesNotExist:
            return JsonResponse({"error": "Staff not found"}, status=404)

        # Check if StaffNeopInfo exists for the given staff
        staff_neop_info, created = StaffNeopInfo.objects.update_or_create(
            staff_id=staff,  # Use staff instance for the foreign key
            defaults={
                'assumption_date': assumption_date,
                'date_end_third': date_end_third,
                'date_end_sixth': date_end_sixth,
            }
        )

        # Return success response
        if created:
            message = "Staff Neop Info created successfully"
        else:
            message = "Staff Neop Info updated successfully"

        return JsonResponse({"message": message}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)