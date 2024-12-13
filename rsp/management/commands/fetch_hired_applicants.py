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
            # url = f'{base_url}?page={page}'
            # response = requests.get(url, headers=headers)
            response = requests.get(base_url, headers=headers, params={'page': page})
            
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f'Error: Unable to fetch data from page {page}'))
                break

            # Parse the data returned by the API
            data = response.json()

            if not data['results']:  # Check if there are no results in the current page
                self.stdout.write(self.style.SUCCESS(f'No more data found, stopping at page {page}'))
                break

            # Store the data in the database
            for item in data['results']:
                # Save each applicant to the database
                NewlyHiredStaff.objects.create(
                    requirements_ok=item.get('requirements_ok',''),
                    full_name=item.get('full_name', ''),
                    position=item.get('position', ''),
                    area_of_assignment=item.get('area_of_assignment', ''),
                    former_incumbent=item.get('former_incumbent', ''),
                    salary=item.get('salary', 0),
                    effectivity_of_contract=item.get('effectivity_of_contract'),
                    end_of_contract=item.get('end_of_contract'),
                    emp_status=item.get('emp_status', ''),
                    nature=item.get('nature', ''),
                    remarks=item.get('remarks', ''),
                )
                print()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully fetched and stored data from page {page}'))

            page += 1  # Move to the next page