"""
Test script for new service request functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoldenSection.settings')
django.setup()

from services.models import Service
from quotations.models import ServiceRequest

print("=" * 60)
print("TESTING SERVICE REQUEST SETUP")
print("=" * 60)

# Check if services exist
services = Service.objects.all()
print(f"\n✓ Total Services: {services.count()}")
if services.exists():
    for service in services[:3]:
        print(f"  - {service.name} (ID: {service.id})")

# Check service requests
requests = ServiceRequest.objects.all()
print(f"\n✓ Total Service Requests: {requests.count()}")
if requests.exists():
    latest = requests.first()
    print(f"\n  Latest Request:")
    print(f"  - ID: {latest.id}")
    print(f"  - Customer: {latest.customer_name}")
    print(f"  - Service: {latest.service.name}")
    print(f"  - Status: {latest.get_status_display()}")
    if latest.booking_date:
        print(f"  - Booking Date: {latest.booking_date}")
    if latest.booking_time:
        print(f"  - Booking Time: {latest.booking_time}")
    if latest.location_address:
        print(f"  - Location: {latest.location_address[:50]}...")

# Check model fields
print("\n✓ ServiceRequest Model Fields:")
for field in ServiceRequest._meta.get_fields():
    if not field.many_to_many and not field.one_to_many:
        print(f"  - {field.name}: {field.get_internal_type()}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
