"""
Test script to verify the API endpoints are working
"""
import requests
import json

def test_api():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing AttenSync API Endpoints")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health Check:")
            print(f"   Status: {data['status']}")
            print(f"   Database Users: {data['database']['users']}")
            print(f"   Database Students: {data['database']['students']}")
            print(f"   Database Attendance: {data['database']['attendance_records']}")
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
    
    # Test dashboard stats
    try:
        response = requests.get(f"{base_url}/api/stats/dashboard")
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Dashboard Stats:")
            print(f"   Total Students: {data['total_students']}")
            print(f"   Total Classes: {data['total_classes']}")
            print(f"   Present Today: {data['present_today']}")
            print(f"   Attendance %: {data['attendance_percentage']}%")
        else:
            print(f"❌ Dashboard Stats Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard Stats Error: {e}")
    
    # Test students endpoint
    try:
        response = requests.get(f"{base_url}/api/students")
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Students Endpoint:")
            print(f"   Total Students: {data['total']}")
            print(f"   Sample Student: {data['students'][0]['full_name']} (RFID: {data['students'][0]['rfid_tag']})")
        else:
            print(f"❌ Students Endpoint Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Students Endpoint Error: {e}")
    
    # Test attendance endpoint
    try:
        response = requests.get(f"{base_url}/api/attendance")
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Attendance Endpoint:")
            print(f"   Total Records: {data['total']}")
            if data['attendance']:
                print(f"   Sample Record: {data['attendance'][0]['student_name']} - {data['attendance'][0]['status']}")
        else:
            print(f"❌ Attendance Endpoint Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Attendance Endpoint Error: {e}")
    
    # Test RFID scans endpoint
    try:
        response = requests.get(f"{base_url}/api/rfid/scans")
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ RFID Scans Endpoint:")
            print(f"   Total Scans: {data['total']}")
            if data['scans']:
                print(f"   Sample Scan: {data['scans'][0]['rfid_tag']} - {data['scans'][0]['status']}")
        else:
            print(f"❌ RFID Scans Endpoint Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ RFID Scans Endpoint Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")

if __name__ == '__main__':
    test_api()