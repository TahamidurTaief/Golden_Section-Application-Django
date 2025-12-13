import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoldenSection.settings')
django.setup()

from quotations.models import ServiceRequest

print("=" * 60)
print("DATABASE STATUS - SERVICE REQUESTS")
print("=" * 60)

requests = ServiceRequest.objects.all().order_by('-created_at')
print(f"\n✅ TOTAL REQUESTS IN DATABASE: {requests.count()}\n")

if requests.exists():
    print("Recent Requests:")
    print("-" * 60)
    for r in requests[:5]:
        print(f"\nID: {r.id}")
        print(f"Customer: {r.customer_name}")
        print(f"Email: {r.email}")
        print(f"Phone: {r.phone}")
        print(f"Service: {r.service.name}")
        print(f"Booking Date: {r.booking_datetime}")
        print(f"Total Amount: £{r.total_amount}")
        print(f"Status: {r.status}")
        print(f"Created: {r.created_at}")
        print("-" * 60)
else:
    print("❌ No requests found in database")

print("\n✅ Data IS being saved to the database!")
print("If you don't see your request, check:")
print("1. Are you submitting the form correctly?")
print("2. Check browser console for errors (F12)")
print("3. Are you looking at the right database?")
