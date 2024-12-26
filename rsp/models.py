from django.db import models
from kt_auth.models import CustomUser
# Create your models here.


from django.db import models

from django.db import models

class NewlyHiredStaff(models.Model):
    requirements_ok = models.CharField(max_length=100,default=False,null=True)  # True if requirements are met
    full_name = models.CharField(max_length=255,null=True)  # Full name of the staff
    first_name = models.CharField(max_length=255,null=True)
    middle_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    position = models.CharField(max_length=100,null=True)  # Job position
    address = models.CharField(max_length=100,null=True)
    age = models.CharField(max_length=100,null=True)
    dob = models.CharField(max_length=100,null=True)
    area_of_assignment = models.CharField(max_length=100,null=True)  # Work location
    former_incumbent = models.CharField(max_length=255, blank=True, null=True)  # Name of previous holder of the position
    salary = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # Salary amount
    salary_grade = models.CharField(max_length=100,null=True)
    effectivity_of_contract = models.CharField(max_length=100, null=True)  # Start date of the contract
    end_of_contract = models.CharField(max_length=100, null=True)  # End date of the contract
    emp_status = models.CharField(max_length=100, null=True)
    fundsource = models.CharField(max_length=100,null=True)
    program = models.CharField(max_length=100,null=True)
    nature = models.CharField(max_length=100,null=True)  # Nature of employment (e.g., permanent, temporary)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically update on save
    remarks = models.TextField(null=True)
    picture = models.CharField(max_length=255,null=True)
    onboarding_type = models.CharField(max_length=100,null=True)
    

    def __str__(self):
        return f"{self.full_name} - {self.position}"
    

class NewlyHiredStaffStreamline(models.Model):
    requirements_ok = models.CharField(max_length=100,default=False,null=True)  # True if requirements are met
    full_name = models.CharField(max_length=255,null=True)  # Full name of the staff
    first_name = models.CharField(max_length=255,null=True)
    middle_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    position = models.CharField(max_length=100,null=True)  # Job position
    address = models.CharField(max_length=100,null=True)
    age = models.CharField(max_length=100,null=True)
    dob = models.CharField(max_length=100,null=True)
    area_of_assignment = models.CharField(max_length=100,null=True)  # Work location
    former_incumbent = models.CharField(max_length=255, blank=True, null=True)  # Name of previous holder of the position
    salary = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # Salary amount
    salary_grade = models.CharField(max_length=100,null=True)
    effectivity_of_contract = models.CharField(max_length=100, null=True)  # Start date of the contract
    end_of_contract = models.CharField(max_length=100, null=True)  # End date of the contract
    emp_status = models.CharField(max_length=100, null=True)
    fundsource = models.CharField(max_length=100,null=True)
    program = models.CharField(max_length=100,null=True)
    nature = models.CharField(max_length=100,null=True)  # Nature of employment (e.g., permanent, temporary)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically update on save
    remarks = models.TextField(null=True)
    picture = models.CharField(max_length=120,null=True)
    

    def __str__(self):
        return f"{self.full_name} - {self.position}"
    


class RspFormType(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'rsp_form_type'


class RspOnboardingLayout(models.Model):
    form_type = models.ForeignKey(RspFormType, models.DO_NOTHING)
    content = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'rsp_onboarding_layout'


class RspEmpstatus(models.Model):
    name = models.CharField(max_length=64, unique=True)
    acronym = models.CharField(max_length=64, unique=True)
    status = models.BooleanField()
    upload_by = models.ForeignKey(CustomUser, models.DO_NOTHING)
    order = models.BooleanField()

    def __str__(self):
        return self.name
        
    class Meta:
        db_table = 'rsp_empstatus'


class RspHiredreq(models.Model):
    name = models.CharField(max_length=255)
    empstatus =  models.ForeignKey(RspEmpstatus, models.DO_NOTHING)
    is_required = models.BooleanField()
    status = models.BooleanField()
    upload_by = models.ForeignKey(CustomUser, models.DO_NOTHING)

    class Meta:
        db_table = 'rsp_hired_requirements'


class RspHiredStreamlinereq(models.Model):
    name = models.CharField(max_length=255)
    empstatus =  models.ForeignKey(RspEmpstatus, models.DO_NOTHING)
    is_required = models.BooleanField()
    status = models.BooleanField()
    upload_by = models.ForeignKey(CustomUser, models.DO_NOTHING)

    class Meta:
        db_table = 'rsp_hired_requirements_streamline'


class LibNeopActivities(models.Model):
    name = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=255,null=True)
    milestone = models.PositiveSmallIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically update on save

class StaffNeopActivities(models.Model):
    staff_id = models.ForeignKey(NewlyHiredStaff, on_delete=models.CASCADE, related_name='neop_activities')
    lib_neop_id = models.ForeignKey(LibNeopActivities, on_delete=models.CASCADE, related_name='staff_activities')
    date = models.DateField(null=True)  # Field to store the date of the activity
    remarks = models.TextField(blank=True, null=True)  # Field to store additional remarks (optional)

    def __str__(self):
        return f'{self.staff_id.full_name} - {self.lib_neop_id.name}'

    # class Meta:
    #     unique_together = ('staff_id', 'lib_neop_id')  # Ensure a staff can't have duplicate activities

class StaffNeopInfo(models.Model):
    staff_id = models.ForeignKey(NewlyHiredStaff, on_delete=models.CASCADE, related_name='neop_info_activities')
    assumption_date = models.DateField(null=True, blank=True)
    date_end_third = models.DateField(null=True, blank=True)
    date_end_sixth = models.DateField(null=True, blank=True)


class LibCosGuidelinesActivities(models.Model):
    name = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically update on save

class StaffCosGuidelinesActivities(models.Model):
    staff_id = models.ForeignKey(NewlyHiredStaff, on_delete=models.CASCADE, related_name='cos_activities')
    lib_cos_guidelines_id = models.ForeignKey(LibCosGuidelinesActivities, on_delete=models.CASCADE, related_name='staff_cos_activities')
    date = models.DateField(null=True)  # Field to store the date of the activity
    remarks = models.TextField(blank=True, null=True)  # Field to store additional remarks (optional)

class StaffCosGuidelinesInfo(models.Model):
    staff_id = models.ForeignKey(NewlyHiredStaff, on_delete=models.CASCADE, related_name='cos_guidelines_info_activities')
    assumption_date = models.DateField(null=True, blank=True)
    requirements_submission_date = models.DateField(null=True, blank=True)
    ccef_submission_date = models.DateField(null=True, blank=True)
    agency_orientation = models.DateField(null=True, blank=True)

    
