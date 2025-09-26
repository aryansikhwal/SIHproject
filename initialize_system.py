"""
AttenSync System Initialization Script
Sets up database, creates test data, and starts all services
"""
import os
import sys
import subprocess
from datetime import datetime, date, timedelta
import random

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from models import db, User, Class, Student, Attendance, RFIDScanLog, init_database
from forecast_model import AttendanceForecastModel

def print_banner():
    """Print startup banner"""
    print("╔" + "="*60 + "╗")
    print("║" + " AttenSync System Initialization ".center(60) + "║")
    print("║" + " Fresh Database & Service Setup ".center(60) + "║")
    print("╚" + "="*60 + "╝")
    print()

def create_flask_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'attensync-init-key'
    
    # Use absolute path for database
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'attensync.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Ensure instance directory exists
    instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    
    return app

def setup_test_data(app):
    """Create comprehensive test data"""
    with app.app_context():
        print("📊 Creating test data...")
        
        # Create admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@attensync.com',
                full_name='System Administrator',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("  ✓ Admin user created")
        
        # Create teacher user
        teacher = User.query.filter_by(username='teacher').first()
        if not teacher:
            teacher = User(
                username='teacher',
                email='teacher@attensync.com',
                full_name='John Teacher',
                role='teacher'
            )
            teacher.set_password('teacher123')
            db.session.add(teacher)
            print("  ✓ Teacher user created")
        
        db.session.commit()
        
        # Create classes
        classes_data = [
            {'name': 'Class 5A', 'grade_level': 5, 'section': 'A'},
            {'name': 'Class 5B', 'grade_level': 5, 'section': 'B'},
            {'name': 'Class 6A', 'grade_level': 6, 'section': 'A'},
        ]
        
        created_classes = []
        for class_data in classes_data:
            existing_class = Class.query.filter_by(name=class_data['name']).first()
            if not existing_class:
                new_class = Class(
                    name=class_data['name'],
                    grade_level=class_data['grade_level'],
                    section=class_data['section'],
                    teacher_id=teacher.id,
                    academic_year='2024-25'
                )
                db.session.add(new_class)
                created_classes.append(new_class)
                print(f"  ✓ Created {class_data['name']}")
        
        db.session.commit()
        
        # Get all classes for student creation
        all_classes = Class.query.filter_by(is_active=True).all()
        
        # Create students with RFID tags
        students_data = [
            {'name': 'Alice Johnson', 'roll': '001', 'rfid': 'RFID001A'},
            {'name': 'Bob Smith', 'roll': '002', 'rfid': 'RFID002B'},
            {'name': 'Charlie Brown', 'roll': '003', 'rfid': 'RFID003C'},
            {'name': 'Diana Prince', 'roll': '004', 'rfid': 'RFID004D'},
            {'name': 'Edward Norton', 'roll': '005', 'rfid': 'RFID005E'},
            {'name': 'Fiona Shaw', 'roll': '006', 'rfid': 'RFID006F'},
            {'name': 'George Wilson', 'roll': '007', 'rfid': 'RFID007G'},
            {'name': 'Helen Davis', 'roll': '008', 'rfid': 'RFID008H'},
            {'name': 'Ivan Petrov', 'roll': '009', 'rfid': 'RFID009I'},
            {'name': 'Julia Roberts', 'roll': '010', 'rfid': 'RFID010J'},
        ]
        
        created_students = []
        for i, student_data in enumerate(students_data):
            class_obj = all_classes[i % len(all_classes)]  # Distribute across classes
            
            existing_student = Student.query.filter_by(
                roll_number=student_data['roll'],
                class_id=class_obj.id
            ).first()
            
            if not existing_student:
                student = Student(
                    roll_number=student_data['roll'],
                    rfid_tag=student_data['rfid'],
                    full_name=student_data['name'],
                    class_id=class_obj.id,
                    gender=random.choice(['male', 'female']),
                    parent_contact=f"+91{random.randint(7000000000, 9999999999)}",
                    parent_email=f"{student_data['name'].lower().replace(' ', '.')}@parent.com"
                )
                db.session.add(student)
                created_students.append(student)
                print(f"  ✓ Created student: {student_data['name']} (RFID: {student_data['rfid']})")
        
        db.session.commit()
        
        # Create historical attendance data for ML training
        print("📈 Generating historical attendance data...")
        all_students = Student.query.filter_by(is_active=True).all()
        
        # Generate attendance for last 30 days
        for days_back in range(30, 0, -1):
            attendance_date = date.today() - timedelta(days=days_back)
            
            # Skip weekends for more realistic data
            if attendance_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
                continue
            
            for student in all_students:
                # 85-95% attendance rate with some randomness
                base_rate = 0.90
                daily_variation = random.uniform(-0.15, 0.10)
                attendance_prob = max(0.70, min(0.98, base_rate + daily_variation))
                
                if random.random() < attendance_prob:
                    # Check if attendance already exists
                    existing = Attendance.query.filter_by(
                        student_id=student.id,
                        attendance_date=attendance_date
                    ).first()
                    
                    if not existing:
                        attendance = Attendance(
                            student_id=student.id,
                            class_id=student.class_id,
                            teacher_id=teacher.id,
                            attendance_date=attendance_date,
                            time_marked=datetime.combine(attendance_date, 
                                                       datetime.min.time().replace(
                                                           hour=random.randint(8, 10),
                                                           minute=random.randint(0, 59)
                                                       )),
                            status='present',
                            method=random.choice(['manual', 'rfid']),
                            confidence_score=1.0
                        )
                        db.session.add(attendance)
        
        db.session.commit()
        print(f"  ✓ Generated attendance records for {len(all_students)} students over 30 days")
        
        # Create some RFID scan logs
        print("📱 Creating sample RFID scan logs...")
        sample_scans = [
            {'rfid': 'RFID001A', 'status': 'success'},
            {'rfid': 'RFID002B', 'status': 'success'},
            {'rfid': 'UNKNOWN123', 'status': 'invalid_tag'},
            {'rfid': 'RFID003C', 'status': 'already_marked'},
        ]
        
        for scan_data in sample_scans:
            student = Student.query.filter_by(rfid_tag=scan_data['rfid']).first()
            
            scan_log = RFIDScanLog(
                rfid_tag=scan_data['rfid'],
                scan_time=datetime.utcnow() - timedelta(minutes=random.randint(1, 60)),
                student_id=student.id if student else None,
                status=scan_data['status'],
                error_message='Invalid RFID tag' if scan_data['status'] == 'invalid_tag' else None
            )
            db.session.add(scan_log)
        
        db.session.commit()
        print(f"  ✓ Created {len(sample_scans)} RFID scan log entries")

