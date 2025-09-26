#!/usr/bin/env python3
"""
Test        # Test data counts
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM students") 
        student_count = cursor.fetchone()[0]ase Connectivity for AttenSync
Verifies all database connections between modules work correctly
"""

import sys
import os
from datetime import datetime, timedelta
import sqlite3

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import db, User, Student, Class, Attendance, RFIDScanLog
from backend import app
from forecast_model import AttendanceForecastModel

def test_database_connection():
    """Test direct database connection"""
    print("1. Testing Database Connection...")
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'attensync.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test basic connection
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"   ✓ Database connected successfully")
        print(f"   ✓ Found {len(tables)} tables: {[t[0] for t in tables]}")
        
        # Test data counts
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM student") 
        student_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM attendance")
        attendance_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM rfid_scan_logs")
        scan_count = cursor.fetchone()[0]
        
        print(f"   ✓ Users: {user_count}")
        print(f"   ✓ Students: {student_count}")
        print(f"   ✓ Attendance records: {attendance_count}")
        print(f"   ✓ RFID scan logs: {scan_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ✗ Database connection failed: {e}")
        return False

def test_flask_app_models():
    """Test Flask app and SQLAlchemy models"""
    print("\n2. Testing Flask App & Models...")
    
    try:
        with app.app_context():
            # Test model queries
            users = User.query.all()
            students = Student.query.all()
            classes = Class.query.all()
            attendance = Attendance.query.all()
            scans = RFIDScanLog.query.all()
            
            print(f"   ✓ Flask app context working")
            print(f"   ✓ Users via model: {len(users)}")
            print(f"   ✓ Students via model: {len(students)}")
            print(f"   ✓ Classes via model: {len(classes)}")
            print(f"   ✓ Attendance via model: {len(attendance)}")
            print(f"   ✓ RFID scans via model: {len(scans)}")
            
            # Test a sample student with their attendance
            if students:
                sample_student = students[0]
                student_attendance = Attendance.query.filter_by(student_id=sample_student.id).all()
                print(f"   ✓ Sample student '{sample_student.full_name}' has {len(student_attendance)} attendance records")
                
        return True
        
    except Exception as e:
        print(f"   ✗ Flask app/models failed: {e}")
        return False

def test_ml_model():
    """Test ML model database connection"""
    print("\n3. Testing ML Model Database Connection...")
    
    try:
        model = AttendanceForecastModel()
        data = model.load_attendance_data(days_back=30)
        
        print(f"   ✓ ML model initialized")
        print(f"   ✓ Loaded {len(data)} historical records")
        
        if len(data) > 0:
            print(f"   ✓ Data columns: {list(data.columns)}")
            if 'ds' in data.columns:
                print(f"   ✓ Date range: {data['ds'].min()} to {data['ds'].max()}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ ML model failed: {e}")
        return False

def test_rfid_database_functions():
    """Test RFID system database functions"""
    print("\n4. Testing RFID Database Functions...")
    
    try:
        with app.app_context():
            # Test finding a student by RFID
            test_student = Student.query.first()
            if test_student and test_student.rfid_tag:
                print(f"   ✓ Test student found: {test_student.full_name} (RFID: {test_student.rfid_tag})")
                
                # Simulate creating an RFID scan log
                test_scan = RFIDScanLog(
                    rfid_tag=test_student.rfid_tag,
                    scan_time=datetime.now(),
                    student_id=test_student.id,
                    status='success'
                )
                
                db.session.add(test_scan)
                db.session.commit()
                
                print(f"   ✓ Test RFID scan log created successfully")
                
                # Clean up the test scan
                db.session.delete(test_scan)
                db.session.commit()
                print(f"   ✓ Test scan cleaned up")
            else:
                print(f"   ! No students with RFID tags found for testing")
                
        return True
        
    except Exception as e:
        print(f"   ✗ RFID database functions failed: {e}")
        return False

def main():
    """Run all database connectivity tests"""
    print("="*50)
    print("AttenSync Database Connectivity Test")
    print("="*50)
    
    tests_passed = 0
    total_tests = 4
    
    if test_database_connection():
        tests_passed += 1
        
    if test_flask_app_models():
        tests_passed += 1
        
    if test_ml_model():
        tests_passed += 1
        
    if test_rfid_database_functions():
        tests_passed += 1
    
    print("\n" + "="*50)
    print(f"Database Connectivity Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("✅ ALL DATABASE CONNECTIONS ARE WORKING!")
        print("✅ Your system rebuild was successful!")
    else:
        print("❌ Some database connections have issues")
    
    print("="*50)

if __name__ == "__main__":
    main()