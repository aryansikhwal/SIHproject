"""
AttenSync # Configure logging with minimal console output
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings and errors in console
    format='%(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rfid_listener.log', level=logging.INFO),  # Full logs to file
        logging.StreamHandler()  # Minimal logs to console
    ]
)em - Windows Compatible Version
Handles missing dependencies gracefully and works with reorganized structure
"""
import sys
import os
import logging
import asyncio
from datetime import datetime, date
import colorama
from colorama import Fore, Back, Style

# Initialize colorama for Windows
colorama.init()

# Configure logging without Unicode characters
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
    bleak_available = False
    serial_available = False
    
    try:
        import bleak
        logger.info("[OK] bleak (Bluetooth LE) dependency found")
        bleak_available = True
    except ImportError:
        missing_deps.append("bleak")
    
    try:
        import serial
        logger.info("[OK] pyserial dependency found")
        serial_available = True
    except ImportError:
        missing_deps.append("pyserial")
    
    return missing_deps, bleak_available, serial_available

def setup_database_connection():
    """Setup database connection with proper Flask app context"""
    try:
        # Add the backend directory to Python path
        backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        # Import Flask and models
        from flask import Flask
        from models import db, Student, Attendance, RFIDScanLog
        
        # Create Flask app for database context
        app = Flask(__name__)
        
        # Configure database
        basedir = os.path.abspath(os.path.dirname(__file__))
        instance_path = os.path.join(basedir, '..', '..', 'instance')
        os.makedirs(instance_path, exist_ok=True)
        db_path = os.path.join(instance_path, 'attendance_system.db')  # Use same DB as backend
        
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Initialize database
        db.init_app(app)
        
        logger.info("[OK] Database connection established")
        return app, db, Student, Attendance, RFIDScanLog
        
    except Exception as e:
        logger.error(f"[ERROR] Database setup failed: {e}")
        return None, None, None, None, None

def print_banner():
    """Print clean banner for RFID system"""
    print(f"\n{Fore.CYAN}🔍 AttenSync RFID System - Ready{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Listening for card taps...{Style.RESET_ALL}\n")

def print_card_detected(rfid_uid, student_name=None, status=None):
    """Print clean RFID card detection"""
    if student_name:
        if status == "success":
            print(f"{Back.GREEN}{Fore.BLACK} ✅ {student_name} - ATTENDANCE MARKED {Style.RESET_ALL}")
        elif status == "duplicate":
            print(f"{Back.YELLOW}{Fore.BLACK} ⚠️  {student_name} - ALREADY PRESENT {Style.RESET_ALL}")
    else:
        print(f"{Back.RED}{Fore.WHITE} ❌ UNKNOWN CARD: {rfid_uid} {Style.RESET_ALL}")
    print()  # Add spacing

