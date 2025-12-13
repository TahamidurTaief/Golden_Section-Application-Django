"""
Test script to submit a service request via the API
"""
import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_ENDPOINT = f"{BASE_URL}/quotations/create/"

# Test data
test_data = {
    "service_id": 48,  # Modern Home Interior Design
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+971501234567",
    "booking_date": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
    "booking_time": "10:00 AM",
    "location_address": "Dubai Marina, Dubai, UAE",
    "location_latitude": "25.0810",
    "location_longitude": "55.1400",
    "additional_notes": "Please call before arriving. Need consultation for living room design.",
    "number_of_people": 1,
    "hourly_rate": 0,
    "cc_zone": False
}

print("=" * 60)
print("TESTING SERVICE REQUEST SUBMISSION")
print("=" * 60)
print(f"\nSubmitting request to: {API_ENDPOINT}")
print(f"Test Data: {json.dumps(test_data, indent=2)}")

try:
    # Make the request
    response = requests.post(
        API_ENDPOINT,
        data=test_data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    
    print(f"\n✓ Response Status: {response.status_code}")
    print(f"✓ Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Success!")
        print(json.dumps(result, indent=2))
    else:
        print(f"\n✗ Error!")
        print(f"Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("\n✗ Connection Error: Make sure the Django development server is running")
    print("   Run: uv run python manage.py runserver")
except Exception as e:
    print(f"\n✗ Error: {str(e)}")

print("\n" + "=" * 60)
