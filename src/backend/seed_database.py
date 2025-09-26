import random
from datetime import datetime, timedelta

def seed():
    from app import app, db, User, Class, Student, Attendance
    with app.app_context():
        db.create_all()
        # Create classes
        class1 = Class(class_name='Class 1', section='A', teacher_id=1, academic_year='2025-26', is_active=True)
        db.session.add(class1)
        db.session.commit()
        # Create students
        students = []
        for i in range(1, 21):
            student = Student(
                student_id=f'STUD{i:03d}',
                full_name=f'Student {i}',
                class_id=class1.id,
                roll_number=str(i),
                father_name=f'Father {i}',
                mother_name=f'Mother {i}',
                date_of_birth=datetime(2010, 1, 1) + timedelta(days=i*30),
                address=f'Address {i}',
                phone=f'99999{i:05d}',
                rfid_tag=f'RFID{i:03d}',
                enrollment_date=datetime(2023, 6, 1),
                is_active=True,
                consent_given=True
            )
            students.append(student)
            db.session.add(student)
        db.session.commit()
        # Create attendance records for 100 days
        start_date = datetime(2025, 6, 1)
        for day in range(100):
            date = start_date + timedelta(days=day)
            for student in students:
                status = 'present' if random.random() > 0.1 else 'absent'
                attendance = Attendance(
                    student_id=student.id,
                    class_id=class1.id,
                    teacher_id=1,
                    attendance_date=date.date(),
                    time_marked=date,
                    status=status,
                    method='rfid',
                    confidence_score=1.0,
                    notes='Seeded attendance'
                )
                db.session.add(attendance)
        db.session.commit()
        print('Database seeded with classes, students, and attendance records.')

if __name__ == '__main__':
    seed()
