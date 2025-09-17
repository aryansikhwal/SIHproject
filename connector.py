from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),  # Will use empty string if not set
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_DATABASE', 'attendance_system')
}

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///attendance_system.db"  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# --- Database Models ---
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    roll_number = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15))
    enrollment_date = db.Column(db.Date, nullable=False)
    consent_given = db.Column(db.Boolean, default=False)

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(10))

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    method = db.Column(db.String(20), nullable=False)

# --- Database Functions ---
def initialize_database():
    """Create all database tables."""
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully")

def get_all_users():
    """Fetch all users from the 'users' table."""
    try:
        users = User.query.all()
        print("\n📋 All Users:")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Name: {user.full_name}, Role: {user.role}")
        return users
    except Exception as e:
        print(f"❌ Error fetching users: {e}")
        return []

def insert_new_student(student_data):
    """
    Inserts a new student record into the 'students' table.
    student_data is a tuple: (student_id, full_name, class_id, roll_number, phone, enrollment_date, consent_given)
    """
    try:
        new_student = Student(
            student_id=student_data[0],
            full_name=student_data[1],
            class_id=student_data[2],
            roll_number=student_data[3],
            phone=student_data[4],
            enrollment_date=student_data[5],
            consent_given=student_data[6]
        )
        db.session.add(new_student)
        db.session.commit()
        print(f"✅ Student '{new_student.full_name}' inserted successfully!")
        return new_student.id
    except Exception as e:
        print(f"❌ Error inserting student: {e}")
        db.session.rollback()
        return None

def record_attendance(attendance_data):
    """
    Records a new attendance entry.
    attendance_data is a tuple: (student_id, class_id, teacher_id, attendance_date, method)
    """
    try:
        new_attendance = Attendance(
            student_id=attendance_data[0],
            class_id=attendance_data[1],
            teacher_id=attendance_data[2],
            attendance_date=attendance_data[3],
            method=attendance_data[4]
        )
        db.session.add(new_attendance)
        db.session.commit()
        print("✅ Attendance record created successfully.")
        return True
    except Exception as e:
        print(f"❌ Error recording attendance: {e}")
        db.session.rollback()
        return False

# --- Example Usage ---
if __name__ == "__main__":
    # Initialize the database and create tables
    initialize_database()
    
    with app.app_context():
        # Create a default class if it doesn't exist
        if not Class.query.first():
            default_class = Class(class_name='Class 10 A', section='A')
            db.session.add(default_class)
            db.session.commit()
            print("✅ Default class created")

        # Create a default admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                full_name='Admin User',
                role='teacher'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Default admin user created")

        # Example 1: Fetch and display all users
        users = get_all_users()

        print("\n--- Inserting a New Student ---")
        # Using the default class (id=1)
        student_info = ('SIH002', 'Jane Smith', 1, '02', '9876543210', '2024-07-15', True)
        new_student_id = insert_new_student(student_info)

        if new_student_id:
            print(f"New student ID: {new_student_id}")

            print("\n--- Recording Attendance for the New Student ---")
            # Using the default admin user (id=1)
            attendance_info = (new_student_id, 1, 1, '2025-09-16', 'manual')
            record_attendance(attendance_info)

    print("\n✅ Operations completed successfully")