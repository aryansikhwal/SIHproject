#!/usr/bin/env python3
"""
AttenSync ESP32 RFID System - Direct Connection
Enhanced BLE connection for ESP32 RFID system
"""

import asyncio
from bleak import BleakScanner, BleakClient
import logging
import time
from datetime import datetime
import sys
import os

# Add project path for models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import db, Student, Attendance, RFIDScanLog
from backend import app

# Configure logging without emojis (Windows compatibility)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ESP32 Configuration - Your specific device
ESP32_TARGET_ADDRESS = "D4:8A:FC:C7:CF:72"  # Your ESP32_BLE_RFID device
ESP32_TARGET_NAME = "ESP32_BLE_RFID"

# Service UUIDs (commonly used by ESP32)
RFID_SERVICE_UUID = "12345678-1234-1234-1234-1234567890ab"
RFID_CHAR_UUID = "abcd1234-5678-90ab-cdef-1234567890ab"

class AttenSyncRFIDListener:
    def __init__(self):
        self.client = None
        self.connected = False
        self.scanning = False
        self.scans_processed = 0
        
    async def find_esp32_device(self, max_attempts=5):
        """Find the specific ESP32 device"""
        for attempt in range(1, max_attempts + 1):
            logger.info(f"Scan attempt {attempt}/{max_attempts} for ESP32...")
            
            try:
                devices = await BleakScanner.discover(timeout=8.0)
                
                for device in devices:
                    device_name = device.name or "Unknown"
                    logger.info(f"Found device: {device.address} - {device_name}")
                    
                    # Check for our specific ESP32
                    if (device.address.upper() == ESP32_TARGET_ADDRESS.upper() or 
                        ESP32_TARGET_NAME in device_name):
                        logger.info(f"TARGET FOUND: {device.address} - {device_name}")
                        return device.address
                
                if attempt < max_attempts:
                    logger.info(f"Target device not found in scan {attempt}. Retrying...")
                    await asyncio.sleep(2)
                    
            except Exception as e:
                logger.error(f"Scan attempt {attempt} failed: {e}")
                await asyncio.sleep(1)
        
        return None
    
    async def connect_to_esp32(self, address):
        """Connect to ESP32 device"""
        try:
            logger.info(f"Connecting to ESP32 at {address}...")
            
            self.client = BleakClient(address, timeout=15.0)
            await self.client.connect()
            
            if self.client.is_connected:
                self.connected = True
                logger.info(f"Successfully connected to ESP32!")
                
                # Get device info
                try:
                    services = self.client.services
                    logger.info(f"Connected device has {len(services)} services:")
                    
                    for service in services:
                        logger.info(f"  Service: {service.uuid}")
                        for char in service.characteristics:
                            props = ', '.join(char.properties)
                            logger.info(f"    Char: {char.uuid} ({props})")
                    
                except Exception as e:
                    logger.error(f"Error getting services: {e}")
                
                return True
            else:
                logger.error("Connection established but client not connected")
                return False
                
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    async def setup_rfid_notifications(self):
        """Set up notifications for RFID data"""
        if not self.connected:
            logger.error("Not connected to device")
            return False
            
        try:
            # Look for notification-capable characteristics
            services = self.client.services
            notification_chars = []
            
            for service in services:
                for char in service.characteristics:
                    if 'notify' in char.properties:
                        notification_chars.append(char)
                        logger.info(f"Found notification char: {char.uuid}")
            
            if not notification_chars:
                logger.warning("No notification characteristics found")
                return False
            
            # Set up notification on the first suitable characteristic
            target_char = notification_chars[0]
            logger.info(f"Setting up notifications on: {target_char.uuid}")
            
            def rfid_notification_handler(sender, data):
                """Handle incoming RFID data"""
                try:
                    self.scans_processed += 1
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    
                    # Try to decode as text
                    try:
                        decoded_data = data.decode('utf-8').strip()
                        logger.info(f"[{timestamp}] RFID Data: {decoded_data}")
                        
                        # Process RFID scan
                        asyncio.create_task(self.process_rfid_scan(decoded_data))
                        
                    except UnicodeDecodeError:
                        # Handle binary data
                        hex_data = data.hex()
                        logger.info(f"[{timestamp}] RFID Binary: {hex_data}")
                        
                except Exception as e:
                    logger.error(f"Error processing RFID data: {e}")
            
            # Start notifications
            await self.client.start_notify(target_char.uuid, rfid_notification_handler)
            logger.info("RFID notifications active! Waiting for scans...")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup notifications: {e}")
            return False
    
    async def process_rfid_scan(self, rfid_data):
        """Process RFID scan and update database"""
        try:
            logger.info(f"Processing RFID scan: {rfid_data}")
            
            # Extract RFID tag from data
            rfid_tag = None
            if 'RFID:' in rfid_data:
                rfid_tag = rfid_data.split('RFID:')[1].strip()
            elif len(rfid_data.strip()) > 4:  # Assume the whole string is the tag
                rfid_tag = rfid_data.strip()
            
            if not rfid_tag:
                logger.warning(f"Could not extract RFID tag from: {rfid_data}")
                return
            
            logger.info(f"Extracted RFID tag: {rfid_tag}")
            
            # Update database in Flask app context
            with app.app_context():
                # Log the scan
                scan_log = RFIDScanLog(
                    rfid_tag=rfid_tag,
                    scan_time=datetime.now(),
                    status='success'
                )
                
                # Find student
                student = Student.query.filter_by(rfid_tag=rfid_tag).first()
                
                if student:
                    scan_log.student_id = student.id
                    logger.info(f"Student found: {student.full_name}")
                    
                    # Check if attendance already marked today
                    today = datetime.now().date()
                    existing_attendance = Attendance.query.filter_by(
                        student_id=student.id,
                        attendance_date=today
                    ).first()
                    
                    if not existing_attendance:
                        # Mark attendance
                        attendance = Attendance(
                            student_id=student.id,
                            class_id=student.class_id,
                            teacher_id=1,  # Default teacher
                            attendance_date=today,
                            method='rfid'
                        )
                        db.session.add(attendance)
                        scan_log.attendance_id = attendance.id
                        
                        logger.info(f"Attendance marked for {student.full_name}")
                    else:
                        scan_log.status = 'already_marked'
                        logger.info(f"Attendance already marked for {student.full_name}")
                        
                else:
                    scan_log.status = 'invalid_tag'
                    scan_log.error_message = f'No student found with RFID tag: {rfid_tag}'
                    logger.warning(f"No student found with RFID tag: {rfid_tag}")
                
                # Save scan log
                db.session.add(scan_log)
                db.session.commit()
                
                logger.info(f"Scan processed successfully! Total scans: {self.scans_processed}")
                
        except Exception as e:
            logger.error(f"Error processing RFID scan: {e}")
    
    async def run_rfid_system(self):
        """Main RFID system loop"""
        try:
            logger.info("Starting AttenSync RFID System...")
            logger.info("="*50)
            
            # Step 1: Find ESP32
            device_address = await self.find_esp32_device()
            if not device_address:
                logger.error("ESP32 device not found!")
                return
            
            # Step 2: Connect
            if not await self.connect_to_esp32(device_address):
                logger.error("Failed to connect to ESP32!")
                return
            
            # Step 3: Setup RFID notifications
            if not await self.setup_rfid_notifications():
                logger.error("Failed to setup RFID notifications!")
                return
            
            # Step 4: Listen for RFID scans
            logger.info("RFID system active! Scan your RFID tags...")
            logger.info("Press Ctrl+C to stop")
            
            self.scanning = True
            while self.scanning:
                await asyncio.sleep(1)  # Keep the system running
                
                # Print status every 30 seconds
                if self.scans_processed > 0 and self.scans_processed % 10 == 0:
                    logger.info(f"Status: {self.scans_processed} scans processed")
            
        except KeyboardInterrupt:
            logger.info("RFID system stopped by user")
        except Exception as e:
            logger.error(f"RFID system error: {e}")
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Cleanup connections"""
        self.scanning = False
        
        if self.client and self.connected:
            try:
                await self.client.disconnect()
                logger.info("Disconnected from ESP32")
            except Exception as e:
                logger.error(f"Disconnect error: {e}")
        
        self.connected = False
        logger.info(f"RFID system shutdown. Total scans processed: {self.scans_processed}")

async def main():
    """Main entry point"""
    rfid_system = AttenSyncRFIDListener()
    await rfid_system.run_rfid_system()

if __name__ == "__main__":
    asyncio.run(main())