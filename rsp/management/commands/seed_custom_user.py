from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from kt_auth.models import CustomUser  # Import your CustomUser model

class Command(BaseCommand):
    help = 'Seeds the CustomUser table with an admin user'

    def handle(self, *args, **kwargs):
        # Create an admin user
        admin_user = CustomUser.objects.create(
            username='admin',  # Admin username
            password='password',  # Admin password (you should use a secure method to hash it)
            employee_id='EMP001',
            id_number='ID123456',
            middle_name='Admin',
            contact='1234567890',
            account_number='ACC12345',
            position='System Administrator',
            division='IT Department',
            section='Administration',
            area_of_assignment='Headquarters',
            gender='Male',
            birthdate='1980-01-01',
            image_path='path/to/image.png',
            status='Active'
        )
        
        # Set user as admin
        admin_user.is_staff = True  # Make the user a staff member (admin privileges)
        admin_user.is_superuser = True  # Grant superuser privileges
        admin_user.save()

        # Optionally, add the user to an admin group if needed
        # admin_group, created = Group.objects.get_or_create(name='Admin')
        # admin_user.groups.add(admin_group)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the admin user in the CustomUser table'))
