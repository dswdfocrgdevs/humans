from django.db import connection

# Decode bytes if necessary and handle null cases
def safe_decode(value):
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value


def check_endorsement_activities_exist(endorsed, staff_id):
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



def check_neop_activities_exist(milestone, staff_id):
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

    return {
        'all_activities_exist': True if result and result[0] == 'TRUE' else False,
        'progress': safe_decode(result[1]) if result and result[1] else '0/0'  # Decode and default to '0/0'
    }


def check_cos_activities_exist(staff_id):
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
        'progress': safe_decode(result[1]) if result else '0/0'  # Default to '0/0' if no result
    }