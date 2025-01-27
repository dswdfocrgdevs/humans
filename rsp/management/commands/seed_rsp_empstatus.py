from django.core.management.base import BaseCommand
from rsp.models import RspEmpstatus  # Import the model for rsp_empstatus

class Command(BaseCommand):
    help = 'Seeds the rsp_empstatus table with initial data'

    def handle(self, *args, **kwargs):
        # Data to be inserted
        data = [
            (1, 'Job Order Savings', 'JO', 1, 1, 1),
            (2, 'Contractual', 'Contractual', 1, 1, 1),
            (3, 'Permanent', 'Permanent', 1,1, 1),
            (4, 'Regular Contractual', 'Regular-Contractual', 1, 1, 1),
            (5, 'COS with ATH', 'COS', 1, 1, 1),
            (6, 'COS Savings', 'Savings', 1,1, 1),
        ]

        # Insert the data into the database
        for row in data:
            RspEmpstatus.objects.create(
                id=row[0],
                name=row[1],
                acronym=row[2],
                status=row[3],
                upload_by_id=row[4],
                order=row[5]
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded rsp_empstatus table with data!'))
