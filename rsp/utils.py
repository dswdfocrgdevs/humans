from .models import NewlyHiredStaff

def search_employees(query):
    """
    Function to search employees based on the query.
    Returns a list of employees matching the query.
    """
    if query:
        # Filter the employees based on the query
        employees = NewlyHiredStaff.objects.filter(full_name__icontains=query)
    else:
        employees = NewlyHiredStaff.objects.all()

    # Prepare the employee data to return
    employee_data = list(employees.values('id', 'full_name', 'position'))
    return employee_data
