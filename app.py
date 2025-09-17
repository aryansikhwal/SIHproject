from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime, date
import pandas as pd
from model import generate_forecast
import json

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:your_password@localhost/attendance_system"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create required directories
for directory in ['uploads', 'static']:
    if not os.path.exists(directory):
        os.makedirs(directory)

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
    method = db.Column(db.Enum('face_recognition', 'qr_code', 'manual'), nullable=False)
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
            
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
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
    
    return render_template('index.html',
                         total_students=total_students,
                         present_today=present_today,
                         weekly_data=weekly_data,
                         recent_activity=recent_activity)

@app.route('/attendance')
@login_required
def attendance():
    class_id = request.args.get('class_id')
    date_str = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    
    students = Student.query.filter_by(class_id=class_id).all() if class_id else []
    classes = Class.query.all()
    
    attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    attendance_records = {}
    
    if students:
        records = Attendance.query.filter_by(
            class_id=class_id,
            attendance_date=attendance_date
        ).all()
        attendance_records = {r.student_id: r.status for r in records}
    
    return render_template('attendance.html',
                         students=students,
                         classes=classes,
                         selected_class=class_id,
                         selected_date=date_str,
                         attendance_records=attendance_records)

@app.route('/mark_attendance', methods=['POST'])
@login_required
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
    return jsonify({'success': True})

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
@app.route('/students')
@login_required
def students():
    students = Student.query.all()
    classes = Class.query.all()
    return render_template('students.html', students=students, classes=classes)

@app.route('/reports')
@login_required
def reports():
    class_id = request.args.get('class_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Get attendance statistics
    query = db.session.query(
        Class.class_name,
        Class.section,
        db.func.count(Student.id).label('total_students'),
        db.func.count(Attendance.id).label('present_count')
    ).join(Student).outerjoin(
        Attendance, 
        db.and_(
            Attendance.student_id == Student.id,
            Attendance.status == 'present'
        )
    ).group_by(Class.id)
    
    if class_id:
        query = query.filter(Class.id == class_id)
    if start_date and end_date:
        query = query.filter(Attendance.attendance_date.between(start_date, end_date))
    
    stats = query.all()
    classes = Class.query.all()
    
    return render_template('reports.html', stats=stats, classes=classes)

@app.route('/trends')
@login_required
def trends():
    # Get attendance data for forecasting
    attendance_data = pd.DataFrame(
        db.session.query(
            Attendance.attendance_date,
            db.func.count().label('count')
        ).filter(
            Attendance.status == 'present'
        ).group_by(Attendance.attendance_date).all(),
        columns=['ds', 'y']
    )
    
    if len(attendance_data) > 0:
        # Generate forecast using Prophet
        forecast, fig1, fig2 = generate_forecast(attendance_data)
        
        # Save visualizations
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plot_path = f'static/forecast_plot_{timestamp}.png'
        trends_path = f'static/trends_plot_{timestamp}.png'
        
        fig1.savefig(plot_path)
        if fig2:
            fig2.savefig(trends_path)
        
        # Calculate trends and statistics
        trends_data = generate_attendance_trends()
        
        return render_template('trends.html',
                             trends_data=trends_data,
                             plot_path=plot_path,
                             trends_path=trends_path if fig2 else None)
    
    flash('Not enough attendance data for forecasting', 'error')
    return redirect(url_for('dashboard'))

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

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

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)