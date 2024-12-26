from django.core.management.base import BaseCommand
from django.db import connection
from rsp.models import LibCosGuidelinesActivities

class Command(BaseCommand):
    help = "Seed LibCosGuidelinesActivities with default activities"

    def handle(self, *args, **options):
        activities = [
            "Notify Newly Hired",
            "Date Newly Hired acknowledged email",
            "Notify Head of ODSU",
            "Immediate Supervisor",
            "Peer Buddy",
            "RICTIMS for Official Email",
            "Administrative Division",
            "Endorsement to PRAISE for Welcome Banner",
            "Endorsement to LDS for Agency Orientation",
            "Notice of Appointment",
            "Prepare Job Offer",
            "Prepare Welcome Letter",
            "Prepare Intro Letter",
            "Prepare HR Orientation Guide",
            "Conduct of HR Orientation",
            "Signing of Contract",
            "Submission of Requirements",
            "Endorsement to PAS for Registration in MyPortal",
            "Endorsement to PAS for Biometric",
            "Endorsement to HR Welfare for SWEAP Membership",
            "Submission of Program Evaluation Form",
            "Submission of Assumption to Duty Form",
            "Submission of CCEF and Rating Guide",
            "Physically Endorse to ODSU",
            "Agency Orientation",
        ]

        for activity in activities:
            LibCosGuidelinesActivities.objects.get_or_create(
                name=activity,
                description=activity,
            )
        
        self.stdout.write(self.style.SUCCESS("Successfully seeded LibCosGuidelinesActivities"))