import requests
from django.core.management.base import BaseCommand
from rsp.models import NewlyHiredStaff
import os

class Command(BaseCommand):
    help = 'Fetch and store hired applicants from the external API'

    def handle(self, *args, **kwargs):
        base_url = os.getenv("IRIS_API_NEWLY_HIRED")
        iris_token = os.getenv("IRIS_API_TOKEN")
        headers = {"Authorization": "Token " + iris_token}

        page = 1
        while True:
            # Fetch data from the API
            response = requests.get(base_url, headers=headers, params={'page': page})

            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f'Error: Unable to fetch data from page {page}'))
                break

            # Parse the data returned by the API
            data = response.json()

            if not data['results']:  # Check if there are no results in the current page
                self.stdout.write(self.style.SUCCESS(f'No more data found, stopping at page {page}'))
                break

            # Store or update the data in the database
            for item in data['results']:
                # Update or create each applicant
                obj, created = NewlyHiredStaff.objects.update_or_create(
                    iris_id=item.get('id'),
                    app_id=item.get('app_id'),
                    defaults={
                        'requirements_ok': item.get('requirements_ok', ''),
                        'full_name': item.get('full_name', ''),
                        'first_name': item.get('first_name', ''),
                        'middle_name': item.get('middle_name', ''),
                        'last_name': item.get('last_name', ''),
                        'position': item.get('position', ''),
                        'area_of_assignment': item.get('area_of_assignment', ''),
                        'former_incumbent': item.get('former_incumbent', ''),
                        'salary': item.get('salary', 0),
                        'salary_grade': item.get('salary_grade', 0),
                        'effectivity_of_contract': item.get('effectivity_of_contract'),
                        'end_of_contract': item.get('end_of_contract'),
                        'created_at': item.get('created_at'),
                        'updated_at': item.get('updated_at'),
                        'emp_status': item.get('emp_status', ''),
                        'fundsource': item.get('fundsource', ''),
                        'program': item.get('program', ''),
                        'nature': item.get('nature', ''),
                        'remarks': item.get('remarks', ''),
                        'picture': item.get('picture', ''),
                        'gender': item.get('gender', ''),
                        'contact_no': item.get('contact_no', ''),
                        'email': item.get('email', ''),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new entry: {item.get("full_name", "")}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated entry: {item.get("full_name", "")}'))

            self.stdout.write(self.style.SUCCESS(f'Successfully fetched and processed data from page {page}'))

            page += 1  # Move to the next page
