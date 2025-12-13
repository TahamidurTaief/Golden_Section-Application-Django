"""
Test script to verify ServiceRequest creation works correctly
"""
import os
import django
import sys
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoldenSection.settings')
django.setup()

from quotations.models import ServiceRequest
from services.models import Service

def test_service_request_creation():
    """Test creating a ServiceRequest"""
    try:
        # Get first service
        service = Service.objects.first()
        if not service:
            print("❌ No services found in database. Please create a service first.")
            return False
        
        print(f"✅ Found service: {service.name}")
        
        # Create test data
        test_data = {
            'service': service,
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone': '+971501234567',
            'pricing_tier': 'standard',
            'booking_estimate': '2-3',
            'booking_datetime': datetime.now() + timedelta(days=1),
            'number_of_people': 2,
            'hourly_rate': 70.00,
            'additional_notes': 'Test booking created by script',
            'cc_zone': False
        }
        
        # Create service request
        service_request = ServiceRequest.objects.create(**test_data)
        
        print(f"✅ ServiceRequest created successfully!")
        print(f"   ID: {service_request.id}")
        print(f"   Customer: {service_request.customer_name}")
        print(f"   Service: {service_request.service.name}")
        print(f"   Status: {service_request.get_status_display()}")
        print(f"   Total Amount: £{service_request.total_amount}")
        print(f"   WhatsApp Sent: {service_request.whatsapp_sent}")
        
        # Verify it was saved
        count = ServiceRequest.objects.count()
        print(f"\n✅ Total ServiceRequests in database: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating ServiceRequest: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Testing ServiceRequest Creation")
    print("=" * 60)
    test_service_request_creation()
