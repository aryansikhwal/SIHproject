"""
Add Arvind and Soumya students to the database
This script directly adds the students and creates absence records for them
Run this script from the main directory with `python add_students.py`
"""
import os
import sys
from datetime import date

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from app.py
try:
    from app import app, db, Student, Class, User, Attendance
except ImportError as e:
    print(f"Error importing from app.py: {e}")
    sys.exit(1)

def add_students():
    with app.app_context():
        try:
            print("Adding students to database...")
            
            # Check if admin exists (for teacher_id reference)
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("Creating admin user first...")
                from app import generate_password_hash
                admin = User(
                    username='admin',
                    password_hash=generate_password_hash('admin123'),
                    full_name='Administrator',
                    email='admin@attensync.com',
                    role='principal'
                )
                db.session.add(admin)
                db.session.commit()
                
            # Check if a class exists
            default_class = Class.query.first()
            if not default_class:
                print("Creating a default class...")
                default_class = Class(
                    class_name="Default Class",
                    section="A",
                    teacher_id=admin.id,
                    academic_year="2025-2026",
                    is_active=True
                )
                db.session.add(default_class)
                db.session.commit()
                
            # Add Arvind if not exists
            arvind = Student.query.filter_by(full_name='Arvind').first()
            if not arvind:
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
                print("Added student: Arvind")
            else:
                print("Student Arvind already exists")
                
            # Add Soumya if not exists  
            soumya = Student.query.filter_by(full_name='Soumya').first()
            if not soumya:
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
                print("Added student: Soumya")
            else:
                print("Student Soumya already exists")
                
            db.session.commit()
            
            # Ensure we have the latest student records
            if not arvind:
                arvind = Student.query.filter_by(full_name='Arvind').first()
            if not soumya:
                soumya = Student.query.filter_by(full_name='Soumya').first()
                
            # Create absent attendance records for today
            today = date.today()
            
            for student in [arvind, soumya]:
                # Check if attendance record already exists
                existing = Attendance.query.filter_by(
                    student_id=student.id,
                    attendance_date=today
                ).first()
                
                if not existing:
                    # Create absent attendance record
                    attendance = Attendance(
                        student_id=student.id,
                        class_id=student.class_id,
                        teacher_id=admin.id,
                        attendance_date=today,
                        status='absent',
                        method='manual'
                    )
                    db.session.add(attendance)
                    print(f"Created absent attendance record for {student.full_name}")
                else:
                    print(f"Attendance record already exists for {student.full_name}")
            
            db.session.commit()
            print("Done! Students added with initial absent status.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            return False
    
    return True

if __name__ == "__main__":
    success = add_students()
    if success:
        print("\nStudents added successfully! You should now see Arvind and Soumya in the students list,")
        print("initially marked as absent. When you scan their RFID tags, they'll be marked as present.")
        print("\nRFID tags to use:")
        print("Arvind: ARVIND001")
        print("Soumya: SOUMYA001")
    else:
        print("\nFailed to add students. Check the error messages above.")
