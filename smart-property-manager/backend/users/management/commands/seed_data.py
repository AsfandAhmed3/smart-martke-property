from django.core.management.base import BaseCommand
from users.models import Role, User


class Command(BaseCommand):
    help = 'Seed initial roles and create demo superuser'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding roles...')

        # Create Admin Role
        admin_role, created = Role.objects.get_or_create(
            name=Role.ADMIN,
            defaults={
                'description': 'Full system access with all permissions',
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
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admin role'))

        # Create Portfolio Manager Role
        pm_role, created = Role.objects.get_or_create(
            name=Role.PORTFOLIO_MANAGER,
            defaults={
                'description': 'Manage properties, tenants, and leases',
                'can_create_properties': True,
                'can_edit_properties': True,
                'can_delete_properties': False,
                'can_manage_tenants': True,
                'can_manage_leases': True,
                'can_manage_financials': True,
                'can_manage_users': False,
                'can_view_analytics': True,
                'can_export_reports': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Portfolio Manager role'))

        # Create View Only Role
        vo_role, created = Role.objects.get_or_create(
            name=Role.VIEW_ONLY,
            defaults={
                'description': 'Read-only access to system data',
                'can_create_properties': False,
                'can_edit_properties': False,
                'can_delete_properties': False,
                'can_manage_tenants': False,
                'can_manage_leases': False,
                'can_manage_financials': False,
                'can_manage_users': False,
                'can_view_analytics': True,
                'can_export_reports': False,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created View Only role'))

        # Create demo superuser
        if not User.objects.filter(email='admin@smartproperty.com').exists():
            user = User.objects.create_superuser(
                username='admin',
                email='admin@smartproperty.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role=admin_role
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created superuser: {user.email} / admin123'
            ))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))

        # Create demo portfolio manager
        if not User.objects.filter(email='jack@gmail.com').exists():
            user = User.objects.create_user(
                username='jack',
                email='jack@gmail.com',
                password='password',
                first_name='Jack',
                last_name='Davis',
                role=pm_role
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created demo user: {user.email} / password'
            ))
        else:
            self.stdout.write(self.style.WARNING('Demo user already exists'))

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write('\nDemo credentials:')
        self.stdout.write('  Admin: admin@smartproperty.com / admin123')
        self.stdout.write('  User: jack@gmail.com / password')
