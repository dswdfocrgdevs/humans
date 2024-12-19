# Generated by Django 4.2.16 on 2024-12-18 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsp', '0007_newlyhiredstaff_remarks'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibNeopActivities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('milestone', models.PositiveSmallIntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
