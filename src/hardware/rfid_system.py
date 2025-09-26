"""
Fresh RFID Listener for AttenSync
Clean implementation with proper database logging and error handling
"""
import asyncio
from bleak import BleakScanner, BleakClient
import sys
import os
from datetime import datetime, date
import logging

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import models with proper Flask app context
from flask import Flask
from models import db, Student, Attendance, RFIDScanLog, init_database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rfid_listener.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# ESP32 Configuration
ESP32_CONFIG = {
    'service_uuid': "12345678-1234-1234-1234-1234567890ab",
    'characteristic_uuid': "abcd1234-5678-90ab-cdef-1234567890ab",
    'device_name': "ESP32_BLE_RFID",
    'device_address': None,  # Will be discovered dynamically
    'connection_timeout': 10.0,
    'scan_timeout': 5.0,
    'max_retries': 5,
    'retry_delay': 3.0
}

class RFIDAttendanceSystem:
    def __init__(self):
        """Initialize the RFID attendance system"""
        self.app = None
        self.db = None
        self.client = None
        self.is_running = True
        self.connection_attempts = 0
        self.total_scans_processed = 0
        
        # Initialize Flask app for database access
        self._init_flask_app()
        
        logger.info("🏷️ RFID Attendance System initialized")

    def _init_flask_app(self):
        """Initialize Flask app context for database operations"""
        try:
            self.app = Flask(__name__)
            self.app.config['SECRET_KEY'] = 'attensync-rfid-key'
            
            # Use absolute path for database
            project_root = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(project_root, 'instance', 'attensync.db')
            self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
            self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            
            # Initialize database
            init_database(self.app)
            self.db = db
            
            logger.info("✓ Database connection established")
            
            # Test database connectivity
            with self.app.app_context():
                student_count = Student.query.count()
                logger.info(f"📊 Found {student_count} students in database")
                
        except Exception as e:
            logger.error(f"✗ Failed to initialize database: {e}")
            raise

    async def scan_for_esp32(self):
        """Scan for ESP32 device and return its address"""
        logger.info("🔍 Scanning for ESP32 device...")
        
        try:
            devices = await BleakScanner.discover(timeout=ESP32_CONFIG['scan_timeout'])
            
            for device in devices:
                if device.name == ESP32_CONFIG['device_name']:
                    logger.info(f"✓ Found ESP32: {device.name} ({device.address})")
                    return device.address
                    
            # If exact name not found, look for any device with ESP32 in name
            for device in devices:
                if device.name and "ESP32" in device.name.upper():
                    logger.info(f"✓ Found ESP32-like device: {device.name} ({device.address})")
                    return device.address
            
            logger.warning("⚠️ ESP32 device not found in scan")
            return None
            
        except Exception as e:
            logger.error(f"✗ Scan error: {e}")
            return None

    async def connect_to_esp32(self, device_address):
        """Connect to ESP32 and set up notifications"""
        try:
            logger.info(f"🔗 Connecting to ESP32 at {device_address}...")
            
            self.client = BleakClient(device_address, timeout=ESP32_CONFIG['connection_timeout'])
            await self.client.connect()
            
            if not self.client.is_connected:
                raise Exception("Failed to establish connection")
            
            logger.info("✓ Connected to ESP32")
            
            # Set up notifications
            logger.info("📡 Setting up RFID notifications...")
            await self.client.start_notify(
                ESP32_CONFIG['characteristic_uuid'],
                self._handle_rfid_notification
            )
            
            logger.info("✓ RFID notifications enabled")
            return True
            
        except Exception as e:
            logger.error(f"✗ Connection failed: {e}")
            await self._cleanup_connection()
            return False

    def _handle_rfid_notification(self, sender, data):
        """Handle incoming RFID data from ESP32"""
        try:
            # Decode RFID tag
            rfid_tag = data.decode('utf-8').strip()
            
            if not rfid_tag:
                logger.warning("⚠️ Received empty RFID data")
                return
            
            scan_time = datetime.utcnow()
            self.total_scans_processed += 1
            
            logger.info(f"🏷️ RFID Tag Scanned: {rfid_tag}")
            
            # Process attendance in Flask app context
            with self.app.app_context():
                self._process_attendance(rfid_tag, scan_time)
                
        except Exception as e:
            logger.error(f"✗ Error processing RFID notification: {e}")

    def _process_attendance(self, rfid_tag, scan_time):
        """Process attendance marking for RFID tag"""
        try:
            # Log the scan attempt
            scan_log = RFIDScanLog(
                rfid_tag=rfid_tag,
                scan_time=scan_time,
                status='processing'
            )
            
            # Find student by RFID tag
            student = Student.query.filter_by(rfid_tag=rfid_tag, is_active=True).first()
            
            if not student:
                scan_log.status = 'invalid_tag'
                scan_log.error_message = f'No active student found for RFID tag: {rfid_tag}'
                self.db.session.add(scan_log)
                self.db.session.commit()
                
                logger.warning(f"⚠️ Unknown RFID tag: {rfid_tag}")
                return
            
            scan_log.student_id = student.id
            logger.info(f"👤 Student found: {student.full_name} (Roll: {student.roll_number})")
            
            # Check if attendance already marked today
            today = scan_time.date()
            existing_attendance = Attendance.query.filter_by(
                student_id=student.id,
                attendance_date=today
            ).first()
            
            if existing_attendance:
                scan_log.status = 'already_marked'
                scan_log.attendance_id = existing_attendance.id
                scan_log.error_message = f'Attendance already marked as {existing_attendance.status}'
                self.db.session.add(scan_log)
                self.db.session.commit()
                
                logger.info(f"ℹ️ Attendance already marked for {student.full_name} today ({existing_attendance.status})")
                return
            
            # Mark attendance
            attendance = Attendance(
                student_id=student.id,
                class_id=student.class_id,
                teacher_id=1,  # System/RFID user
                attendance_date=today,
                time_marked=scan_time,
                status='present',
                method='rfid',
                confidence_score=1.0,
                notes=f'Auto-marked via RFID: {rfid_tag}'
            )
            
            self.db.session.add(attendance)
            self.db.session.flush()  # Get the attendance ID
            
            # Update scan log with success
            scan_log.status = 'success'
            scan_log.attendance_id = attendance.id
            self.db.session.add(scan_log)
            
            # Commit all changes
            self.db.session.commit()
            
            logger.info(f"✅ Attendance marked: {student.full_name} - Present")
            logger.info(f"📝 Class: {student.class_info.name if student.class_info else 'Unknown'}")
            
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"✗ Error processing attendance: {e}")
            
            # Log the error
            try:
                error_log = RFIDScanLog(
                    rfid_tag=rfid_tag,
                    scan_time=scan_time,
                    status='error',
                    error_message=str(e)
                )
                self.db.session.add(error_log)
                self.db.session.commit()
            except:
                pass  # Don't cascade errors

    async def run_attendance_system(self):
        """Main loop for the attendance system"""
        logger.info("🚀 Starting RFID Attendance System...")
        logger.info("📍 Press Ctrl+C to stop")
        
        while self.is_running:
            try:
                self.connection_attempts += 1
                logger.info(f"🔄 Connection attempt #{self.connection_attempts}")
                
                # Scan for ESP32
                device_address = await self.scan_for_esp32()
                
                if not device_address:
                    if self.connection_attempts >= ESP32_CONFIG['max_retries']:
                        logger.error("❌ Maximum connection attempts reached. Exiting...")
                        break
                    
                    logger.info(f"⏳ Retrying in {ESP32_CONFIG['retry_delay']} seconds...")
                    await asyncio.sleep(ESP32_CONFIG['retry_delay'])
                    continue
                
                # Connect to ESP32
                if await self.connect_to_esp32(device_address):
                    logger.info("🎉 RFID system ready! Waiting for tag scans...")
                    
                    # Reset connection attempts on successful connection
                    self.connection_attempts = 0
                    
                    # Keep connection alive and process notifications
                    try:
                        while self.is_running and self.client.is_connected:
                            await asyncio.sleep(0.1)
                    except asyncio.CancelledError:
                        logger.info("📋 System shutdown requested")
                        break
                    except Exception as e:
                        logger.error(f"✗ Connection lost: {e}")
                
                await self._cleanup_connection()
                
                if self.is_running:
                    logger.info(f"⏳ Reconnecting in {ESP32_CONFIG['retry_delay']} seconds...")
                    await asyncio.sleep(ESP32_CONFIG['retry_delay'])
                
            except KeyboardInterrupt:
                logger.info("\n🛑 Shutdown requested by user")
                break
            except Exception as e:
                logger.error(f"✗ Unexpected error: {e}")
                await asyncio.sleep(ESP32_CONFIG['retry_delay'])
        
        await self._cleanup_connection()
        logger.info(f"📊 Total RFID scans processed: {self.total_scans_processed}")
        logger.info("👋 RFID Attendance System stopped")

    async def _cleanup_connection(self):
        """Clean up BLE connection"""
        if self.client:
            try:
                if self.client.is_connected:
                    await self.client.disconnect()
                logger.info("🔌 Connection cleaned up")
            except Exception as e:
                logger.error(f"✗ Cleanup error: {e}")
            finally:
                self.client = None

    def stop(self):
        """Stop the attendance system"""
        self.is_running = False

# ==================== MAIN EXECUTION ====================

def print_startup_banner():
    """Print startup banner"""
    print("╔" + "="*48 + "╗")
    print("║" + " RFID ATTENDANCE SYSTEM - AttenSync ".center(48) + "║")
    print("╠" + "="*48 + "╣")
    print("║" + f" Version: 2.0 | Fresh Database Integration ".ljust(48) + "║")
    print("║" + f" ESP32 BLE | Auto-Attendance Marking ".ljust(48) + "║")
    print("╚" + "="*48 + "╝")
    print()

async def main():
    """Main function"""
    print_startup_banner()
    
    # Initialize system
    rfid_system = RFIDAttendanceSystem()
    
    try:
        # Run the attendance system
        await rfid_system.run_attendance_system()
    except KeyboardInterrupt:
        logger.info("🛑 Interrupted by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
    finally:
        rfid_system.stop()
        logger.info("🏁 System shutdown complete")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)