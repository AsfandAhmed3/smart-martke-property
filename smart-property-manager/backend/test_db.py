import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from users.models import User

print("=" * 60)
print("SUPABASE DATABASE CONNECTION TEST")
print("=" * 60)

# Test connection
try:
    connection.ensure_connection()
    print(f"✓ Connected to: {connection.settings_dict['HOST']}")
    print(f"✓ Database: {connection.settings_dict['NAME']}")
    print(f"✓ User: {connection.settings_dict['USER']}")
    print()
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit(1)

# Check users
try:
    users = User.objects.all()
    print(f"Total users in database: {users.count()}")
    print()
    
    if users.exists():
        print("Users:")
        for user in users:
            superadmin_badge = "🔑 SUPERADMIN" if user.is_superadmin else ""
            print(f"  - {user.email} | {user.first_name} {user.last_name} {superadmin_badge}")
    else:
        print("No users found in database")
    
    print()
    
    # Check superadmins
    superadmins = User.objects.filter(is_superadmin=True)
    print(f"Superadmin users: {superadmins.count()}")
    for sa in superadmins:
        print(f"  ✓ {sa.email}")
    
except Exception as e:
    print(f"✗ Query failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("TEST COMPLETE")
print("=" * 60)
