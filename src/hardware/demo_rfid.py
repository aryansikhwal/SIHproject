#!/usr/bin/env python3#!/usr/bin/env python3

""""""

AttenSync RFID System - Demo/Development VersionAttenSync RFID System - Demo/Development Version

Runs without hardware dependencies for testing and developmentRuns without hardware dependencies for testing and development

""""""

import sysimport sys

import osimport os

import loggingimport logging

import asyncioimport asyncio

import randomimport random

import timeimport time

from datetime import datetime, datefrom datetime import datetime, date



# Configure logging# Configure logging

logging.basicConfig(logging.basicConfig(

    level=logging.INFO,    level=logging.INFO,

    format='%(asctime)s - %(levelname)s - %(message)s',    format='%(asctime)s - %(levelname)s - %(message)s',

    handlers=[    handlers=[

        logging.FileHandler('rfid_demo.log'),        logging.FileHandler('rfid_demo.log'),

        logging.StreamHandler(sys.stdout)        logging.StreamHandler(sys.stdout)

    ]    ]

))



logger = logging.getLogger(__name__)logger = logging.getLogger(__name__)



def setup_database_connection():def setup_database_connection():

    """Setup database connection with proper Flask app context"""    """Setup database connection with proper Flask app context"""

    try:    try:

        # Add the backend directory to Python path        # Add the backend directory to Python path

        backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')        backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')

        if backend_path not in sys.path:        if backend_path not in sys.path:

            sys.path.insert(0, backend_path)            sys.path.insert(0, backend_path)

                

        # Import Flask and models        # Import Flask and models

        from flask import Flask        from flask import Flask

        from models import db, Student, Attendance, RFIDScanLog        from models import db, Student, Attendance, RFIDScanLog

                

        # Create Flask app for database context        # Create Flask app for database context

        app = Flask(__name__)        app = Flask(__name__)

                

        # Configure database        # Configure database

        basedir = os.path.abspath(os.path.dirname(__file__))        basedir = os.path.abspath(os.path.dirname(__file__))

        instance_path = os.path.join(basedir, '..', '..', 'instance')        instance_path = os.path.join(basedir, '..', '..', 'instance')

        os.makedirs(instance_path, exist_ok=True)        os.makedirs(instance_path, exist_ok=True)

        db_path = os.path.join(instance_path, 'attensync.db')        db_path = os.path.join(instance_path, 'attensync.db')

                

        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

                

        # Initialize database        # Initialize database

        db.init_app(app)        db.init_app(app)

                

        logger.info("[OK] Database connection established")        logger.info("[OK] Database connection established")

        return app, db, Student, Attendance, RFIDScanLog        return app, db, Student, Attendance, RFIDScanLog

                

    except Exception as e:    except Exception as e:

        logger.error(f"[ERROR] Database setup failed: {e}")        logger.error(f"[ERROR] Database setup failed: {e}")

        return None, None, None, None, None        return None, None, None, None, None

            student_id=student.id

