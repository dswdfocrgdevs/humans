# Generated by Django 4.2.16 on 2025-01-02 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsp', '0006_newlyhiredstaff_onboarding_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newlyhiredstaff',
            name='iris_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='newlyhiredstaffstreamline',
            name='iris_id',
            field=models.IntegerField(null=True),
        ),
    ]
