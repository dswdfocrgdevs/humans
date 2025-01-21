from django.core.management.base import BaseCommand
from rsp.models import RspHiredStreamlinereq

class Command(BaseCommand):
    help = 'Seeds rsp_hired_requirements_streamline table with sample data'

    def handle(self, *args, **kwargs):
        data = [
            (1, 'Transcript of Record', 1, 1, 1, 1),
            (2, 'Personal Data Sheet', 1, 1, 1, 1),
            (3, 'Work Experience Sheet', 1, 1, 1, 1),
            (4, 'Relevant Trainings', 1, 1, 1, 1),
            (5, 'Transcript of Record', 2, 1, 1, 1),
            (6, 'Personal Data Sheet', 2, 1, 1, 1),
            (7, 'Work Experience Sheet', 2, 1, 1, 1),
            (8, 'Relevant Trainings', 2, 1, 1, 1),
            (9, 'Transcript of Record', 3, 1, 1, 1),
            (10, 'Personal Data Sheet', 3, 1, 1, 1),
            (11, 'Work Experience Sheet', 3, 1, 1, 1),
            (12, 'Relevant Trainings', 3, 1, 1, 1),
            (13, 'Transcript of Record', 4, 1, 1, 1),
            (14, 'Personal Data Sheet', 4, 1, 1, 1),
            (15, 'Work Experience Sheet', 4, 1, 1, 1),
            (16, 'Relevant Trainings', 4, 1, 1, 1),
            (17, 'Transcript of Record', 5, 1, 1, 1),
            (18, 'Personal Data Sheet', 5, 1, 1, 1),
            (19, 'Work Experience Sheet', 5, 1, 1, 1),
            (20, 'Relevant Trainings', 5, 1, 1, 1),
            (21, 'Transcript of Record', 6, 1, 1, 1),
            (22, 'Personal Data Sheet', 6, 1, 1, 1),
            (23, 'Work Experience Sheet', 6, 1, 1, 1),
            (24, 'Relevant Trainings', 6, 1, 1, 1),
        ]
        
        for item in data:
            RspHiredStreamlinereq.objects.create(
                id=item[0],
                name=item[1],
                is_required=bool(item[2]),
                status=bool(item[3]),
                empstatus_id=item[4],
                upload_by_id=item[5]
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded rsp_hired_requirements_streamline table'))
