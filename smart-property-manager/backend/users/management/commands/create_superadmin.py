from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Role

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superadmin user'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email address')
        parser.add_argument('--password', type=str, help='Password')
        parser.add_argument('--first-name', type=str, help='First name')
        parser.add_argument('--last-name', type=str, help='Last name')

    def handle(self, *args, **options):
        email = options.get('email') or 'admin@smartproperty.com'
        password = options.get('password') or 'admin123456'
        first_name = options.get('first_name') or 'Super'
        last_name = options.get('last_name') or 'Admin'

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'User with email {email} already exists!'))
            return

        # Get or create admin role
        admin_role, created = Role.objects.get_or_create(
            name='admin',
            defaults={
                'description': 'Administrator with full system access',
                'can_create_properties': True,
                'can_edit_properties': True,
                'can_delete_properties': True,
                'can_manage_tenants': True,
                'can_manage_leases': True,
                'can_manage_financials': True,
                'can_manage_users': True,
                'can_view_analytics': True,
                'can_export_reports': True,
            }
        )

        # Create superadmin user
        user = User.objects.create_user(
            email=email,
            username=email.split('@')[0],
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=admin_role,
            is_superadmin=True,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS(
            f'\nSuperadmin user created successfully!\n'
            f'Email: {email}\n'
            f'Password: {password}\n'
            f'Please change the password after first login.\n'
        ))
