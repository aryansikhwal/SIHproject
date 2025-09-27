from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
# Create a custom decorator that does nothing (to bypass login_required)
def login_required(f):
    return f
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from datetime import datetime, date
import pandas as pd
from model import generate_forecast
import json
import sqlite3

# Initialize Flask app
app = Flask(__name__, static_url_path='', static_folder='static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app, resources={r"/api/*": {
    "origins": "http://localhost:5001",
    "supports_credentials": True
}})  # Allow React frontend access with credentials

# Additional static folder for nested static files
app.static_folder = 'static'
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.static_folder, 'static'), filename)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(instance_path, 'attendance_system.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create required directories
for directory in ['uploads', 'static']:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Path for the separate RFID scan database
# RFID data now stored in main database via models

# RFID data now stored in main database via models
def init_rfid_db():
    """RFID scans now stored in main database via RFIDScanLog model"""
    pass

init_rfid_db()

# Database Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum('principal', 'teacher'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(10), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    academic_year = db.Column(db.String(10), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    students = db.relationship('Student', backref='class', lazy=True)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    roll_number = db.Column(db.String(10), nullable=False)
    father_name = db.Column(db.String(100))
    mother_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.Text)
    phone = db.Column(db.String(15))
    face_encoding = db.Column(db.Text)  # JSON string
    photo_filename = db.Column(db.String(255))
    qr_code = db.Column(db.Text)  # JSON string
    rfid_tag = db.Column(db.String(50), unique=True)  # RFID tag number
    enrollment_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    consent_given = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    attendance = db.relationship('Attendance', backref='student', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    time_marked = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('present', 'absent'), default='present')
    method = db.Column(db.Enum('face_recognition', 'qr_code', 'manual', 'rfid'), nullable=False)
    confidence_score = db.Column(db.Numeric(5, 3))
    photo_filename = db.Column(db.String(255))
    notes = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, default=False)

class AttendanceSession(db.Model):
    __tablename__ = 'attendance_sessions'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.DateTime, default=datetime.utcnow)
    photo_filename = db.Column(db.String(255), nullable=False)
    total_students_detected = db.Column(db.Integer, default=0)
    total_students_recognized = db.Column(db.Integer, default=0)
    processing_status = db.Column(db.Enum('pending', 'completed', 'failed'), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AttendanceForecast(db.Model):
    __tablename__ = 'attendance_forecast'
    id = db.Column(db.Integer, primary_key=True)
    forecast_date = db.Column(db.Date, unique=True, nullable=False)
    predicted_present = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RFIDScanLog(db.Model):
    __tablename__ = 'rfid_scan_log'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        required_columns = ['ds', 'y']
        
        # Check if required columns exist
        if not all(col in df.columns for col in required_columns):
            return False, "CSV must contain 'ds' and 'y' columns"
        
        # Validate date format
        try:
            pd.to_datetime(df['ds'])
        except:
            return False, "Date column 'ds' must be in YYYY-MM-DD format"
        
        # Validate attendance numbers
        if not pd.to_numeric(df['y'], errors='coerce').notnull().all():
            return False, "Attendance column 'y' must contain valid numbers"
            
        return True, "Valid CSV file"
    except Exception as e:
        return False, f"Error validating CSV: {str(e)}"

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    try:
        # Bypass login check - auto-login as admin
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("Admin user not found")
            return jsonify({
                'success': False,
                'message': 'Admin user not found. Please initialize the database.'
            }), 500
        
        print("Auto-login as admin")
        login_user(admin)
        return jsonify({
            'success': True,
            'user': {
                'id': admin.id,
                'username': admin.username,
                'full_name': admin.full_name,
                'email': admin.email,
                'role': admin.role
            },
            'token': 'dummy-jwt-token'  # In production, generate a real JWT token
        })
        
    except Exception as e:
        print(f"Error during login: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during login'
        }), 500

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # Bypass login for GET requests by serving the React frontend
    if request.method == 'GET':
        return send_from_directory(app.static_folder, 'index.html')
    
    # Handle POST requests for backward compatibility
    admin = User.query.filter_by(username='admin').first()
    if admin:
        login_user(admin)
        return jsonify({
            'success': True,
            'message': 'Auto-logged in as admin'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Admin user not found. Please initialize the database.'
        }), 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    # Handle API routes separately
    if path.startswith('api/'):
        return {"error": "Not Found"}, 404
    
    # Serve static files for specific assets
    if path and '.' in path:  # Likely a file with extension
        static_file = os.path.join(app.static_folder, path)
        if os.path.exists(static_file) and os.path.isfile(static_file):
            return send_from_directory(app.static_folder, path)
    
    # For all other routes, serve the React index.html to support client-side routing
    return send_from_directory(app.static_folder, 'index.html')

