import json
from django.core.management.base import BaseCommand
from rsp.models import RspHiredreq

class Command(BaseCommand):
    help = 'Seed Hiredreq data from JSON file'

    def handle(self, *args, **kwargs):
        file_path = 'rsp/management/json/rsp_hired_requirements.json'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                records = data.get("RECORDS", [])
                for record in records:
                    RspHiredreq.objects.update_or_create(
                        id=record["id"],
                        defaults={
                            "name": record["name"],
                            "is_required": record["is_required"],
                            "status": record["status"],
                            "empstatus_id": record["empstatus_id"],
                            "upload_by_id": record["upload_by_id"],
                        }
                    )
                self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(records)} records."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
