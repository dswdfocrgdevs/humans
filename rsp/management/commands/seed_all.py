from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Run all custom commands sequentially"

    def handle(self, *args, **kwargs):
        commands = [
            'seed_cos_guidlines_activities', 
            'seed_neop_activities',          
        ]

        for command in commands:
            self.stdout.write(self.style.NOTICE(f"Running: {command}"))
            try:
                call_command(command)
                self.stdout.write(self.style.SUCCESS(f"Successfully ran: {command}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error running {command}: {e}"))