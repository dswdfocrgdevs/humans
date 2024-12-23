# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('KtAuthCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class KtAuthCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    employee_id = models.CharField(max_length=255, blank=True, null=True)
    id_number = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    division = models.CharField(max_length=255, blank=True, null=True)
    section = models.CharField(max_length=255, blank=True, null=True)
    area_of_assignment = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kt_auth_customuser'


class KtAuthCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(KtAuthCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kt_auth_customuser_groups'
        unique_together = (('customuser', 'group'),)


class KtAuthCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(KtAuthCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'kt_auth_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class RspFormType(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rsp_form_type'


class RspNewlyhiredstaff(models.Model):
    id = models.BigAutoField(primary_key=True)
    requirements_ok = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    area_of_assignment = models.CharField(max_length=100, blank=True, null=True)
    former_incumbent = models.CharField(max_length=255, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    effectivity_of_contract = models.CharField(max_length=100, blank=True, null=True)
    end_of_contract = models.CharField(max_length=100, blank=True, null=True)
    emp_status = models.CharField(max_length=100, blank=True, null=True)
    nature = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rsp_newlyhiredstaff'


class RspOnboardingLayout(models.Model):
    form_type_id = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rsp_onboarding_layout'
