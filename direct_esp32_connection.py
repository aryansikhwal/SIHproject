#!/usr/bin/env python3
"""
Direct ESP32 Connection Attempt
Tries to connect directly to known ESP32 address
"""

import asyncio
from bleak import BleakClient
import logging
import sys
import os
from datetime import datetime

# Add project path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import db, Student, Attendance, RFIDScanLog
from backend import app

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Your ESP32 device address
ESP32_ADDRESS = "D4:8A:FC:C7:CF:72"
RFID_CHAR_UUID = "abcd1234-5678-90ab-cdef-1234567890ab"

class DirectESP32Connection:
    def __init__(self):
        self.client = None
        self.connected = False
        self.scans_processed = 0
    
    async def connect_directly(self):
        """Connect directly to ESP32 without scanning"""
        try:
            logger.info(f"Attempting direct connection to {ESP32_ADDRESS}...")
            
            self.client = BleakClient(ESP32_ADDRESS, timeout=15.0)
            await self.client.connect()
            
            if self.client.is_connected:
                self.connected = True
                logger.info("✅ Direct connection successful!")
                
                # List services
                services = self.client.services
                logger.info("Available services:")
                for service in services:
                    logger.info(f"  Service: {service.uuid}")
                    for char in service.characteristics:
                        props = ', '.join(char.properties)
                        logger.info(f"    Char: {char.uuid} ({props})")
                
                return True
            else:
                logger.error("Connection failed")
                return False
                
        except Exception as e:
            logger.error(f"Direct connection error: {e}")
            return False
    
    async def setup_notifications(self):
        """Setup RFID notifications"""
        try:
            def rfid_handler(sender, data):
                """Handle RFID data"""
                try:
                    self.scans_processed += 1
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    
                    # Decode data
                    try:
                        decoded = data.decode('utf-8').strip()
                        logger.info(f"🏷️ [{timestamp}] RFID: {decoded}")
                        
                        # Process in background
                        asyncio.create_task(self.process_rfid(decoded))
                        
                    except UnicodeDecodeError:
                        hex_data = data.hex()
                        logger.info(f"🏷️ [{timestamp}] RFID Binary: {hex_data}")
                        
                except Exception as e:
                    logger.error(f"Handler error: {e}")
            
            # Start notifications
            await self.client.start_notify(RFID_CHAR_UUID, rfid_handler)
            logger.info("🎯 RFID notifications active!")
            logger.info("📱 Ready for RFID card scans...")
            
            return True
            
        except Exception as e:
            logger.error(f"Notification setup failed: {e}")
            return False
    
    async def process_rfid(self, rfid_data):
        """Process RFID scan"""
        try:
            logger.info(f"Processing: {rfid_data}")
            
            # Extract RFID tag
            rfid_tag = rfid_data.strip()
            if 'RFID:' in rfid_data:
                rfid_tag = rfid_data.split('RFID:')[1].strip()
            
            # Update database
            with app.app_context():
                # Log scan
                scan_log = RFIDScanLog(
                    rfid_tag=rfid_tag,
                    scan_time=datetime.now(),
                    status='success'
                )
                
                # Find student
                student = Student.query.filter_by(rfid_tag=rfid_tag).first()
                
                if student:
                    scan_log.student_id = student.id
                    logger.info(f"✅ Student: {student.full_name}")
                    
                    # Mark attendance
                    today = datetime.now().date()
                    existing = Attendance.query.filter_by(
                        student_id=student.id,
                        attendance_date=today
                    ).first()
                    
                    if not existing:
                        attendance = Attendance(
                            student_id=student.id,
                            class_id=student.class_id,
                            teacher_id=1,
                            attendance_date=today,
                            method='rfid'
                        )
                        db.session.add(attendance)
                        scan_log.attendance_id = attendance.id
                        logger.info(f"✅ Attendance marked!")
                    else:
                        scan_log.status = 'already_marked'
                        logger.info(f"⚠️ Already marked today")
                else:
                    scan_log.status = 'invalid_tag'
                    logger.warning(f"❌ Unknown RFID: {rfid_tag}")
                
                db.session.add(scan_log)
                db.session.commit()
                
                logger.info(f"📊 Scans processed: {self.scans_processed}")
                
        except Exception as e:
            logger.error(f"Processing error: {e}")
    
    async def run_listener(self):
        """Main listener loop"""
        try:
            logger.info("🚀 AttenSync Direct ESP32 Connection")
            logger.info("="*50)
            
            # Connect
            if not await self.connect_directly():
                logger.error("❌ Failed to connect")
                return
            
            # Setup notifications
            if not await self.setup_notifications():
                logger.error("❌ Failed to setup notifications")
                return
            
            # Listen
            logger.info("🎯 System ready! Scan your RFID cards now!")
            logger.info("Press Ctrl+C to stop")
            
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("⏹️ Stopped by user")
        except Exception as e:
            logger.error(f"❌ System error: {e}")
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Cleanup"""
        if self.client and self.connected:
            try:
                await self.client.disconnect()
                logger.info("👋 Disconnected")
            except Exception as e:
                logger.error(f"Disconnect error: {e}")
        
        logger.info(f"🏁 Total scans: {self.scans_processed}")

async def main():
    connector = DirectESP32Connection()
    await connector.run_listener()

if __name__ == "__main__":
    asyncio.run(main())