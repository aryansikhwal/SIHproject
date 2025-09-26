#!/usr/bin/env python3
"""
View RFID Scan Data
"""
from models import *
from backend import app

with app.app_context():
    print("🏷️ Recent RFID Scans:")
    print("=" * 50)
    
    # Get recent scans
    scans = RFIDScanLog.query.order_by(RFIDScanLog.scan_time.desc()).limit(10).all()
    
    for scan in scans:
        time_str = scan.scan_time.strftime('%H:%M:%S')
        print(f"⏰ {time_str} - RFID: {scan.rfid_tag} - Status: {scan.status}")
        if scan.error_message:
            print(f"   ❌ Error: {scan.error_message}")
    
    print("=" * 50)
    print(f"📊 Total RFID scans in system: {RFIDScanLog.query.count()}")
    print(f"✅ Today's attendance records: {Attendance.query.filter_by(attendance_date=datetime.now().date()).count()}")
    print(f"👥 Total students: {Student.query.count()}")
    
    # Show which RFID tags are registered
    print("\n🎫 Registered RFID Tags:")
    students = Student.query.filter(Student.rfid_tag.isnot(None)).all()
    for student in students:
        print(f"   📱 {student.rfid_tag} - {student.full_name}")