"""
Test form submission directly
"""
import os
import django
import json
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoldenSection.settings')
django.setup()

from django.test import Client
from services.models import Service

def test_form_submission():
    """Test the actual form submission endpoint"""
    
    # Get a service
    service = Service.objects.first()
    if not service:
        print("❌ No services found!")
        return
    
    print(f"✅ Testing with service: {service.name} (ID: {service.id})")
    
    # Create test data matching the form
    booking_time = datetime.now() + timedelta(days=1)
    booking_datetime_str = booking_time.strftime('%Y-%m-%dT%H:%M')
    
    form_data = {
        'service_id': service.id,
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+971501234567',
        'booking_estimate': '2-3',
        'booking_datetime': booking_datetime_str,
        'number_of_people': 2,
        'hourly_rate': 70.0,
        'additional_notes': 'Test booking from direct submission',
        'cc_zone': False
    }
    
    print("\n📤 Sending form data:")
    print(json.dumps(form_data, indent=2))
    
    # Create client and submit
    client = Client()
    response = client.post(
        '/quotations/create/',
        data=json.dumps(form_data),
        content_type='application/json'
    )
    
    print(f"\n📥 Response Status: {response.status_code}")
    
    try:
        result = response.json()
        print("Response Data:")
        print(json.dumps(result, indent=2))
        
        if result.get('success'):
            print("\n✅ SUCCESS! Service request created!")
            print(f"   Request ID: {result.get('request_id')}")
            
            # Verify it's in the database
            from quotations.models import ServiceRequest
            count = ServiceRequest.objects.count()
            print(f"   Total requests in DB: {count}")
            
            latest = ServiceRequest.objects.last()
            if latest:
                print(f"   Latest: ID={latest.id}, Customer={latest.customer_name}")
        else:
            print(f"\n❌ FAILED: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error parsing response: {e}")
        print(f"Raw response: {response.content}")

if __name__ == '__main__':
    print("=" * 60)
    print("Testing Service Request Form Submission")
    print("=" * 60)
    test_form_submission()