def test_database_operations(app):
    """Test database operations"""
    with app.app_context():
        print("🧪 Testing database operations...")
        
        # Test counts
        user_count = User.query.count()
        class_count = Class.query.count()
        student_count = Student.query.count()
        attendance_count = Attendance.query.count()
        rfid_scan_count = RFIDScanLog.query.count()
        
        print(f"  ✓ Users: {user_count}")
        print(f"  ✓ Classes: {class_count}")
        print(f"  ✓ Students: {student_count}")
        print(f"  ✓ Attendance records: {attendance_count}")
        print(f"  ✓ RFID scans: {rfid_scan_count}")
        
        # Test a complex query
        today_attendance = Attendance.query.filter_by(attendance_date=date.today()).count()
        print(f"  ✓ Today's attendance: {today_attendance}")
        
        return {
            'users': user_count,
            'classes': class_count,
            'students': student_count,
            'attendance': attendance_count,
            'rfid_scans': rfid_scan_count,
            'today_attendance': today_attendance
        }

def test_ml_model():
    """Test ML forecasting model"""
    print("🤖 Testing ML forecasting model...")
    
    try:
        # Initialize model
        model = AttendanceForecastModel()
        
        # Load data
        data = model.load_attendance_data(days_back=30)
        print(f"  ✓ Loaded {len(data)} days of data")
        
        if len(data) >= 14:
            # Train model
            if model.train_model():
                print("  ✓ Model training successful")
                
                # Generate forecast
                forecast = model.generate_forecast(periods=7)
                if forecast:
                    print(f"  ✓ 7-day forecast generated (avg: {forecast['summary']['average_predicted_attendance']}%)")
                
                # Generate insights
                insights = model.get_attendance_insights()
                if 'error' not in insights:
                    print("  ✓ Attendance insights generated")
                    return True
        else:
            print("  ⚠️ Insufficient data for ML training")
            return False
            
    except Exception as e:
        print(f"  ❌ ML model test failed: {e}")
        return False
    
    return True

