from django.db import models

# Create your models here.


from django.db import models

from django.db import models

class NewlyHiredStaff(models.Model):
    requirements_ok = models.CharField(max_length=100,default=False,null=True)  # True if requirements are met
    full_name = models.CharField(max_length=255,null=True)  # Full name of the staff
    position = models.CharField(max_length=100,null=True)  # Job position
    area_of_assignment = models.CharField(max_length=100,null=True)  # Work location
    former_incumbent = models.CharField(max_length=255, blank=True, null=True)  # Name of previous holder of the position
    salary = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # Salary amount
    effectivity_of_contract = models.CharField(max_length=100, null=True)  # Start date of the contract
    end_of_contract = models.CharField(max_length=100, null=True)  # End date of the contract
    emp_status = models.CharField(max_length=100, null=True)
    nature = models.CharField(max_length=100,null=True)  # Nature of employment (e.g., permanent, temporary)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically update on save
    remarks = models.TextField(null=True)

    def __str__(self):
        return f"{self.full_name} - {self.position}"
