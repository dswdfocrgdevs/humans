# Generated by Django 5.1.4 on 2024-12-12 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsp', '0002_newlyhiredstaff_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newlyhiredstaff',
            name='effectivity_of_contract',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='newlyhiredstaff',
            name='end_of_contract',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='newlyhiredstaff',
            name='requirements_ok',
            field=models.CharField(default=False, max_length=100, null=True),
        ),
    ]