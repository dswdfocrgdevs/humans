# your_app/management/commands/seed_onboarding_status.py
from django.core.management.base import BaseCommand
from rsp.models import OnboardingStatus

class Command(BaseCommand):
    help = 'Seed Onboarding Statuses into the database'

    def handle(self, *args, **kwargs):
        # Define the onboarding statuses and their respective status values
        statuses = [
            {'name': 'NEOP', 'status': 1},
            {'name': 'COS with Guidelines', 'status': 1},
            {'name': 'Internal Staff', 'status': 1},
        ]
        
        # Iterate over the statuses and create OnboardingStatus objects
        for status_data in statuses:
            onboarding_status, created = OnboardingStatus.objects.get_or_create(
                name=status_data['name'],
                status=status_data['status'],
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully created {onboarding_status.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"{onboarding_status.name} already exists"))