class RFIDSystemDemo:        )

    """RFID System Demo - simulates hardware for testing"""        db.session.add(scan)

            

    def __init__(self):        # Mark attendance

        self.app = None        today = datetime.date.today()

        self.db = None        existing_attendance = Attendance.query.filter_by(

        self.Student = None            student_id=student.id,

        self.Attendance = None            attendance_date=today

        self.RFIDScanLog = None        ).first()

        self.running = False        

                if not existing_attendance:

        # Demo RFID cards for testing            attendance = Attendance(

        self.demo_rfids = [                student_id=student.id,

            "1234567890",                class_id=student.class_id,

            "0987654321",                 teacher_id=1,

            "1122334455",                attendance_date=today,

            "5544332211"                method='rfid'

        ]            )

                db.session.add(attendance)

    def process_rfid_scan(self, rfid_uid):            scan.attendance_id = attendance.id

        """Process RFID scan and update attendance"""            print(f"✅ Attendance marked successfully!")

        if not all([self.app, self.db, self.Student, self.Attendance, self.RFIDScanLog]):        else:

            logger.error("[ERROR] Database not properly initialized")            scan.status = 'already_marked'

            return            print(f"⚠️  Attendance already marked for today")

                

        try:        db.session.commit()

            with self.app.app_context():        

                # Log the scan        print(f"📊 Total scans in system: {RFIDScanLog.query.count()}")

                scan_log = self.RFIDScanLog(        print(f"📈 Total attendance records: {Attendance.query.count()}")

                    rfid_uid=rfid_uid,        

                    scan_time=datetime.now(),    else:

                    status='detected'        print("❌ No student found with RFID tag RFID001A")
                )
                self.db.session.add(scan_log)
                
                # Find student by RFID
                student = self.Student.query.filter_by(rfid_uid=rfid_uid).first()
                
                if student:
                    # Check if already marked present today
                    today = date.today()
                    existing_attendance = self.Attendance.query.filter_by(
                        student_id=student.id,
                        date=today
                    ).first()
                    
                    if existing_attendance:
                        logger.info(f"[DUPLICATE] {student.name} already marked present today")
                        scan_log.status = 'duplicate'
                    else:
                        # Mark attendance
                        attendance = self.Attendance(
                            student_id=student.id,
                            date=today,
                            time_in=datetime.now(),
                            status='present'
                        )
                        self.db.session.add(attendance)
                        logger.info(f"[SUCCESS] Attendance marked for {student.name}")
                        scan_log.status = 'success'
                else:
                    logger.warning(f"[UNKNOWN] Unknown RFID card: {rfid_uid}")
                    scan_log.status = 'unknown_card'
                
                self.db.session.commit()
                
        except Exception as e:
            logger.error(f"[ERROR] Database error: {e}")
            if self.db:
                self.db.session.rollback()
    
    async def simulate_rfid_scanning(self):
        """Simulate RFID card scanning for demo purposes"""
        logger.info("[DEMO] Simulating RFID card scanning...")
        logger.info("[DEMO] This is a demo mode - no actual hardware required")
        logger.info("[DEMO] Press Ctrl+C to stop")
        
        scan_count = 0
        while self.running:
            try:
                # Wait 5-15 seconds between scans for demo
                wait_time = random.randint(5, 15)
                await asyncio.sleep(wait_time)
                
                # Simulate a random RFID scan
                rfid_uid = random.choice(self.demo_rfids)
                logger.info(f"[DEMO] Simulating RFID scan: {rfid_uid}")
                self.process_rfid_scan(rfid_uid)
                
                scan_count += 1
                if scan_count % 3 == 0:
                    logger.info(f"[DEMO] {scan_count} scans processed so far...")
                
            except Exception as e:
                logger.error(f"[ERROR] Simulation error: {e}")
                await asyncio.sleep(5)
    
    async def start_system(self):
        """Start the RFID system in demo mode"""
        logger.info("[START] Starting AttenSync RFID System (Demo Mode)")
        
        # Setup database
        self.app, self.db, self.Student, self.Attendance, self.RFIDScanLog = setup_database_connection()
        if not self.app:
            logger.error("[ERROR] Database setup failed")
            return False
        
        # Initialize database tables
        with self.app.app_context():
            self.db.create_all()
            logger.info("[OK] Database tables initialized")
            
            # Create demo students if they don't exist
            for i, rfid in enumerate(self.demo_rfids):
                existing = self.Student.query.filter_by(rfid_uid=rfid).first()
                if not existing:
                    student = self.Student(
                        name=f"Demo Student {i+1}",
                        student_id=f"DEMO{i+1:03d}",
                        rfid_uid=rfid
                    )
                    self.db.session.add(student)
            
            self.db.session.commit()
            logger.info("[OK] Demo students created/verified")
        
        self.running = True
        
        try:
            await self.simulate_rfid_scanning()
                    
        except KeyboardInterrupt:
            logger.info("[STOP] RFID System stopped by user")
        except Exception as e:
            logger.error(f"[ERROR] System error: {e}")
        finally:
            self.running = False
        
        return True

def main():
    """Main entry point"""
    logger.info("[DEMO] AttenSync RFID Demo System")
    logger.info("[DEMO] This version runs without hardware dependencies")
    logger.info("[DEMO] For production use, install: pip install bleak pyserial")
    
    system = RFIDSystemDemo()
    
    try:
        # Run the async system
        asyncio.run(system.start_system())
    except KeyboardInterrupt:
        logger.info("[SHUTDOWN] RFID System shutdown")
    except Exception as e:
        logger.error(f"[FATAL] Fatal error: {e}")

if __name__ == "__main__":
    main()