# Add explicit handlers for common static files
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(app.static_folder, 'manifest.json')

@app.route('/logo192.png')
def logo192():
    return send_from_directory(app.static_folder, 'logo192.png')

@app.route('/logo512.png')
def logo512():
    return send_from_directory(app.static_folder, 'logo512.png')

@app.route('/api/dashboard')
def get_dashboard_data():
    # Get today's date
    today = date.today()
    
    # Get class statistics
    total_students = Student.query.filter_by(is_active=True).count()
    present_today = Attendance.query.filter_by(
        attendance_date=today,
        status='present'
    ).count()
    
    # Calculate weekly attendance
    weekly_data = db.session.query(
        Attendance.attendance_date,
        db.func.count().label('count')
    ).filter(
        Attendance.status == 'present',
        Attendance.attendance_date >= date.today() - pd.Timedelta(days=7)
    ).group_by(Attendance.attendance_date).all()
    
    # Get recent activity
    recent_activity = AttendanceSession.query.order_by(
        AttendanceSession.created_at.desc()
    ).limit(5).all()
    
    return jsonify({
        'statistics': {
            'total_students': total_students,
            'present_today': present_today,
            'attendance_rate': (present_today / total_students * 100) if total_students > 0 else 0
        },
        'weekly_data': [{
            'date': data[0].strftime('%Y-%m-%d'),
            'count': data[1]
        } for data in weekly_data],
        'recent_activity': [{
            'id': activity.id,
            'class_id': activity.class_id,
            'date': activity.session_date.strftime('%Y-%m-%d'),
            'time': activity.session_time.strftime('%H:%M:%S'),
            'total_detected': activity.total_students_detected,
            'total_recognized': activity.total_students_recognized,
            'status': activity.processing_status
        } for activity in recent_activity]
    })

@app.route('/api/attendance')
def get_attendance():
    class_id = request.args.get('class')
    date_str = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    
    attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Get attendance records with student information
    records = db.session.query(Attendance, Student).join(
        Student, Attendance.student_id == Student.id
    ).filter(
        Attendance.class_id == class_id,
        Attendance.attendance_date == attendance_date
    ).all()
    
    # Format response with student details
    attendance_data = []
    for attendance, student in records:
        attendance_data.append({
            'student_id': student.id,
            'student_name': student.full_name,
            'roll_number': student.roll_number,
            'rfid_tag': student.rfid_tag,
            'status': attendance.status,
            'time_marked': attendance.time_marked.isoformat() if attendance.time_marked else None,
            'method': attendance.method,
            'is_verified': attendance.is_verified
        })
    
    return jsonify({
        'date': date_str,
        'class_id': class_id,
        'records': attendance_data
    })

@app.route('/api/attendance/today')
def get_today_attendance():
    """Get all RFID attendance for today"""
    today = date.today().strftime('%Y-%m-%d')
    
    # Get today's RFID attendance records with student information
    records = db.session.query(Attendance, Student).join(
        Student, Attendance.student_id == Student.id
    ).filter(
        Attendance.attendance_date == date.today(),
        Attendance.method == 'rfid'
    ).order_by(Attendance.time_marked.desc()).all()
    
    # Format response
    attendance_data = []
    for attendance, student in records:
        attendance_data.append({
            'student_id': student.id,
            'student_name': student.full_name,
            'roll_number': student.roll_number,
            'rfid_tag': student.rfid_tag,
            'status': attendance.status,
            'time_marked': attendance.time_marked.isoformat() if attendance.time_marked else None,
            'method': attendance.method,
            'class_name': student.class_info.name if student.class_info else 'Unknown'
        })
    
    return jsonify({
        'date': today,
        'total_rfid_scans': len(attendance_data),
        'records': attendance_data
    })

@app.route('/attendance')  # Route redirects to React frontend
def attendance_page():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    student_id = data.get('student_id')
    status = data.get('status')
    date_str = data.get('date')
    
    attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Update or create attendance record
    attendance = Attendance.query.filter_by(
        student_id=student_id,
        attendance_date=attendance_date
    ).first()
    
    if attendance:
        attendance.status = status
    else:
        student = Student.query.get(student_id)
        attendance = Attendance(
            student_id=student_id,
            class_id=student.class_id,
            teacher_id=current_user.id,
            attendance_date=attendance_date,
            status=status,
            method='manual'
        )
        db.session.add(attendance)
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Attendance marked successfully'})

