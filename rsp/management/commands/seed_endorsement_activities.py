from django.core.management.base import BaseCommand
from django.db import connection
from rsp.models import EndorsementActivities

class Command(BaseCommand):
    help = "Seeds the database with predefined EndorsementActivities."

    def handle(self, *args, **kwargs):
        # Truncate the table and reset the auto-incrementing ID
        EndorsementActivities.objects.all().delete()
        
        # Reset the auto-increment value to 1 for MySQL
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE rsp_endorsementactivities AUTO_INCREMENT = 1;")
        
        activities = [
            {"name": "Welcome Banner", "endorsed": 1},
            {"name": "Congratulatory Banner", "endorsed": 1},
            {"name": "SWEAP Membership", "endorsed": 1},

            {"name": "Agency Orientation", "endorsed": 2},
            {"name": "Monitoring of LDI", "endorsed": 2},
            {"name": "For IDP", "endorsed": 2},

            {"name": "Probationary Staff", "endorsed": 3},
            {"name": "Monitoring of DSPMS Submission", "endorsed": 3},
            {"name": "SWEAP Membership", "endorsed": 3},

            {"name": "Creation of MyPORTAL ID and Biometrics", "endorsed": 4},
            {"name": "For Payroll","endorsed":4},
            {"name": "Transmit 201 Files", "endorsed": 4},
        ]

        for activity in activities:
            EndorsementActivities.objects.get_or_create(
                name=activity["name"],
                description=activity["name"],  # description is same as name
                endorsed=activity["endorsed"]
            )
            self.stdout.write(self.style.SUCCESS(f"Seeded activity: {activity['name']}"))

        self.stdout.write(self.style.SUCCESS("Successfully seeded all activities."))
