import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from properties.models import Property
from tenants.models import Tenant
from leases.models import Lease
from maintenance.models import MaintenanceRequest
from documents.models import Document, Folder
from users.models import User

print("=" * 70)
print("DATABASE CHECK - SUPABASE CONNECTION")
print("=" * 70)

# Check connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✓ PostgreSQL Version: {version[0]}")
        print(f"✓ Database: {connection.settings_dict['NAME']}")
        print(f"✓ Host: {connection.settings_dict['HOST']}")
        print()
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    exit(1)

# Check tables and counts
print("TABLE COUNTS:")
print("-" * 70)

models = [
    ('Users', User),
    ('Properties', Property),
    ('Tenants', Tenant),
    ('Leases', Lease),
    ('Maintenance Requests', MaintenanceRequest),
    ('Documents', Document),
    ('Folders', Folder),
]

for name, model in models:
    try:
        count = model.objects.count()
        print(f"{name:.<30} {count:>5} records")
    except Exception as e:
        print(f"{name:.<30} ERROR: {str(e)[:30]}")

print()
print("=" * 70)
print("SAMPLE DATA")
print("=" * 70)

# Show sample users
print("\nUSERS:")
for user in User.objects.all()[:5]:
    superadmin = "🔑 SUPERADMIN" if user.is_superadmin else ""
    print(f"  - {user.email} ({user.first_name} {user.last_name}) {superadmin}")

# Show sample properties
print("\nPROPERTIES:")
if Property.objects.exists():
    for prop in Property.objects.all()[:5]:
        print(f"  - {prop.name} | {prop.city} | {prop.total_units} units | Occupancy: {prop.occupancy_rate}%")
else:
    print("  ⚠ No properties found - add properties via the UI")

# Show sample tenants
print("\nTENANTS:")
if Tenant.objects.exists():
    for tenant in Tenant.objects.all()[:5]:
        print(f"  - {tenant.first_name} {tenant.last_name} | {tenant.email} | Status: {tenant.status}")
else:
    print("  ⚠ No tenants found - add tenants via the UI")

# Show sample leases
print("\nLEASES:")
if Lease.objects.exists():
    for lease in Lease.objects.all()[:5]:
        tenant_name = f"{lease.tenant.first_name} {lease.tenant.last_name}" if lease.tenant else "N/A"
        prop_name = lease.lease_property.name if lease.lease_property else "N/A"
        print(f"  - {tenant_name} @ {prop_name} | Status: {lease.status} | Rent: ${lease.monthly_rent}")
else:
    print("  ⚠ No leases found - add leases via the UI")

print()
print("=" * 70)
print("DATABASE CHECK COMPLETE")
print("=" * 70)
