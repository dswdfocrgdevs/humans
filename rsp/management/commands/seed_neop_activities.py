from django.core.management.base import BaseCommand
from django.db import connection
from rsp.models import LibNeopActivities

class Command(BaseCommand):
    help = "Seeds the database with predefined LibNeopActivities."

    def handle(self, *args, **kwargs):
        # Truncate the table and reset the auto-incrementing ID
        LibNeopActivities.objects.all().delete()
        
        # Reset the auto-increment value to 1 for MySQL
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE rsp_libneopactivities AUTO_INCREMENT = 1;")
        
        activities = [
            {"name": "Preparation of Congratulatory Letter", "milestone": 1},
            {"name": "Appointment and other CSC Documents", "milestone": 1},
            {"name": "Notify Newly Hired", "milestone": 1},
            {"name": "Date newly hired acknowledged email", "milestone": 1},
            {"name": "Notice of Newly Hired posted in MyPORTAL", "milestone": 1},
            {"name": "Notify Head of ODSU", "milestone": 1},
            {"name": "Immediate Supervisor", "milestone": 1},
            {"name": "Peer Buddy", "milestone": 1},
            {"name": "RICTMS for Email", "milestone": 1},
            {"name": "Administrative Division", "milestone": 1},
            {"name": "Prepare Welcome Letter", "milestone": 1},
            {"name": "Journey Checklist", "milestone": 1},
            {"name": "Program Evaluation Form", "milestone": 1},
            {"name": "HR Orientation Form", "milestone": 1},
            {"name": "Memo re: DSPMS", "milestone": 1},
            {"name": "Endorsement to PRAISE for Welcome Banner", "milestone": 1},
            {"name": "Prepare Intro Letter", "milestone": 1},
            {"name": "Endorsement to LDS for Agency Orientation", "milestone": 1},
            {"name": "Conduct of HR Orientation", "milestone": 1},
            {"name": "Provision of GoBag", "milestone": 1},
            {"name": "Signing of Appointment", "milestone": 1},
            {"name": "Endorse to PAS for Biometrics", "milestone": 1},
            {"name": "Endorse to PAS for Deductions", "milestone": 1},
            {"name": "Endorse to PAS Enrollment to GSIS etc.", "milestone": 1},
            {"name": "Submission of requirements", "milestone": 1},

            {"name": "Endorsment to ODSU", "milestone": 2},
            {"name": "Endorsment to PAS for Payroll Inclusion", "milestone": 2},
            {"name": "Submission of IPC (for Probationary)", "milestone": 2},

            {"name": "Submission of Requirements to CSC Validation", "milestone": 3},
            {"name": "Oath taking Ceremony", "milestone": 3},
            {"name": "Agency Orientation", "milestone": 3},
            {"name": "Endorsement to LDS for any in-house and agency-initiated LDI", "milestone": 3},

            {"name": "Remind staff and Immediate supervisor on submission of IPCR (for probationary)", "milestone": 4},
            {"name": "Revisitation of Journey Checklist","milestone":4},
            {"name": "Submission of 1st IPCR (First 3 months)", "milestone": 4},
            {"name": "Submission of 2nd IPCR (Last 3 months)", "milestone": 4},
            {"name": "Issuance if notice of termination", "milestone": 4},

            {"name": "Prepare Congratulatory Letter and Certificate of Completion", "milestone": 5},
            {"name": "Invite the Staff for onboarding Evaluation", "milestone": 5},
            {"name": "Collect the accomplished onboarding forms", "milestone": 5},
            {"name": "Endorse to Welfare for issuance of Congratulatory Banner", "milestone": 5},
        ]

        for activity in activities:
            LibNeopActivities.objects.get_or_create(
                name=activity["name"],
                description=activity["name"],  # description is same as name
                milestone=activity["milestone"]
            )
            self.stdout.write(self.style.SUCCESS(f"Seeded activity: {activity['name']}"))

        self.stdout.write(self.style.SUCCESS("Successfully seeded all activities."))
