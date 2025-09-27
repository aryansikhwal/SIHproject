"""
AttenSync RFID System - Fixed Version
Handles missing dependencies gracefully and works with reorganized structure
"""
import sys
import os
import logging
import asyncio
from datetime import datetime, date

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rfid_listener.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import bleak
        logger.info("✅ bleak (Bluetooth LE) dependency found")
    except ImportError:
        missing_deps.append("bleak")
    
    try:
        import serial
        logger.info("✅ pyserial dependency found")
    except ImportError:
        missing_deps.append("pyserial")
    
    return missing_deps

def setup_database_connection():
    """Setup database connection with proper Flask app context"""
    try:
        # Add the backend directory to Python path
        backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        # Import Flask and models
        from flask import Flask
        from models import db, Student, Attendance, RFIDScanLog, init_database
        
        # Create Flask app for database context
        app = Flask(__name__)
        
        # Configure database
        basedir = os.path.abspath(os.path.dirname(__file__))
        instance_path = os.path.join(basedir, '..', '..', 'instance')
        os.makedirs(instance_path, exist_ok=True)
        db_path = os.path.join(instance_path, 'attensync.db')
        
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Initialize database
        db.init_app(app)
        
        logger.info("✅ Database connection established")
        return app, db, Student, Attendance, RFIDScanLog
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        return None, None, None, None, None

class RFIDSystem:
    """RFID System with BLE communication"""
    
    def __init__(self):
        self.app = None
        self.db = None
        self.Student = None
        self.Attendance = None
        self.RFIDScanLog = None
        self.running = False
        
        # ESP32 Configuration
        self.ESP32_NAME = "ESP32-RFID"
        self.ESP32_SERVICE_UUID = "12345678-1234-5678-9abc-123456789abc"
        self.ESP32_CHARACTERISTIC_UUID = "87654321-4321-8765-cba9-987654321cba"
        
    async def scan_for_esp32(self):
        """Scan for ESP32 device"""
        try:
            from bleak import BleakScanner
            
            logger.info("🔍 Scanning for ESP32 RFID device...")
            devices = await BleakScanner.discover(timeout=10.0)
            
            for device in devices:
                if device.name and self.ESP32_NAME.lower() in device.name.lower():
                    logger.info(f"✅ Found ESP32: {device.name} ({device.address})")
                    return device
                    
            logger.warning("⚠️  ESP32 RFID device not found")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error scanning for devices: {e}")
            return None
    
    async def connect_and_listen(self, device):
        """Connect to ESP32 and listen for RFID data"""
        try:
            from bleak import BleakClient
            
            async with BleakClient(device.address) as client:
                logger.info(f"🔗 Connected to {device.name}")
                
                # Check if service exists
                services = await client.get_services()
                service_found = False
                for service in services:
                    if service.uuid == self.ESP32_SERVICE_UUID:
                        service_found = True
                        break
                
                if not service_found:
                    logger.error("❌ RFID service not found on ESP32")
                    return
                
                # Setup notification handler
                def notification_handler(sender, data):
                    try:
                        rfid_data = data.decode('utf-8').strip()
                        logger.info(f"📡 RFID Card detected: {rfid_data}")
                        self.process_rfid_scan(rfid_data)
                    except Exception as e:
                        logger.error(f"❌ Error processing RFID data: {e}")
                
                # Start listening for notifications
                await client.start_notify(self.ESP32_CHARACTERISTIC_UUID, notification_handler)
                logger.info("👂 Listening for RFID cards...")
                
                # Keep connection alive
                while self.running:
                    await asyncio.sleep(1)
                    
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
    
    def process_rfid_scan(self, rfid_uid):
        """Process RFID scan and update attendance"""
        if not all([self.app, self.db, self.Student, self.Attendance, self.RFIDScanLog]):
            logger.error("❌ Database not properly initialized")
            return
        
        try:
            with self.app.app_context():
                # Log the scan
                scan_log = self.RFIDScanLog(
                    rfid_uid=rfid_uid,
                    scan_time=datetime.now(),
                    status='detected'
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
                        logger.info(f"👤 {student.name} already marked present today")
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
                        logger.info(f"✅ Attendance marked for {student.name}")
                        scan_log.status = 'success'
                else:
                    logger.warning(f"⚠️  Unknown RFID card: {rfid_uid}")
                    scan_log.status = 'unknown_card'
                
                self.db.session.commit()
                
        except Exception as e:
            logger.error(f"❌ Database error: {e}")
            if self.db:
                self.db.session.rollback()
    
    async def start_system(self):
        """Start the RFID system"""
        logger.info("🚀 Starting AttenSync RFID System...")
        
        # Check dependencies
        missing_deps = check_dependencies()
        if missing_deps:
            logger.error(f"❌ Missing dependencies: {', '.join(missing_deps)}")
            logger.error("Install with: pip install bleak pyserial")
            return False
        
        # Setup database
        self.app, self.db, self.Student, self.Attendance, self.RFIDScanLog = setup_database_connection()
        if not self.app:
            logger.error("❌ Database setup failed")
            return False
        
        # Initialize database tables
        with self.app.app_context():
            self.db.create_all()
            logger.info("✅ Database tables initialized")
        
        self.running = True
        
        try:
            while self.running:
                # Scan for ESP32
                device = await self.scan_for_esp32()
                if device:
                    await self.connect_and_listen(device)
                else:
                    logger.info("⏳ Retrying in 10 seconds...")
                    await asyncio.sleep(10)
                    
        except KeyboardInterrupt:
            logger.info("🛑 RFID System stopped by user")
        except Exception as e:
            logger.error(f"❌ System error: {e}")
        finally:
            self.running = False
        
        return True

def main():
    """Main entry point"""
    system = RFIDSystem()
    
    try:
        # Run the async system
        asyncio.run(system.start_system())
    except KeyboardInterrupt:
        logger.info("🛑 RFID System shutdown")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()