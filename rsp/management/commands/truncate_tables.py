from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Truncate all tables in the database."

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  # Disable foreign key checks
            tables = connection.introspection.table_names()
            for table in tables:
                cursor.execute(f"TRUNCATE TABLE `{table}`;")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  # Re-enable foreign key checks
        self.stdout.write(self.style.SUCCESS("All tables truncated successfully!"))
