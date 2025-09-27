"""
Fresh Flask backend for AttenSync
Clean API implementation with proper database connections
"""
from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from models import db, User, Class, Student, Attendance, RFIDScanLog, init_database, get_db_stats
from datetime import datetime, date, timedelta
import os
import json
import pandas as pd
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Configuration
app.config['SECRET_KEY'] = 'attensync-secret-key-2024'  # Change in production

# Use absolute path for database
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)
db_path = os.path.join(instance_path, 'attendance_system.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Enable CORS for all routes
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5000"],
        "supports_credentials": False,  # Temporarily disable credentials
        "allow_headers": ["Content-Type", "Authorization"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    }
})

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
init_database(app)

# Serve React static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.static_folder, 'static'), filename)

# ==================== API ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        stats = get_db_stats()
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': stats
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

# ==================== AUTH ROUTES ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict()
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """User logout"""
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current user info"""
    return jsonify({'user': current_user.to_dict()})

# ==================== STUDENT ROUTES ====================

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students with optional filtering"""
    try:
        class_id = request.args.get('class_id', type=int)
        search = request.args.get('search', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        query = Student.query.filter_by(is_active=True)
        
        if class_id:
            query = query.filter_by(class_id=class_id)
        
        if search:
            query = query.filter(
                db.or_(
                    Student.full_name.contains(search),
                    Student.roll_number.contains(search),
                    Student.rfid_tag.contains(search)
                )
            )
        
        students = query.order_by(Student.roll_number).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'students': [student.to_dict() for student in students.items],
            'total': students.total,
            'pages': students.pages,
            'current_page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students', methods=['POST'])
