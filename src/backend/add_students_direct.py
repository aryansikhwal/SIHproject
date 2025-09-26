"""
Add Arvind and Soumya directly to the database
This script will:
1. Create a class if none exists
2. Add Arvind and Soumya as students
3. Create initial "absent" attendance records

Run this script from the terminal with:
python add_students_direct.py
"""

from app import app, db, User, Class, Student, Attendance
from datetime import date
import sys

def add_students_direct():
    # Use Flask app context
    with app.app_context():
        try:
            print("Starting to add students to database...")
            
            # 1. Get/create admin user (needed for teacher_id foreign key)
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                from werkzeug.security import generate_password_hash
                print("Creating admin user first...")
                admin = User(
                    username='admin',
                    password_hash=generate_password_hash('admin123'),
                    full_name='Administrator',
                    email='admin@attensync.com',
                    role='principal'
                )
                db.session.add(admin)
                db.session.commit()
                print("Admin user created.")
                
            # 2. Get/create class (needed for class_id foreign key)
            default_class = Class.query.first()
            if not default_class:
                print("No class found. Creating a default class...")
                default_class = Class(
                    class_name="Default Class",
                    section="A",
                    teacher_id=admin.id,
                    academic_year="2025-2026",
                    is_active=True
                )
                db.session.add(default_class)
                db.session.commit()
                print(f"Default class created with ID: {default_class.id}")
            else:
                print(f"Using existing class: {default_class.class_name} (ID: {default_class.id})")
            
            # 3. Add Arvind if not exists
            arvind = Student.query.filter_by(full_name='Arvind').first()
            if not arvind:
                print("Adding Arvind to students table...")
                arvind = Student(
                    student_id="SIH001",
                    full_name="Arvind",
                    class_id=default_class.id,
                    roll_number="1",
                    rfid_tag="ARVIND001",
                    enrollment_date=date.today(),
                    is_active=True
                )
                db.session.add(arvind)
                db.session.commit()
                print(f"Arvind added with ID: {arvind.id}")
            else:
                print(f"Arvind already exists with ID: {arvind.id}")
            
            # 4. Add Soumya if not exists
            soumya = Student.query.filter_by(full_name='Soumya').first()
            if not soumya:
                print("Adding Soumya to students table...")
                soumya = Student(
                    student_id="SIH002",
                    full_name="Soumya",
                    class_id=default_class.id,
                    roll_number="2",
                    rfid_tag="SOUMYA001",
                    enrollment_date=date.today(),
                    is_active=True
                )
                db.session.add(soumya)
                db.session.commit()
                print(f"Soumya added with ID: {soumya.id}")
            else:
                print(f"Soumya already exists with ID: {soumya.id}")
                
            # Refresh student references
            if not arvind:
                arvind = Student.query.filter_by(full_name='Arvind').first()
            if not soumya:
                soumya = Student.query.filter_by(full_name='Soumya').first()
                
            # 5. Create initial "absent" attendance records
            today = date.today()
            
            # For Arvind
            arvind_attendance = Attendance.query.filter_by(
                student_id=arvind.id,
                attendance_date=today
            ).first()
            
            if not arvind_attendance:
                print("Creating absent attendance record for Arvind...")
                arvind_attendance = Attendance(
                    student_id=arvind.id,
                    class_id=arvind.class_id,
                    teacher_id=admin.id,
                    attendance_date=today,
                    status='absent',
                    method='manual'
                )
                db.session.add(arvind_attendance)
            else:
                print(f"Attendance record already exists for Arvind (status: {arvind_attendance.status})")
            
            # For Soumya
            soumya_attendance = Attendance.query.filter_by(
                student_id=soumya.id,
                attendance_date=today
            ).first()
            
            if not soumya_attendance:
                print("Creating absent attendance record for Soumya...")
                soumya_attendance = Attendance(
                    student_id=soumya.id,
                    class_id=soumya.class_id,
                    teacher_id=admin.id,
                    attendance_date=today,
                    status='absent',
                    method='manual'
                )
                db.session.add(soumya_attendance)
            else:
                print(f"Attendance record already exists for Soumya (status: {soumya_attendance.status})")
            
            # Commit all changes
            db.session.commit()
            print("\n✅ SUCCESS! Arvind and Soumya are now in the database.")
            print("They should now appear in the students list in your frontend.")
            print("\nRFID tags:")
            print("- Arvind: ARVIND001")
            print("- Soumya: SOUMYA001")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ ERROR: {str(e)}")
            return False
            
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("ADDING STUDENTS TO DATABASE")
    print("=" * 50)
    
    success = add_students_direct()
    
    if success:
        print("\nWhat's next:")
        print("1. Refresh your frontend to see the new students")
        print("2. Test RFID scanning with: python test_rfid_scan.py")
    else:
        print("\nFailed to add students. Please check the error messages above.")
