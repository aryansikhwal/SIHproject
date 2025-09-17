import asyncio
from bleak import BleakScanner, BleakClient
import time
from datetime import datetime
from sqlalchemy import create_engine, text
import os
from app import db, Attendance, Student  # Import from your existing Flask app

# ESP32 RFID Reader characteristic UUID - Updated to match current ESP32 firmware
RFID_SERVICE_UUID = "12345678-1234-1234-1234-1234567890ab"  # Custom Service UUID from ESP32
RFID_CHAR_UUID = "abcd1234-5678-90ab-cdef-1234567890ab"     # Custom Characteristic UUID from ESP32

class RFIDReader:
    def __init__(self, device_address="D4:8A:FC:C7:CF:72", max_retries=3, retry_delay=5):
        self.device_address = device_address  # Your paired ESP32's MAC address
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.client = None
        self.device = None
        self.is_running = True

    async def start(self):
        """Start the RFID reader and listen for tags."""
        retries = self.max_retries
        
        while retries > 0 and self.is_running:
            try:
                print(f"Scanning for ESP32 ({self.device_address})...")
                
                # Scan with longer timeout and show all discovered devices
                device = None
                devices = await BleakScanner.discover(timeout=10.0)
                
                print("\nDiscovered devices:")
                for d in devices:
                    name = d.name or "Unknown"
                    print(f"  • {name} ({d.address})")
                    if d.address.upper() == self.device_address.upper():
                        device = d
                        print("    ↳ This is our ESP32!")
                print()
                
                if not device:
                    raise Exception("ESP32 not found. Please ensure it's powered on and in range")
                
                print(f"Found ESP32! Connecting...")
                self.client = BleakClient(device)
                
                # Try to connect
                await self.client.connect()
                if self.client.is_connected:
                    print("✓ Connected successfully!")
                
                # Try to start notifications immediately
                print("Looking for RFID service...")
                try:
                    # Start notification subscription
                    await self.client.start_notify(
                        RFID_CHAR_UUID,
                        self.notification_handler
                    )
                    print("✓ RFID service found and notifications enabled")
                except Exception as e:
                    raise Exception(f"RFID service error: {str(e)}")
                
                # Start listening for RFID tags
                await self._listen_for_tags()
                
            except Exception as e:
                retries -= 1
                print(f"Connection failed: {str(e)}")
                
                if retries > 0:
                    print(f"Retrying in {self.retry_delay} seconds... ({retries} attempts remaining)")
                    await asyncio.sleep(self.retry_delay)
                else:
                    print("Maximum retry attempts reached. Exiting...")
                    self.is_running = False
                    break
            
            except KeyboardInterrupt:
                print("\nProgram terminated by user.")
                break
            
            finally:
                await self.cleanup()

    def notification_handler(self, sender, data):
        """Handle incoming BLE notifications."""
        try:
            rfid_tag = data.decode().strip()
            if not rfid_tag:  # Skip empty data
                return
                
            current_time = datetime.now()
            print(f"\n🏷️  Tag detected: {rfid_tag}")
            print(f"⏰ Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            self._save_attendance(rfid_tag, current_time)
        except Exception as e:
            print(f"Error processing RFID data: {e}")
        finally:
            print("\nWaiting for next tag...")

    async def _listen_for_tags(self):
        """Listen for RFID tags and process them."""
        if not self.client.is_connected:
            raise Exception("Not connected to device")

        print("Listening for RFID tags...")
        print("Waiting for tags to be scanned...")
        
        try:
            # Start notification subscription
            await self.client.start_notify(
                RFID_CHAR_UUID,
                self.notification_handler
            )
            
            # Keep the connection alive
            while self.is_running and self.client.is_connected:
                await asyncio.sleep(0.1)  # Shorter sleep for better responsiveness
        except Exception as e:
            print(f"Error while listening for tags: {e}")
            raise

    def _save_attendance(self, rfid_tag, timestamp):
        """Save the attendance record to database."""
        try:
            student = Student.query.filter_by(rfid_tag=rfid_tag).first()
            
            if not student:
                print(f"No student found with RFID tag {rfid_tag}")
                return
            
            today_attendance = Attendance.query.filter(
                Attendance.student_id == student.id,
                Attendance.attendance_date == timestamp.date()
            ).first()
            
            if today_attendance:
                print(f"Attendance already marked for student {student.full_name} today")
                return
                
            new_attendance = Attendance(
                student_id=student.id,
                class_id=student.class_id,
                teacher_id=1,  # Default to admin user
                attendance_date=timestamp.date(),
                time_marked=timestamp,
                status='present',
                method='rfid',
                confidence_score=1.0,  # RFID is considered 100% accurate
                notes=f"Marked via RFID tag: {rfid_tag}"
            )
            
            db.session.add(new_attendance)
            db.session.commit()
            print(f"✓ Attendance marked for {student.full_name}")
                
        except Exception as e:
            db.session.rollback()
            print(f"Failed to save attendance record: {e}")

    async def cleanup(self):
        """Close the BLE connection."""
        if self.client and self.client.is_connected:
            try:
                await self.client.disconnect()
            except Exception as e:
                print(f"Error during disconnect: {e}")
            finally:
                print("Bluetooth connection closed.")

if __name__ == '__main__':
    print("╔════════════════════════════════╗")
    print("║     RFID Attendance System     ║")
    print("╚════════════════════════════════╝")
    print("\nInitializing...")
    print("Press Ctrl+C to stop")
    
    reader = RFIDReader()  # Uses the ESP32 MAC address we found
    
    try:
        asyncio.run(reader.start())
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        reader.is_running = False  # Signal the listener to stop
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        print("System shutdown complete.")