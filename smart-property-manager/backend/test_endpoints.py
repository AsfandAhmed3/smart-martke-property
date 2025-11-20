"""
Test script to verify backend endpoints are working
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from properties.models import Property
from tenants.models import Tenant
from leases.models import Lease
from maintenance.models import MaintenanceRequest

print("\n=== Database Records ===")
print(f"Users: {User.objects.count()}")
print(f"Properties: {Property.objects.count()}")
print(f"Tenants: {Tenant.objects.count()}")
print(f"Leases: {Lease.objects.count()}")
print(f"Maintenance Requests: {MaintenanceRequest.objects.count()}")

print("\n=== Sample Users ===")
for user in User.objects.all()[:5]:
    print(f"  - {user.email} (Superadmin: {user.is_superadmin})")

print("\n=== Testing Auth ===")
# Test if superadmin exists
superadmin = User.objects.filter(is_superadmin=True).first()
if superadmin:
    print(f"✓ Superadmin found: {superadmin.email}")
else:
    print("✗ No superadmin found")

print("\n=== Testing Endpoints ===")
print("Backend should be running on: http://127.0.0.1:8000")
print("Try these endpoints:")
print("  POST http://127.0.0.1:8000/api/auth/login/")
print("  GET  http://127.0.0.1:8000/api/auth/admin/users/")
print("  GET  http://127.0.0.1:8000/api/maintenance/")
print("  GET  http://127.0.0.1:8000/api/documents/")
