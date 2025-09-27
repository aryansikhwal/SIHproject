"""
Fresh database models for AttenSync
Clean implementation with proper relationships and constraints
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for teachers/administrators"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='teacher')  # 'admin', 'teacher'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    classes_taught = db.relationship('Class', backref='teacher', lazy=True)
    attendance_records = db.relationship('Attendance', backref='marked_by', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Class(db.Model):
    """Class/Grade model"""
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # e.g., "Class 5A", "Grade 10"
    grade_level = db.Column(db.Integer, nullable=False)  # 1-12
    section = db.Column(db.String(10))  # A, B, C, etc.
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    academic_year = db.Column(db.String(10), nullable=False)  # e.g., "2024-25"
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    students = db.relationship('Student', backref='class_info', lazy=True, cascade='all, delete-orphan')
    attendance_records = db.relationship('Attendance', backref='class_info', lazy=True)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'grade_level': self.grade_level,
            'section': self.section,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher.full_name if self.teacher else None,
            'academic_year': self.academic_year,
            'is_active': self.is_active,
            'student_count': len(self.students),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Student(db.Model):
    """Student model"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(20), nullable=False)
    rfid_tag = db.Column(db.String(50), unique=True, nullable=True)  # RFID tag ID
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)  # 'male', 'female', 'other'
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    parent_contact = db.Column(db.String(15), nullable=True)
    parent_email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    enrollment_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add unique constraint for roll_number within a class
    __table_args__ = (db.UniqueConstraint('roll_number', 'class_id', name='unique_roll_per_class'),)
    
    # Relationships
    attendance_records = db.relationship('Attendance', backref='student_info', lazy=True, cascade='all, delete-orphan')
    
    def get_attendance_percentage(self, days=30):
        """Calculate attendance percentage for last N days"""
        from datetime import timedelta
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        total_records = Attendance.query.filter(
            Attendance.student_id == self.id,
            Attendance.attendance_date >= start_date,
            Attendance.attendance_date <= end_date
        ).count()
        
        if total_records == 0:
            return 0.0
            
        present_records = Attendance.query.filter(
            Attendance.student_id == self.id,
            Attendance.attendance_date >= start_date,
            Attendance.attendance_date <= end_date,
            Attendance.status == 'present'
        ).count()
        
        return round((present_records / total_records) * 100, 2)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'roll_number': self.roll_number,
            'rfid_tag': self.rfid_tag,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'class_id': self.class_id,
            'class_name': self.class_info.name if self.class_info else None,
            'parent_contact': self.parent_contact,
            'parent_email': self.parent_email,
            'address': self.address,
            'is_active': self.is_active,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'attendance_percentage': self.get_attendance_percentage(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Attendance(db.Model):
    """Attendance record model"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False, default=date.today)
    time_marked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(10), nullable=False, default='present')  # 'present', 'absent', 'late'
    method = db.Column(db.String(20), nullable=False, default='manual')  # 'rfid', 'manual', 'facial'
    confidence_score = db.Column(db.Float, default=1.0)  # 0.0 to 1.0
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ensure one attendance record per student per day
    __table_args__ = (db.UniqueConstraint('student_id', 'attendance_date', name='unique_attendance_per_day'),)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student_info.full_name if self.student_info else None,
            'student_roll': self.student_info.roll_number if self.student_info else None,
            'class_id': self.class_id,
            'class_name': self.class_info.name if self.class_info else None,
            'teacher_id': self.teacher_id,
            'teacher_name': self.marked_by.full_name if self.marked_by else None,
            'attendance_date': self.attendance_date.isoformat() if self.attendance_date else None,
            'time_marked': self.time_marked.isoformat() if self.time_marked else None,
            'status': self.status,
            'method': self.method,
            'confidence_score': self.confidence_score,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class RFIDScanLog(db.Model):
    """Log of all RFID scans (including invalid ones)"""
    __tablename__ = 'rfid_scan_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    rfid_tag = db.Column(db.String(50), nullable=False)
    scan_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)  # NULL if invalid tag
    student_name = db.Column(db.String(100), nullable=True)  # Store student name for quick access
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendance.id'), nullable=True)  # NULL if already marked
    status = db.Column(db.String(20), nullable=False)  # 'success', 'invalid_tag', 'already_marked', 'error'
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student_info = db.relationship('Student', backref='rfid_scans', lazy=True)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'rfid_tag': self.rfid_tag,
            'student_name': self.student_name,
            'scan_time': self.scan_time.isoformat() if self.scan_time else None,
            'student_id': self.student_id,
            'attendance_id': self.attendance_id,
            'status': self.status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

def init_database(app):
    """Initialize database with app context"""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default admin user if not exists
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
            db.session.commit()  # Commit admin first
            
            # Create a default class
            default_class = Class(
                name='Demo Class',
                grade_level=5,
                section='A',
                teacher_id=admin.id,
                academic_year='2024-25'
            )
            db.session.add(default_class)
            
            try:
                db.session.commit()
                print("✓ Database initialized with default admin user and class")
            except Exception as e:
                db.session.rollback()
                print(f"✗ Error initializing database: {e}")
        else:
            print("✓ Database already initialized")

def get_db_stats():
    """Get database statistics"""
    try:
        return {
            'users': User.query.count(),
            'classes': Class.query.count(),
            'students': Student.query.count(),
            'attendance_records': Attendance.query.count(),
            'rfid_scans': RFIDScanLog.query.count()
        }
    except Exception as e:
        return {'error': str(e)}