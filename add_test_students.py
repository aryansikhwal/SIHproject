from app import app, db, Student, Attendance, User
from datetime import date
import time

# This script adds Arvind and Soumya to the database
# and creates initial absent attendance records for them

def add_test_students():
    with app.app_context():
        try:
            print("Adding test students...")
            
            # Get admin user for attendance records
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                print("Error: Admin user not found. Please run app.py first to initialize the database.")
                return False
                
            # Get or create a default class
            from app import Class
            default_class = Class.query.first()
            if not default_class:
                print("Creating default class...")
                default_class = Class(
                    class_name="Test Class",
                    section="A",
                    teacher_id=admin_user.id,
                    academic_year="2025-2026",
                    is_active=True
                )
                db.session.add(default_class)
                db.session.commit()
                
            # Check if students already exist
            arvind = Student.query.filter_by(full_name='Arvind').first()
            soumya = Student.query.filter_by(full_name='Soumya').first()
            
            if not arvind:
                # Add Arvind
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
                
            if not soumya:
                # Add Soumya
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
                
            # Commit to save students
            db.session.commit()
            
            # Make sure we have the student records
            if not arvind:
                arvind = Student.query.filter_by(full_name='Arvind').first()
            if not soumya:
                soumya = Student.query.filter_by(full_name='Soumya').first()
            
            today = date.today()
            
            # Create absent attendance records for today
            students = [arvind, soumya]
            for student in students:
                # Check if attendance already exists
                existing = Attendance.query.filter_by(
                    student_id=student.id,
                    attendance_date=today
                ).first()
                
                if not existing:
                    attendance = Attendance(
                        student_id=student.id,
                        class_id=student.class_id,
                        teacher_id=admin_user.id,
                        attendance_date=today,
                        status='absent',
                        method='manual'
                    )
                    db.session.add(attendance)
                    print(f"Created absent attendance record for {student.full_name}")
                else:
                    print(f"Attendance record already exists for {student.full_name}")
            
            db.session.commit()
            print("Successfully added test students and created attendance records!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error adding test students: {str(e)}")
            return False

if __name__ == '__main__':
    add_test_students()
