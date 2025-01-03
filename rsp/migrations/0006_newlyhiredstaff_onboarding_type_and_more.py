# Generated by Django 4.2.16 on 2024-12-26 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rsp', '0005_rename_lib_neop_id_staffcosguidelinesactivities_lib_cos_guidelines_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='newlyhiredstaff',
            name='onboarding_type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='newlyhiredstaff',
            name='picture',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='staffcosguidelinesactivities',
            name='lib_cos_guidelines_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_cos_activities', to='rsp.libcosguidelinesactivities'),
        ),
    ]
