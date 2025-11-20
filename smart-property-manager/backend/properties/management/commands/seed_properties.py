from django.core.management.base import BaseCommand
from properties.models import Property, Owner
from users.models import User


class Command(BaseCommand):
    help = 'Seed demo properties matching Figma design'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding properties...')

        # Get or create default owner
        owner, created = Owner.objects.get_or_create(
            email='investor@realestate.com',
            defaults={
                'name': 'Real Estate Investments LLC',
                'phone': '555-0123',
                'address': '123 Investment Blvd, Financial District'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created owner: {owner.name}'))

        # Get admin user for created_by field
        admin_user = User.objects.filter(is_superuser=True).first()

        # Create Sunset Apartments (from Figma)
        sunset, created = Property.objects.get_or_create(
            name='Sunset Apartments',
            defaults={
                'property_type': 'residential',
                'status': 'active',
                'address': '456 Sunset Boulevard',
                'city': 'Downtown District',
                'state': 'CA',
                'zip_code': '90001',
                'total_units': 24,
                'occupied_units': 23,  # 95% occupied
                'size_sqft': 18000,
                'year_built': 2015,
                'purchase_price': 3200000,
                'current_value': 3200000,
                'monthly_revenue': 48000,
                'monthly_expenses': 12000,
                'owner': owner,
                'description': 'Modern residential complex in prime downtown location',
                'created_by': admin_user
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created: {sunset.name} - {sunset.occupancy_rate}% Occupied, ROI: {sunset.roi}%'))

        # Create Oak Street Complex (from Figma)
        oak, created = Property.objects.get_or_create(
            name='Oak Street Complex',
            defaults={
                'property_type': 'residential',
                'status': 'active',
                'address': '789 Oak Street',
                'city': 'Midtown',
                'state': 'CA',
                'zip_code': '90002',
                'total_units': 18,
                'occupied_units': 16,  # 87% occupied
                'size_sqft': 15000,
                'year_built': 2018,
                'purchase_price': 2100000,
                'current_value': 2100000,
                'monthly_revenue': 32400,
                'monthly_expenses': 9000,
                'owner': owner,
                'description': 'Well-maintained residential units in growing neighborhood',
                'created_by': admin_user
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created: {oak.name} - {oak.occupancy_rate}% Occupied, ROI: {oak.roi}%'))

        # Create Downtown Plaza (from Figma)
        plaza, created = Property.objects.get_or_create(
            name='Downtown Plaza',
            defaults={
                'property_type': 'commercial',
                'status': 'active',
                'address': '321 Main Street',
                'city': 'Financial District',
                'state': 'CA',
                'zip_code': '90003',
                'total_units': 36,
                'occupied_units': 36,  # 100% occupied
                'size_sqft': 45000,
                'year_built': 2020,
                'purchase_price': 5800000,
                'current_value': 5800000,
                'monthly_revenue': 72000,
                'monthly_expenses': 18000,
                'owner': owner,
                'description': 'Premium commercial space in heart of financial district',
                'created_by': admin_user
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created: {plaza.name} - {plaza.occupancy_rate}% Occupied, ROI: {plaza.roi}%'))

        self.stdout.write(self.style.SUCCESS('\nProperties seeded successfully!'))
        self.stdout.write(f'Total Properties: {Property.objects.count()}')
        self.stdout.write(f'Total Value: ${sum(p.current_value for p in Property.objects.all()):,.0f}')