def create_student():
    """Create a new student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'roll_number', 'class_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if roll number already exists in the class
        existing_student = Student.query.filter_by(
            roll_number=data['roll_number'],
            class_id=data['class_id']
        ).first()
        
        if existing_student:
            return jsonify({'error': 'Roll number already exists in this class'}), 400
        
        # Check if RFID tag already exists (if provided)
        if data.get('rfid_tag'):
            existing_rfid = Student.query.filter_by(rfid_tag=data['rfid_tag']).first()
            if existing_rfid:
                return jsonify({'error': 'RFID tag already assigned to another student'}), 400
        
        student = Student(
            full_name=data['full_name'],
            roll_number=data['roll_number'],
            class_id=data['class_id'],
            rfid_tag=data.get('rfid_tag'),
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data.get('date_of_birth') else None,
            gender=data.get('gender'),
            parent_contact=data.get('parent_contact'),
            parent_email=data.get('parent_email'),
            address=data.get('address')
        )
        
        db.session.add(student)
        db.session.commit()
        
        return jsonify({
            'message': 'Student created successfully',
            'student': student.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a specific student"""
    try:
        student = Student.query.get_or_404(student_id)
        return jsonify({'student': student.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update a student"""
    try:
        student = Student.query.get_or_404(student_id)
        data = request.get_json()
        
        # Update fields
        if 'full_name' in data:
            student.full_name = data['full_name']
        if 'roll_number' in data:
            # Check for duplicate roll number in the same class
            existing = Student.query.filter(
                Student.roll_number == data['roll_number'],
                Student.class_id == student.class_id,
                Student.id != student_id
            ).first()
            if existing:
                return jsonify({'error': 'Roll number already exists in this class'}), 400
            student.roll_number = data['roll_number']
        
        if 'rfid_tag' in data:
            if data['rfid_tag']:  # Only check if not empty
                existing = Student.query.filter(
                    Student.rfid_tag == data['rfid_tag'],
                    Student.id != student_id
                ).first()
                if existing:
                    return jsonify({'error': 'RFID tag already assigned to another student'}), 400
            student.rfid_tag = data['rfid_tag']
        
        if 'date_of_birth' in data:
            student.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data['date_of_birth'] else None
        
        if 'gender' in data:
            student.gender = data['gender']
        if 'parent_contact' in data:
            student.parent_contact = data['parent_contact']
        if 'parent_email' in data:
            student.parent_email = data['parent_email']
        if 'address' in data:
            student.address = data['address']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Student updated successfully',
            'student': student.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student (soft delete)"""
    try:
        student = Student.query.get_or_404(student_id)
        student.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Student deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== ATTENDANCE ROUTES ====================

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    """Get attendance records with filtering"""
    try:
        class_id = request.args.get('class_id', type=int)
        student_id = request.args.get('student_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        
        query = Attendance.query
        
        if class_id:
            query = query.filter_by(class_id=class_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Attendance.attendance_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
        if end_date:
            query = query.filter(Attendance.attendance_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
        
        attendance = query.order_by(Attendance.attendance_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'attendance': [record.to_dict() for record in attendance.items],
            'total': attendance.total,
            'pages': attendance.pages,
            'current_page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/mark', methods=['POST'])
def mark_attendance():
    """Mark attendance for students"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        status = data.get('status', 'present')
        attendance_date = data.get('date', date.today().isoformat())
        method = data.get('method', 'manual')
        notes = data.get('notes', '')
        
        if not student_id:
            return jsonify({'error': 'student_id is required'}), 400
        
        # Get student and validate
        student = Student.query.get_or_404(student_id)
        attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
        
        # Check if attendance already exists for this date
        existing = Attendance.query.filter_by(
            student_id=student_id,
            attendance_date=attendance_date
        ).first()
        
        if existing:
            # Update existing record
            existing.status = status
            existing.method = method
            existing.notes = notes
            existing.updated_at = datetime.utcnow()
            existing.teacher_id = getattr(current_user, 'id', 1)  # Default to admin if no user
            
            db.session.commit()
            
            return jsonify({
                'message': 'Attendance updated successfully',
                'attendance': existing.to_dict()
            })
        else:
            # Create new record
            attendance = Attendance(
                student_id=student_id,
                class_id=student.class_id,
                teacher_id=getattr(current_user, 'id', 1),  # Default to admin if no user
                attendance_date=attendance_date,
                status=status,
                method=method,
                notes=notes
            )
            
            db.session.add(attendance)
            db.session.commit()
            
            return jsonify({
                'message': 'Attendance marked successfully',
                'attendance': attendance.to_dict()
            }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/bulk', methods=['POST'])
def bulk_mark_attendance():
    """Mark attendance for multiple students"""
    try:
        data = request.get_json()
        student_ids = data.get('student_ids', [])
        status = data.get('status', 'present')
        attendance_date = data.get('date', date.today().isoformat())
        method = data.get('method', 'manual')
        
        if not student_ids:
            return jsonify({'error': 'student_ids array is required'}), 400
        
        attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
        results = []
        
        for student_id in student_ids:
            try:
                student = Student.query.get(student_id)
                if not student:
                    results.append({'student_id': student_id, 'status': 'error', 'message': 'Student not found'})
                    continue
                
                # Check if attendance already exists
                existing = Attendance.query.filter_by(
                    student_id=student_id,
                    attendance_date=attendance_date
                ).first()
                
                if existing:
                    existing.status = status
                    existing.method = method
                    existing.updated_at = datetime.utcnow()
                    existing.teacher_id = getattr(current_user, 'id', 1)
                    results.append({'student_id': student_id, 'status': 'updated', 'attendance_id': existing.id})
                else:
                    attendance = Attendance(
                        student_id=student_id,
                        class_id=student.class_id,
                        teacher_id=getattr(current_user, 'id', 1),
                        attendance_date=attendance_date,
                        status=status,
                        method=method
                    )
                    db.session.add(attendance)
                    db.session.flush()  # Get the ID without committing
                    results.append({'student_id': student_id, 'status': 'created', 'attendance_id': attendance.id})
                    
            except Exception as e:
                results.append({'student_id': student_id, 'status': 'error', 'message': str(e)})
        
        db.session.commit()
        
        return jsonify({
            'message': 'Bulk attendance operation completed',
            'results': results
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== CLASS ROUTES ====================

@app.route('/api/classes', methods=['GET'])
def get_classes():
    """Get all active classes"""
    try:
        classes = Class.query.filter_by(is_active=True).order_by(Class.grade_level, Class.section).all()
        return jsonify({
            'classes': [cls.to_dict() for cls in classes]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/classes', methods=['POST'])
def create_class():
    """Create a new class"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'grade_level', 'teacher_id', 'academic_year']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        cls = Class(
            name=data['name'],
            grade_level=data['grade_level'],
            section=data.get('section', 'A'),
            teacher_id=data['teacher_id'],
            academic_year=data['academic_year']
        )
        
        db.session.add(cls)
        db.session.commit()
        
        return jsonify({
            'message': 'Class created successfully',
            'class': cls.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== RFID ROUTES ====================

@app.route('/api/rfid/scans', methods=['GET'])
def get_rfid_scans():
    """Get recent RFID scan logs"""
    try:
        limit = request.args.get('limit', 50, type=int)
        
        # Direct SQL query as fallback
        import sqlite3
        db_path = os.path.join('instance', 'attendance_system.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get today's date in the right format
        from datetime import date
        today = date.today().strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT r.rfid_tag, r.scan_time, r.status, r.student_id, r.id, 
                   COALESCE(r.student_name, s.full_name) as student_name
            FROM rfid_scan_logs r
            LEFT JOIN students s ON r.student_id = s.id
            WHERE DATE(r.scan_time) >= DATE('now', '-1 day')
            ORDER BY r.scan_time DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        scans = []
        for row in rows:
            scans.append({
                'id': row[4],
                'rfid_tag': row[0],
                'scan_time': row[1],
                'status': row[2],
                'student_id': row[3],
                'student_name': row[5]  # Now includes student name from JOIN
            })
        
        return jsonify({
            'scans': scans,
            'total': len(scans),
            'debug': f'Found {len(scans)} scans since yesterday'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        today = date.today()
        
        # Basic counts
        total_students = Student.query.filter_by(is_active=True).count()
        total_classes = Class.query.filter_by(is_active=True).count()
        
        # Today's attendance
        today_attendance = Attendance.query.filter_by(attendance_date=today).all()
        present_today = len([a for a in today_attendance if a.status == 'present'])
        absent_today = total_students - present_today
        
        # Weekly average
        week_ago = today - timedelta(days=7)
        weekly_attendance = db.session.query(Attendance.attendance_date, db.func.count(Attendance.id)).filter(
            Attendance.attendance_date >= week_ago,
            Attendance.attendance_date <= today,
            Attendance.status == 'present'
        ).group_by(Attendance.attendance_date).all()
        
        weekly_avg = sum([count for date, count in weekly_attendance]) / 7 if weekly_attendance else 0
        
        # Recent RFID scans
        recent_scans = RFIDScanLog.query.order_by(RFIDScanLog.scan_time.desc()).limit(10).all()
        
        return jsonify({
            'total_students': total_students,
            'total_classes': total_classes,
            'present_today': present_today,
            'absent_today': absent_today,
            'weekly_average': round(weekly_avg, 1),
            'attendance_percentage': round((present_today / total_students * 100), 1) if total_students > 0 else 0,
            'recent_rfid_scans': [scan.to_dict() for scan in recent_scans]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting AttenSync Backend Server...")
    print("📊 Dashboard: http://localhost:5000")
    print("🔌 API Health: http://localhost:5000/api/health")
    print("📚 API Docs: Available at /api/ endpoints")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)