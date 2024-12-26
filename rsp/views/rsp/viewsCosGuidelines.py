


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from rsp.models import LibCosGuidelinesActivities, NewlyHiredStaff, StaffCosGuidelinesActivities, StaffCosGuidelinesInfo
from datetime import datetime
import json

@csrf_exempt


def check_activities_exist(staff_id):
    """Check if all activities for a given staff member exist and return progress (completed/total)."""
    with connection.cursor() as cursor:
        query = """
        SELECT 
            CASE 
                WHEN NOT EXISTS (
                    SELECT 1
                    FROM rsp_libcosguidelinesactivities lib
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM rsp_staffcosguidelinesactivities staff
                        WHERE staff.staff_id_id = %s
                        AND staff.lib_cos_guidelines_id_id = lib.id
                    )
                ) THEN 'TRUE'
                ELSE 'FALSE'
            END AS all_activities_exist,
            
            CONCAT(
                (SELECT COUNT(1) 
                 FROM rsp_staffcosguidelinesactivities staff 
                 WHERE staff.staff_id_id = %s
                 AND EXISTS (
                    SELECT 1 
                    FROM rsp_libcosguidelinesactivities lib 
                    WHERE lib.id = staff.lib_cos_guidelines_id_id
                )),
                '/', 
                (SELECT COUNT(1) 
                 FROM rsp_libcosguidelinesactivities lib)
            ) AS progress;
        """
        cursor.execute(query, [staff_id, staff_id])  # Pass `staff_id`
        result = cursor.fetchone()

    # Return a dictionary with both existence and progress
    return {
        'all_activities_exist': True if result and result[0] == 'TRUE' else False,
        'progress': result[1] if result else '0/0'  # Default to '0/0' if no result
    }

def GetCosGuideLines (request):
    return render(request, 'rsp/CosGuidelines/index.html', {
        'title': 'COS with Guidelines'
    })

def GetCosGuideLinesStaffList(request):
    try:
        # Get query params for pagination and search
        page = int(request.GET.get('page', 1))  # Default page is 1
        per_page = int(request.GET.get('length', 10))  # Default length is 10
        search_value = request.GET.get('search[value]', '').strip()  # Get search query

        # Fetch data and apply search filter if search term exists
        newly_hired_data = NewlyHiredStaff.objects.all()
        newly_hired_data = newly_hired_data.filter(
            emp_status__icontains='COS'
        )

        if search_value:
            newly_hired_data = newly_hired_data.filter(
                full_name__icontains=search_value
            )
      

        # Total records (before pagination)
        total = newly_hired_data.count()

        # Paginate data
        start = (page - 1) * per_page

        data = []
        paginated_data = newly_hired_data[start:start + per_page]

        for item in paginated_data:
            # Fetch related StaffNeopInfo data for each NewlyHiredStaff
            try:
                staff_cost_guidelines_info = StaffCosGuidelinesInfo.objects.get(staff_id=item.id)
                assumption_date = staff_cost_guidelines_info.assumption_date
                requirements_submission_date = staff_cost_guidelines_info.requirements_submission_date
                ccef_submission_date = staff_cost_guidelines_info.ccef_submission_date
                agency_orientation = staff_cost_guidelines_info.agency_orientation
            except StaffCosGuidelinesInfo.DoesNotExist:
                assumption_date = None
                requirements_submission_date = None
                ccef_submission_date = None
                agency_orientation = None

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
                'activityExist': check_activities_exist(item.id)['all_activities_exist'],
                'activityProgress': check_activities_exist(item.id)['progress'],
                'assumption_date': assumption_date,   
                'requirements_submission_date': requirements_submission_date,   
                'ccef_submission_date': ccef_submission_date,
                'agency_orientation': agency_orientation    
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

def GetLibCosGuideLinesActivities(request):
    # Get the 'milestone' and 'staff_id' parameters from the URL query string
    staff_id = request.GET.get('staff_id')

    # Get the StaffCosGuidelinesActivities for the provided staff_id
    staff_neop_activities = StaffCosGuidelinesActivities.objects.filter(staff_id_id=staff_id)

    # Filter LibCosGuidelinesActivities based on the provided milestone
    lib_cos_guidelines_activities = LibCosGuidelinesActivities.objects.all()
        
    # Serialize the LibCosGuidelinesActivities queryset
    activities_data = list(lib_cos_guidelines_activities.values('id', 'name', 'description'))

    # Add the 'test' column with value 1 for each row
    for activity in activities_data:
        activity['test'] = 1

        # Check if there's a corresponding StaffNeopActivity
        staff_activity = staff_neop_activities.filter(lib_cos_guidelines_id_id=activity['id']).first()
        
        if staff_activity:
            # Add 'date' and 'remarks' from StaffCosGuidelinesActivities
            activity['date'] = staff_activity.date  # Assuming `date` is a field in StaffCosGuidelinesActivities
            activity['remarks'] = staff_activity.remarks  # Assuming `remarks` is a field in StaffCosGuidelinesActivities

    return JsonResponse({
        'lib_cos_guidelines_activities': activities_data
    }, status=200)

@csrf_exempt
def PostLibCostGuideLinesActivities(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)  # Deserialize JSON data
            
            # If your data has a `data` key as in the JavaScript payload
            activities = data.get('data', [])

            for activity in activities:
                staff = NewlyHiredStaff.objects.get(id=activity.get('user_id'))  # Fetch the staff object
                lib_cost_guidelines_activity = LibCosGuidelinesActivities.objects.get(id=activity.get('id'))  # Get the LibNeopActivities object
                StaffCosGuidelinesActivities.objects.update_or_create(
                    staff_id=staff,
                    lib_cos_guidelines_id=lib_cost_guidelines_activity,
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
def PostCosGuideLinesStaffInfo(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body)

        # Extract data
        staff_id = data.get('data', {}).get('staff_id')
        assumption_date = data.get('data', {}).get('assumption_date')
        requirements_submission_date = data.get('data', {}).get('requirements_submission_date')
        ccef_submission_date = data.get('data', {}).get('ccef_submission_date')
        agency_orientation = data.get('data', {}).get('agency_orientation')

        # Helper function to safely parse date strings
        def parse_date(date_str):
            if date_str:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            return None

        # Safely convert the date strings to date objects
        assumption_date = parse_date(assumption_date)
        requirements_submission_date = parse_date(requirements_submission_date)
        ccef_submission_date = parse_date(ccef_submission_date)
        agency_orientation = parse_date(agency_orientation)

        # Get the staff instance
        try:
            staff = NewlyHiredStaff.objects.get(id=staff_id)
        except NewlyHiredStaff.DoesNotExist:
            return JsonResponse({"error": "Staff not found"}, status=404)

        # Check if StaffCosGuidelinesInfo exists for the given staff
        staff_cost_guidelines_info, created = StaffCosGuidelinesInfo.objects.update_or_create(
            staff_id=staff,  # Use staff instance for the foreign key
            defaults={
                'assumption_date': assumption_date,
                'requirements_submission_date': requirements_submission_date,
                'ccef_submission_date': ccef_submission_date,
                'agency_orientation': agency_orientation,
            }
        )

        # Return success response
        if created:
            message = "Staff Cost with Guidelines Info created successfully"
        else:
            message = "Staff Cost with Guidelines Info updated successfully"

        return JsonResponse({"message": message}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)