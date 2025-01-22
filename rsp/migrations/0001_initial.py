# Generated by Django 4.2.16 on 2025-01-21 07:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EndorsementActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('endorsed', models.PositiveSmallIntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LibCosGuidelinesActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('is_email_notify', models.BooleanField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LibNeopActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('milestone', models.PositiveSmallIntegerField(null=True)),
                ('is_email_notify', models.BooleanField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewlyHiredStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iris_id', models.IntegerField(null=True)),
                ('app_id', models.IntegerField(null=True)),
                ('requirements_ok', models.CharField(default=False, max_length=100, null=True)),
                ('full_name', models.CharField(max_length=255, null=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('middle_name', models.CharField(max_length=255, null=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('position', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('age', models.CharField(max_length=100, null=True)),
                ('dob', models.CharField(max_length=100, null=True)),
                ('area_of_assignment', models.CharField(max_length=100, null=True)),
                ('former_incumbent', models.CharField(blank=True, max_length=255, null=True)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('salary_grade', models.CharField(max_length=100, null=True)),
                ('effectivity_of_contract', models.CharField(max_length=100, null=True)),
                ('end_of_contract', models.CharField(max_length=100, null=True)),
                ('emp_status', models.CharField(max_length=100, null=True)),
                ('fundsource', models.CharField(max_length=100, null=True)),
                ('program', models.CharField(max_length=100, null=True)),
                ('nature', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', models.TextField(null=True)),
                ('picture', models.CharField(max_length=255, null=True)),
                ('gender', models.CharField(max_length=100, null=True)),
                ('contact_no', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewlyHiredStaffStreamline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iris_id', models.IntegerField(null=True)),
                ('app_id', models.IntegerField(null=True)),
                ('requirements_ok', models.CharField(default=False, max_length=100, null=True)),
                ('full_name', models.CharField(max_length=255, null=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('middle_name', models.CharField(max_length=255, null=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('position', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('age', models.CharField(max_length=100, null=True)),
                ('dob', models.CharField(max_length=100, null=True)),
                ('area_of_assignment', models.CharField(max_length=100, null=True)),
                ('former_incumbent', models.CharField(blank=True, max_length=255, null=True)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('salary_grade', models.CharField(max_length=100, null=True)),
                ('effectivity_of_contract', models.CharField(max_length=100, null=True)),
                ('end_of_contract', models.CharField(max_length=100, null=True)),
                ('emp_status', models.CharField(max_length=100, null=True)),
                ('fundsource', models.CharField(max_length=100, null=True)),
                ('program', models.CharField(max_length=100, null=True)),
                ('nature', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', models.TextField(null=True)),
                ('picture', models.CharField(max_length=100, null=True)),
                ('gender', models.CharField(max_length=100, null=True)),
                ('contact_no', models.CharField(max_length=100, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OnboardingStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('status', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RspEmpstatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('acronym', models.CharField(max_length=64, unique=True)),
                ('status', models.BooleanField()),
                ('order', models.BooleanField()),
                ('upload_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'rsp_empstatus',
            },
        ),
        migrations.CreateModel(
            name='RspFormType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'rsp_form_type',
            },
        ),
        migrations.CreateModel(
            name='StaffNeopInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assumption_date', models.DateField(blank=True, null=True)),
                ('date_end_third', models.DateField(blank=True, null=True)),
                ('date_end_sixth', models.DateField(blank=True, null=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='neop_info_activities', to='rsp.newlyhiredstaff')),
            ],
        ),
        migrations.CreateModel(
            name='StaffNeopActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('lib_neop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_activities', to='rsp.libneopactivities')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='neop_activities', to='rsp.newlyhiredstaff')),
            ],
        ),
        migrations.CreateModel(
            name='StaffEndorsementActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('lib_endorsed_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rsp.endorsementactivities')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rsp.newlyhiredstaff')),
            ],
        ),
        migrations.CreateModel(
            name='StaffCosGuidelinesInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assumption_date', models.DateField(blank=True, null=True)),
                ('requirements_submission_date', models.DateField(blank=True, null=True)),
                ('ccef_submission_date', models.DateField(blank=True, null=True)),
                ('agency_orientation', models.DateField(blank=True, null=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cos_guidelines_info_activities', to='rsp.newlyhiredstaff')),
            ],
        ),
        migrations.CreateModel(
            name='StaffCosGuidelinesActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('lib_cos_guidelines_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_cos_activities', to='rsp.libcosguidelinesactivities')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cos_activities', to='rsp.newlyhiredstaff')),
            ],
        ),
        migrations.CreateModel(
            name='RspOnboardingLayout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('form_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rsp.rspformtype')),
            ],
            options={
                'db_table': 'rsp_onboarding_layout',
            },
        ),
        migrations.CreateModel(
            name='RspHiredStreamlinereq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_required', models.BooleanField()),
                ('status', models.BooleanField()),
                ('empstatus', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rsp.rspempstatus')),
                ('upload_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'rsp_hired_requirements_streamline',
            },
        ),
        migrations.CreateModel(
            name='RspHiredreq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_required', models.BooleanField()),
                ('status', models.BooleanField()),
                ('empstatus', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rsp.rspempstatus')),
                ('upload_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'rsp_hired_requirements',
            },
        ),
        migrations.CreateModel(
            name='OnboardingStatusNewlyhired',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rsp.newlyhiredstaff')),
                ('onboarding_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rsp.onboardingstatus')),
            ],
        ),
        migrations.AddField(
            model_name='newlyhiredstaff',
            name='onboarding_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rsp.onboardingstatus'),
        ),
        migrations.CreateModel(
            name='HiredreqCompliance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.IntegerField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=255, null=True)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('hired_req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rsp.rsphiredreq')),
            ],
            options={
                'db_table': 'rsp_hiredreq_compliance',
            },
        ),
    ]
