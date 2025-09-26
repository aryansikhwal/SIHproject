#!/usr/bin/env python3
"""
Demo RFID Scan Simulation
"""
from models import *
from backend import app
import datetime

with app.app_context():
    # Find student with RFID tag
    student = Student.query.filter_by(rfid_tag='RFID001A').first()
    
    if student:
        print(f"📱 RFID Scan Detected: {student.rfid_tag}")
        print(f"👤 Student: {student.full_name}")
        
        # Log the scan
        scan = RFIDScanLog(
            rfid_tag=student.rfid_tag,
            scan_time=datetime.datetime.now(),
            status='success',
            student_id=student.id
        )
        db.session.add(scan)
        
        # Mark attendance
        today = datetime.date.today()
        existing_attendance = Attendance.query.filter_by(
            student_id=student.id,
            attendance_date=today
        ).first()
        
        if not existing_attendance:
            attendance = Attendance(
                student_id=student.id,
                class_id=student.class_id,
                teacher_id=1,
                attendance_date=today,
                method='rfid'
            )
            db.session.add(attendance)
            scan.attendance_id = attendance.id
            print(f"✅ Attendance marked successfully!")
        else:
            scan.status = 'already_marked'
            print(f"⚠️  Attendance already marked for today")
        
        db.session.commit()
        
        print(f"📊 Total scans in system: {RFIDScanLog.query.count()}")
        print(f"📈 Total attendance records: {Attendance.query.count()}")
        
    else:
        print("❌ No student found with RFID tag RFID001A")