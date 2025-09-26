import requests
import json
import time

# Test script to simulate RFID scanning for Arvind and Soumya

BASE_URL = "http://localhost:5001"  # Change if your Flask app runs on a different port

def scan_rfid(tag, student_name):
    print(f"\nScanning RFID for {student_name}...")
    url = f"{BASE_URL}/api/scan_rfid"
    
    payload = {
        "tag": tag,
        "student_name": student_name
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response:")
            print(json.dumps(data, indent=2))
            print(f"RFID scan successful for {student_name}!")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error connecting to server: {str(e)}")
        return False

def check_attendance_status():
    print("\nChecking current attendance status...")
    try:
        response = requests.get(f"{BASE_URL}/api/attendance?class=1&date={time.strftime('%Y-%m-%d')}")
        
        if response.status_code == 200:
            data = response.json()
            print("Current attendance records:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error getting attendance: {response.text}")
            
    except Exception as e:
        print(f"Error connecting to server: {str(e)}")

def check_scan_logs():
    print("\nChecking recent RFID scans...")
    try:
        response = requests.get(f"{BASE_URL}/api/rfid_scans?limit=5")
        
        if response.status_code == 200:
            data = response.json()
            print("Recent RFID scans:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error getting scan logs: {response.text}")
            
    except Exception as e:
        print(f"Error connecting to server: {str(e)}")

def check_student_list():
    """Check if students are in the database"""
    print("\nChecking student list...")
    try:
        response = requests.get(f"{BASE_URL}/api/students")
        if response.status_code == 200:
            students = response.json()
            print(f"Found {len(students)} students in database:")
            for student in students:
                print(f" - {student['full_name']} (ID: {student['student_id']})")
            return students
        else:
            print(f"Error retrieving student list: {response.text}")
            return []
    except Exception as e:
        print(f"Error connecting to server: {str(e)}")
        print("Is your Flask server running? Make sure it's started with 'python app.py'")
        return []

if __name__ == "__main__":
    print("RFID Scan Test for AttenSync")
    print("===========================")
    
    # Check if students exist
    students = check_student_list()
    found_arvind = any(s['full_name'] == 'Arvind' for s in students)
    found_soumya = any(s['full_name'] == 'Soumya' for s in students)
    
    if not found_arvind or not found_soumya:
        print("\n⚠️ WARNING: Students not found in database!")
        if not found_arvind:
            print("- Arvind is missing")
        if not found_soumya:
            print("- Soumya is missing")
        print("\nPlease run 'python add_students.py' first to add the required students.")
        choice = input("\nDo you want to continue anyway? (y/n): ")
        if choice.lower() != 'y':
            print("Exiting. Run 'python add_students.py' first.")
            exit()
    
    # Initial status
    check_attendance_status()
    check_scan_logs()
    
    # Perform scans
    input("\nPress Enter to scan RFID for Arvind...")
    scan_rfid("ARVIND001", "Arvind")
    
    input("\nPress Enter to scan RFID for Soumya...")
    scan_rfid("SOUMYA001", "Soumya")
    
    # Check final status
    check_attendance_status()
    check_scan_logs()
    
    print("\nTest complete!")
