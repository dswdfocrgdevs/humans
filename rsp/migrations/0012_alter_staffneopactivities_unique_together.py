# Generated by Django 4.2.16 on 2024-12-18 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsp', '0011_remove_staffneopactivities_date_completed'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='staffneopactivities',
            unique_together=set(),
        ),
    ]