class RFIDSystem:
    """RFID System with BLE communication or demo mode"""
    
    def __init__(self, demo_mode=False):
        self.app = None
        self.db = None
        self.Student = None
        self.Attendance = None
        self.RFIDScanLog = None
        self.running = False
        self.demo_mode = demo_mode
        
        # ESP32 Configuration
        self.ESP32_NAME = "ESP32_BLE_RFID"  # Updated to match actual device name
        self.ESP32_ADDRESS = "D4:8A:FC:C7:CF:72"  # Known address from scan
        self.ESP32_SERVICE_UUID = "12345678-1234-1234-1234-1234567890ab"
        self.ESP32_CHARACTERISTIC_UUID = "abcd1234-5678-90ab-cdef-1234567890ab"
        
        # Demo RFID cards for testing
        self.demo_rfids = [
            "1234567890",
            "0987654321", 
            "1122334455",
            "5544332211"
        ]
        
    async def simulate_rfid_scanning(self):
        """Simulate RFID card scanning for demo purposes"""
        logger.info("[DEMO] Simulating RFID card scanning...")
        logger.info("[DEMO] This is demo mode - no actual hardware required")
        logger.info("[DEMO] Press Ctrl+C to stop")
        
        # Create demo students if they don't exist
        with self.app.app_context():
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
            logger.info("[DEMO] Demo students created/verified")
        
        scan_count = 0
        while self.running:
            try:
                # Wait 5-15 seconds between scans for demo
                import random
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
    
    async def scan_for_esp32(self):
        """Scan for ESP32 device"""
        try:
            from bleak import BleakScanner
            
            logger.info("[SCAN] Scanning for ESP32 RFID device...")
            devices = await BleakScanner.discover(timeout=10.0)
            
            for device in devices:
                device_name = device.name or ""
                device_addr = device.address or ""
                
                # Check for both name and address match
                if (device_name and self.ESP32_NAME.lower() in device_name.lower()) or \
                   (device_addr.upper() == self.ESP32_ADDRESS.upper()):
                    logger.info(f"[FOUND] ESP32: {device_name} ({device_addr})")
                    return device
                    
            logger.warning("[WARNING] ESP32 RFID device not found")
            logger.info(f"[INFO] Looking for device name: {self.ESP32_NAME} or address: {self.ESP32_ADDRESS}")
            return None
            
        except Exception as e:
            logger.error(f"[ERROR] Error scanning for devices: {e}")
            return None
    
    async def connect_and_listen(self, device):
        """Connect to ESP32 and listen for RFID data"""
        try:
            from bleak import BleakClient
            
            async with BleakClient(device.address) as client:
                logger.info(f"[CONNECT] Connected to {device.name}")
                
                # Get all services and try to find any notification characteristics
                services = client.services
                service_count = len(list(services))
                logger.info(f"[INFO] Found {service_count} services on ESP32")
                
                # Try each service and characteristic for notifications
                for service in services:
                    logger.info(f"[SERVICE] {service.uuid}")
                    for char in service.characteristics:
                        props = list(char.properties)
                        logger.info(f"  [CHAR] {char.uuid} - {props}")
                        
                        # Try to use any characteristic that supports notifications
                        if 'notify' in props:
                            try:
                                logger.info(f"[SETUP] Attempting to setup notifications on {char.uuid}")
                                
                                # Setup notification handler
                                def notification_handler(sender, data):
                                    try:
                                        rfid_data = data.decode('utf-8').strip()
                                        logger.info(f"[RFID] Card detected: {rfid_data}")
                                        student_name, status = self.process_rfid_scan(rfid_data)
                                        print_card_detected(rfid_data, student_name, status)
                                    except UnicodeDecodeError:
                                        # Handle binary data
                                        hex_data = data.hex().upper()
                                        logger.info(f"[RFID] Card detected (hex): {hex_data}")
                                        student_name, status = self.process_rfid_scan(hex_data)
                                        print_card_detected(hex_data, student_name, status)
                                    except Exception as e:
                                        logger.error(f"[ERROR] Error processing RFID data: {e}")
                                        print(f"{Fore.RED}❌ Error processing RFID data: {e}{Style.RESET_ALL}")
                                
                                # Start notifications
                                await client.start_notify(char.uuid, notification_handler)
                                logger.info(f"[SUCCESS] Notifications started on {char.uuid}")
                                logger.info("[LISTEN] Listening for RFID cards...")
                                
                                # Keep connection alive
                                while self.running:
                                    await asyncio.sleep(1)
                                
                                return  # Exit if successful
                                
                            except Exception as e:
                                logger.warning(f"[SKIP] Could not setup notifications on {char.uuid}: {e}")
                                continue
                
                # If we get here, no working notification characteristic was found
                logger.error("[ERROR] No working notification characteristics found")
                logger.info("[INFO] Trying alternative approach - checking all characteristics...")
                
                # Try ALL characteristics, even those without notify property
                for service in services:
                    for char in service.characteristics:
                        try:
                            logger.info(f"[ATTEMPT] Trying {char.uuid}")
                            
                            def notification_handler(sender, data):
                                try:
                                    rfid_data = data.decode('utf-8').strip()
                                    logger.info(f"[RFID] Card detected: {rfid_data}")
                                    student_name, status = self.process_rfid_scan(rfid_data)
                                    print_card_detected(rfid_data, student_name, status)
                                except UnicodeDecodeError:
                                    hex_data = data.hex().upper()
                                    logger.info(f"[RFID] Card detected (hex): {hex_data}")
                                    student_name, status = self.process_rfid_scan(hex_data)
                                    print_card_detected(hex_data, student_name, status)
                                except Exception as e:
                                    logger.error(f"[ERROR] Error processing RFID data: {e}")
                                    print(f"{Fore.RED}❌ Error processing RFID data: {e}{Style.RESET_ALL}")
                            
                            await client.start_notify(char.uuid, notification_handler)
                            logger.info(f"[SUCCESS] Alternative setup successful on {char.uuid}")
                            logger.info("[LISTEN] Listening for RFID cards...")
                            
                            while self.running:
                                await asyncio.sleep(1)
                            return
                            
                        except Exception as e:
                            continue
                
                logger.error("[ERROR] Could not setup notifications on any characteristic")
                    
        except Exception as e:
            logger.error(f"[ERROR] Connection error: {e}")
    
    def process_rfid_scan(self, rfid_uid):
        """Process RFID scan and update attendance"""
        if not all([self.app, self.db, self.Student, self.Attendance, self.RFIDScanLog]):
            logger.error("[ERROR] Database not properly initialized")
            return None, None
        
        try:
            with self.app.app_context():
                # Log the scan
                scan_log = self.RFIDScanLog(
                    rfid_tag=rfid_uid,  # Changed from rfid_uid to rfid_tag
                    scan_time=datetime.now(),
                    status='detected'
                )
                self.db.session.add(scan_log)
                
                # Find student by RFID
                student = self.Student.query.filter_by(rfid_tag=rfid_uid).first()  # Changed from rfid_uid to rfid_tag
                
                if student:
                    # Check if already marked present today
                    today = date.today()
                    existing_attendance = self.Attendance.query.filter_by(
                        student_id=student.id,
                        attendance_date=today  # Changed from date to attendance_date
                    ).first()
                    
                    if existing_attendance:
                        logger.info(f"[DUPLICATE] {student.full_name} already marked present today")
                        scan_log.status = 'already_marked'
                        scan_log.student_id = student.id
                        scan_log.student_name = student.full_name
                        self.db.session.commit()  # Commit the scan log
                        return student.full_name, "duplicate"
                    else:
                        # Mark attendance
                        attendance = self.Attendance(
                            student_id=student.id,
                            class_id=student.class_id,
                            teacher_id=1,  # Default teacher ID - should be configurable
                            attendance_date=today,
                            time_marked=datetime.now(),
                            status='present',
                            method='rfid'
                        )
                        self.db.session.add(attendance)
                        logger.info(f"[SUCCESS] Attendance marked for {student.full_name}")
                        scan_log.status = 'success'
                        scan_log.student_id = student.id
                        scan_log.student_name = student.full_name
                        scan_log.attendance_id = attendance.id  # Link the attendance record
                        self.db.session.commit()  # Commit both attendance and scan log
                        return student.full_name, "success"
                else:
                    logger.warning(f"[UNKNOWN] Unknown RFID card: {rfid_uid}")
                    scan_log.status = 'invalid_tag'
                    scan_log.error_message = f'No student found with RFID tag: {rfid_uid}'
                    self.db.session.commit()  # Commit the scan log even for unknown cards
                    return None, "unknown"
                
        except Exception as e:
            logger.error(f"[ERROR] Database error: {e}")
            if self.db:
                try:
                    self.db.session.rollback()
                except:
                    pass
            return None, "error"
    
    async def start_system(self):
        """Start the RFID system"""
        logger.info("[START] Starting AttenSync RFID System...")
        
        # Show colorful banner
        print_banner()
        
        # Check dependencies
        missing_deps, bleak_available, serial_available = check_dependencies()
        
        # Setup database
        self.app, self.db, self.Student, self.Attendance, self.RFIDScanLog = setup_database_connection()
        if not self.app:
            logger.error("[ERROR] Database setup failed")
            return False
        
        # Initialize database tables
        with self.app.app_context():
            self.db.create_all()
            logger.info("[OK] Database tables initialized")
        
        self.running = True
        
        # If hardware dependencies are missing, offer to run in demo mode
        if missing_deps:
            logger.warning(f"[WARNING] Missing dependencies: {', '.join(missing_deps)}")
            logger.info("[INFO] Hardware dependencies not available")
            logger.info("[INFO] To install: pip install bleak pyserial")
            
            # For now, let's try to install dependencies automatically
            try:
                logger.info("[INSTALL] Attempting to install missing dependencies...")
                import subprocess
                import sys
                
                for dep in missing_deps:
                    logger.info(f"[INSTALL] Installing {dep}...")
                    result = subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        logger.info(f"[SUCCESS] {dep} installed successfully")
                    else:
                        logger.error(f"[ERROR] Failed to install {dep}: {result.stderr}")
                
                # Re-check dependencies after installation
                missing_deps, bleak_available, serial_available = check_dependencies()
                
            except Exception as e:
                logger.error(f"[ERROR] Auto-installation failed: {e}")
        
        # If we still have missing dependencies, fall back to demo mode
        if missing_deps:
            logger.info("[FALLBACK] Running in demo/simulation mode")
            self.demo_mode = True
        
        try:
            if self.demo_mode or not bleak_available:
                await self.simulate_rfid_scanning()
            else:
                while self.running:
                    # Scan for ESP32
                    device = await self.scan_for_esp32()
                    if device:
                        await self.connect_and_listen(device)
                    else:
                        logger.info("[RETRY] Retrying in 10 seconds...")
                        await asyncio.sleep(10)
                    
        except KeyboardInterrupt:
            logger.info("[STOP] RFID System stopped by user")
        except Exception as e:
            logger.error(f"[ERROR] System error: {e}")
        finally:
            self.running = False
        
        return True

