#!/usr/bin/env python
"""Quick script to check if services exist in the database"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoldenSection.settings')
django.setup()

from services.models import Service

# Check services
services = Service.objects.all()
active_services = Service.objects.filter(is_active=True)

print("\n" + "="*60)
print("SERVICE DATABASE CHECK")
print("="*60)
print(f"Total Services: {services.count()}")
print(f"Active Services: {active_services.count()}")
print("="*60)

if services.exists():
    print("\nServices in database:")
    for service in services[:10]:  # Show first 10
        status = "✓ Active" if service.is_active else "✗ Inactive"
        print(f"  {status} | ID: {service.id} | {service.name}")
else:
    print("\n❌ NO SERVICES FOUND IN DATABASE!")
    print("\nTo fix this, you need to:")
    print("1. Go to Django admin: http://127.0.0.1:8000/admin/")
    print("2. Navigate to Services")
    print("3. Add at least one service")
    print("4. Make sure 'is_active' is checked")

print("\n" + "="*60 + "\n")