@app.route('/upload_attendance', methods=['POST'])
@login_required
def upload_attendance():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('attendance'))
    
    file = request.files['file']
    class_id = request.form.get('class_id')
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('attendance'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Create attendance session
        session = AttendanceSession(
            class_id=class_id,
            teacher_id=current_user.id,
            session_date=date.today(),
            photo_filename=filename
        )
        db.session.add(session)
        db.session.commit()
        
        # Process attendance (face recognition would go here)
        # For now, just redirect back
        flash('Attendance file uploaded successfully', 'success')
        return redirect(url_for('attendance', class_id=class_id))
    
    flash('Invalid file type', 'error')
    return redirect(url_for('attendance'))

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        return send_file(f'static/{filename}', as_attachment=True)
    except Exception as e:
        flash('Error downloading file', 'error')
        return redirect(url_for('home'))

# API Endpoints
@app.route('/api/students')
def get_students():
    class_id = request.args.get('class')
    search_term = request.args.get('search')
    
    query = Student.query
    if class_id and class_id != 'all':
        query = query.filter_by(class_id=class_id)
    if search_term:
        query = query.filter(Student.full_name.ilike(f'%{search_term}%'))
    
    students = query.all()
    return jsonify([{
        'id': student.id,
        'student_id': student.student_id,
        'full_name': student.full_name,
        'class_id': student.class_id,
        'roll_number': student.roll_number,
        'father_name': student.father_name,
        'mother_name': student.mother_name,
        'phone': student.phone,
        'is_active': student.is_active
    } for student in students])

@app.route('/students')  # Route redirects to React frontend
def students_page():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/reports')
def reports():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/trends')
def trends():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/settings')
def settings():
    return send_from_directory(app.static_folder, 'index.html')

# Helper functions for trends analysis
def generate_attendance_trends():
    # Calculate various trends
    current_trend = calculate_current_trend()
    best_day = find_best_attendance_day()
    seasonal_peak = analyze_seasonal_patterns()
    accuracy = calculate_prediction_accuracy()
    
    return {
        'current_trend': current_trend,
        'best_day': best_day,
        'seasonal_peak': seasonal_peak,
        'accuracy': accuracy
    }

def calculate_current_trend():
    # Calculate attendance trend over the last 30 days
    thirty_days_ago = date.today() - pd.Timedelta(days=30)
    attendance_data = pd.DataFrame(
        db.session.query(
            Attendance.attendance_date,
            db.func.count().label('count')
        ).filter(
            Attendance.status == 'present',
            Attendance.attendance_date >= thirty_days_ago
        ).group_by(Attendance.attendance_date).all()
    )
    
    if len(attendance_data) > 0:
        recent_avg = attendance_data['count'].iloc[-7:].mean()
        past_avg = attendance_data['count'].iloc[:-7].mean()
        change = ((recent_avg - past_avg) / past_avg) * 100
        return {
            'direction': 'Improving' if change > 0 else 'Declining',
            'change': abs(change)
        }
    return None

def find_best_attendance_day():
    # Find the day with highest average attendance
    attendance_by_day = pd.DataFrame(
        db.session.query(
            db.func.dayofweek(Attendance.attendance_date).label('day'),
            db.func.count().label('count')
        ).filter(
            Attendance.status == 'present'
        ).group_by(
            db.func.dayofweek(Attendance.attendance_date)
        ).all()
    )
    
    if len(attendance_by_day) > 0:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        best_day_index = attendance_by_day['count'].argmax()
        return days[attendance_by_day['day'].iloc[best_day_index] - 1]
    return None

def analyze_seasonal_patterns():
    # Analyze attendance patterns by season
    attendance_by_month = pd.DataFrame(
        db.session.query(
            db.func.month(Attendance.attendance_date).label('month'),
            db.func.count().label('count')
        ).filter(
            Attendance.status == 'present'
        ).group_by(
            db.func.month(Attendance.attendance_date)
        ).all()
    )
    
    if len(attendance_by_month) > 0:
        seasons = {
            'Winter': [12, 1, 2],
            'Spring': [3, 4, 5],
            'Summer': [6, 7, 8],
            'Fall': [9, 10, 11]
        }
        month = attendance_by_month['month'].iloc[attendance_by_month['count'].argmax()]
        for season, months in seasons.items():
            if month in months:
                return season
    return None

def calculate_prediction_accuracy():
    # Here you would compare predicted vs actual attendance
    # This is a placeholder that could be improved with actual model validation
    return 87.3

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/forecast')
def get_forecast():
    forecasts = AttendanceForecast.query.order_by(AttendanceForecast.forecast_date).all()
    return jsonify([
        {
            'date': f.forecast_date.strftime('%Y-%m-%d'),
            'predicted_present': f.predicted_present
        } for f in forecasts
    ])

@app.route('/api/trigger_forecast', methods=['POST'])
def trigger_forecast():
    from model import generate_forecast_from_db
    generate_forecast_from_db()
    return jsonify({'success': True, 'message': 'Forecast updated.'})

@app.route('/api/test')
def test_endpoint():
    """Simple test endpoint"""
    return jsonify({'message': 'Backend is working!', 'timestamp': datetime.now().isoformat()})

@app.route('/api/rfid_scans')
def get_rfid_scans():
    """Get recent RFID attendance records - simplified version"""
    try:
        limit = int(request.args.get('limit', 10))
        
        # Simple query to get attendance records with RFID method
        records = Attendance.query.filter(
            Attendance.method == 'rfid'
        ).order_by(Attendance.time_marked.desc()).limit(limit).all()
        
        scan_data = []
        for record in records:
            # Get student info
            student = Student.query.get(record.student_id)
            scan_data.append({
                'id': record.id,
                'rfid_tag': student.rfid_tag if student else 'Unknown',
                'student_name': student.full_name if student else 'Unknown Student',
                'status': record.status,
                'timestamp': record.time_marked.strftime('%Y-%m-%d %H:%M:%S') if record.time_marked else 'N/A',
                'date': record.attendance_date.strftime('%Y-%m-%d') if record.attendance_date else 'N/A'
            })
        
        return jsonify({
            'scans': scan_data,
            'total': len(scan_data)
        })
    except Exception as e:
        return jsonify({'error': str(e), 'scans': [], 'total': 0}), 500

# Function to log RFID scan in both databases and mark attendance
def log_rfid_scan(tag, student_name):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = date.today()
    
    # Insert into main attendance_system.db via SQLAlchemy only
    scan = RFIDScanLog(tag=tag, student_name=student_name, timestamp=datetime.now())
    db.session.add(scan)
    
    # Mark attendance for the student
    student = Student.query.filter_by(full_name=student_name).first()
    if student:
        # Check if attendance already exists for today
        existing_attendance = Attendance.query.filter_by(
            student_id=student.id,
            attendance_date=today
        ).first()
        
        if existing_attendance:
            existing_attendance.status = 'present'
            existing_attendance.method = 'rfid'
            existing_attendance.time_marked = datetime.now()  # Update timestamp for when attendance was last modified
        else:
            # Create new attendance record
            attendance = Attendance(
                student_id=student.id,
                class_id=student.class_id,
                teacher_id=1,  # Using admin user as default
                attendance_date=today,
                status='present',
                method='rfid'
            )
            db.session.add(attendance)
    
    # Commit changes immediately to ensure real-time updates
    db.session.commit()

# Example API endpoint to trigger scan logging
@app.route('/api/scan_rfid', methods=['POST'])
def scan_rfid():
    data = request.json
    tag = data.get('tag')
    student_name = data.get('student_name')
    if not tag or not student_name:
        return jsonify({'success': False, 'message': 'Tag and student_name required'}), 400
    
    # Check if student exists before proceeding
    student = Student.query.filter_by(full_name=student_name).first()
    if not student:
        return jsonify({
            'success': False,
            'message': f'Student not found: {student_name}. Please add the student to the database first.',
            'scan': {
                'tag': tag,
                'student_name': student_name,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 404
    
    # Log the scan and mark attendance
    log_rfid_scan(tag, student_name)
    
    # Format response with student details and attendance status
    response = {
        'success': True,
        'message': f'RFID scan logged for {student_name}',
        'scan': {
            'tag': tag,
            'student_name': student_name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }
    
    # Add attendance details
    today = date.today()
    attendance = Attendance.query.filter_by(
        student_id=student.id,
        attendance_date=today
    ).first()
    
    if attendance:
        response['attendance'] = {
            'student_id': student.id,
            'status': attendance.status,
            'method': attendance.method,
            'date': today.strftime('%Y-%m-%d'),
            'time_marked': attendance.time_marked.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    return jsonify(response)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Initialize database and create admin user
def init_db():
    with app.app_context():
        try:
            print("Creating database tables...")
            db.create_all()
            print("Database tables created successfully")

            print("Checking for admin user...")
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("Creating admin user...")
                admin = User(
                    username='admin',
                    password_hash=generate_password_hash('admin123'),
                    full_name='Administrator',
                    email='admin@attensync.com',
                    role='principal'
                )
                db.session.add(admin)
                db.session.commit()
                print("Created admin user successfully")
            else:
                print("Admin user already exists")
        except Exception as e:
            print(f"Error during database initialization: {str(e)}")
            db.session.rollback()
            raise  # Re-raise the exception to see the full error

if __name__ == '__main__':
    init_db()
    # Use port 5001 since port 5000 is already in use by macOS AirPlay
    import sys
    port = 5001
    if len(sys.argv) > 1 and sys.argv[1].startswith('--port='):
        port = int(sys.argv[1].split('=')[1])
    app.run(debug=True, host='0.0.0.0', port=port)