def main():
    """Main entry point"""
    logger.info("[INIT] AttenSync RFID System Starting...")
    
    # Try to auto-install dependencies first
    try:
        missing_deps, _, _ = check_dependencies()
        if missing_deps:
            logger.info("[SETUP] Attempting to install RFID dependencies...")
            import subprocess
            import sys
            
            # Try installing with different methods
            for dep in missing_deps:
                logger.info(f"[INSTALL] Installing {dep}...")
                
                # Try pip install first
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                                      capture_output=True, text=True)
                
                if result.returncode != 0:
                    # If that fails, try with --user flag
                    logger.info(f"[INSTALL] Retrying {dep} with --user flag...")
                    result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', dep], 
                                          capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"[SUCCESS] {dep} installed successfully")
                else:
                    logger.warning(f"[WARNING] Could not install {dep} - will run in demo mode")
                    logger.debug(f"Error: {result.stderr}")
    
    except Exception as e:
        logger.error(f"[ERROR] Dependency installation failed: {e}")
    
    system = RFIDSystem()
    
    try:
        # Run the async system
        asyncio.run(system.start_system())
    except KeyboardInterrupt:
        logger.info("[SHUTDOWN] RFID System shutdown")
    except Exception as e:
        logger.error(f"[FATAL] Fatal error: {e}")
        # Print full traceback for debugging
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()