def create_startup_scripts():
    """Create convenient startup scripts"""
    print("📜 Creating startup scripts...")
    
    # Backend startup script
    backend_script = """#!/bin/bash
# AttenSync Backend Startup Script

echo "Starting AttenSync Backend Server..."
python backend.py
"""
    
    with open('start_backend.sh', 'w', encoding='utf-8') as f:
        f.write(backend_script)
    
    # RFID listener startup script
    rfid_script = """#!/bin/bash
# AttenSync RFID Listener Startup Script

echo "Starting AttenSync RFID Listener..."
python rfid_system.py
"""
    
    with open('start_rfid.sh', 'w', encoding='utf-8') as f:
        f.write(rfid_script)
    
    # Frontend startup script
    frontend_script = """#!/bin/bash
# AttenSync Frontend Startup Script

echo "Starting AttenSync Frontend..."
cd client
npm start
"""
    
    with open('start_frontend.sh', 'w', encoding='utf-8') as f:
        f.write(frontend_script)
    
    # Make scripts executable
    try:
        os.chmod('start_backend.sh', 0o755)
        os.chmod('start_rfid.sh', 0o755)
        os.chmod('start_frontend.sh', 0o755)
        print("  ✓ Created executable startup scripts")
    except:
        print("  ✓ Created startup scripts (Windows)")

def print_usage_instructions():
    """Print usage instructions"""
    print("\n🎉 AttenSync System Initialization Complete!")
    print("=" * 60)
    print("📚 Usage Instructions:")
    print()
    print("1. Start Backend Server:")
    print("   python backend.py")
    print("   → Available at: http://localhost:5000")
    print()
    print("2. Start RFID Listener:")
    print("   python rfid_system.py")
    print("   → Connects to ESP32 and processes RFID scans")
    print()
    print("3. Start Frontend (in new terminal):")
    print("   cd client && npm start")
    print("   → Available at: http://localhost:3000")
    print()
    print("🔑 Login Credentials:")
    print("   Admin: admin / admin123")
    print("   Teacher: teacher / teacher123")
    print()
    print("📊 Test Data:")
    print("   • 10 students with RFID tags (RFID001A - RFID010J)")
    print("   • 3 classes (5A, 5B, 6A)")
    print("   • 30 days of historical attendance")
    print("   • ML model ready for forecasting")
    print()
    print("🏷️ Test RFID Tags:")
    print("   RFID001A → Alice Johnson")
    print("   RFID002B → Bob Smith") 
    print("   RFID003C → Charlie Brown")
    print("   (and more...)")
    print()
    print("=" * 60)

def main():
    """Main initialization function"""
    print_banner()
    
    try:
        # Create Flask app
        app = create_flask_app()
        print("✅ Flask app created")
        
        # Initialize database
        init_database(app)
        print("✅ Database initialized")
        
        # Set up test data
        setup_test_data(app)
        print("✅ Test data created")
        
        # Test database operations
        stats = test_database_operations(app)
        print("✅ Database operations tested")
        
        # Test ML model
        ml_success = test_ml_model()
        if ml_success:
            print("✅ ML model tested")
        else:
            print("⚠️ ML model test completed with warnings")
        
        # Create startup scripts
        create_startup_scripts()
        print("✅ Startup scripts created")
        
        # Print usage instructions
        print_usage_instructions()
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

if __name__ == '__main__':
    success = main()
    if success:
        print("🎊 System ready for use!")
    else:
        print("💥 Initialization failed!")
        sys.exit(1)