import asyncio
from bleak import BleakScanner, BleakClient
import time
from datetime import datetime
from app import db, Attendance, Student
from rfid_scan_log import RFIDScanLog

# ESP32 BLE details
RFID_SERVICE_UUID = "12345678-1234-1234-1234-1234567890ab"
RFID_CHAR_UUID = "abcd1234-5678-90ab-cdef-1234567890ab"
ESP32_MAC = "D355B978-C1BD-9B78-CF56-07B1351FC0ED"  # Update to your device

class BLE_RFIDReader:
    def __init__(self, device_address=ESP32_MAC, max_retries=3, retry_delay=5):
        self.device_address = device_address
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.client = None
        self.is_running = True

    async def start(self):
        retries = self.max_retries
        while retries > 0 and self.is_running:
            try:
                print(f"Scanning for ESP32 ({self.device_address})...")
                device = None
                devices = await BleakScanner.discover(timeout=10.0)
                print("Discovered devices:")
                for d in devices:
                    name = d.name or "Unknown"
                    print(f"  • {name} ({d.address})")
                    if d.address.upper() == self.device_address.upper():
                        device = d
                        print("    ↳ This is our ESP32!")
                print()
                if not device:
                    raise Exception("ESP32 not found. Ensure it's powered on and in range.")
                self.client = BleakClient(device)
                await self.client.connect()
                if self.client.is_connected:
                    print("✓ Connected successfully!")
                    print("Discovering services and characteristics...")
                    for service in self.client.services:
                        print(f"Service: {service.uuid}")
                        for char in service.characteristics:
                            print(f"  Characteristic: {char.uuid} (Properties: {char.properties})")
                    # Check if expected characteristic exists
                    char_found = False
                    for service in self.client.services:
                        for char in service.characteristics:
                            if char.uuid.lower() == RFID_CHAR_UUID.lower():
                                char_found = True
                    if not char_found:
                        print(f"ERROR: Characteristic UUID {RFID_CHAR_UUID} not found on ESP32. Connection will stay open for debugging.")
                        while self.is_running and self.client.is_connected:
                            await asyncio.sleep(1)
                        continue
                    print("Looking for RFID service...")
                    try:
                        await self.client.start_notify(RFID_CHAR_UUID, self.notification_handler)
                        print("✓ RFID service found and notifications enabled")
                    except Exception as e:
                        print(f"RFID service error: {str(e)}")
                        print("Connection will stay open for debugging.")
                        while self.is_running and self.client.is_connected:
                            await asyncio.sleep(1)
                        continue
                    print("Listening for RFID tags...")
                    while self.is_running and self.client.is_connected:
                        await asyncio.sleep(0.1)
            except Exception as e:
                retries -= 1
                print(f"Connection failed: {str(e)}")
                if retries > 0:
                    print(f"Retrying in {self.retry_delay} seconds... ({retries} attempts left)")
                    await asyncio.sleep(self.retry_delay)
                else:
                    print("Maximum retries reached. Exiting...")
                    self.is_running = False
                    break
            finally:
                await self.cleanup()

    def notification_handler(self, sender, data):
        from app import app, db  # Import app and db for context
        try:
            print(f"Notification received from {sender}. Raw data: {data}")
            try:
                rfid_tag = data.decode().strip()
            except Exception as decode_err:
                print(f"Decode error: {decode_err}. Data: {data}")
                rfid_tag = None
            if not rfid_tag:
                print("No valid RFID tag received.")
                return
            current_time = datetime.now()
            print(f"\n🏷️  Tag detected: {rfid_tag}")
            print(f"⏰ Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            # Save to database inside app context
            try:
                with app.app_context():
                    self._save_attendance(rfid_tag, current_time)
                    print(f"✓ RFID tag {rfid_tag} saved at {current_time}")
            except Exception as db_err:
                db.session.rollback()
                print(f"Failed to save RFID tag: {db_err}")
        except Exception as e:
            print(f"Error processing RFID data: {e}")
        finally:
            print("\nWaiting for next tag...")

    def _save_attendance(self, rfid_tag, timestamp):
        from app import db
        try:
            student = Student.query.filter_by(rfid_tag=rfid_tag).first()
            student_name = student.full_name if student else "Unknown"
            scan_log = RFIDScanLog(tag=rfid_tag, student_name=student_name, timestamp=timestamp)
            db.session.add(scan_log)
            db.session.commit()
            print(f"✓ RFID scan {rfid_tag} ({student_name}) logged at {timestamp}")
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
                teacher_id=1,
                attendance_date=timestamp.date(),
                time_marked=timestamp,
                status='present',
                method='rfid',
                confidence_score=1.0,
                notes=f"Marked via RFID tag: {rfid_tag}"
            )
            db.session.add(new_attendance)
            db.session.commit()
            print(f"✓ Attendance marked for {student.full_name}")
            from model import generate_forecast_from_db
            generate_forecast_from_db()
        except Exception as e:
            db.session.rollback()
            print(f"Failed to save attendance record: {e}")

    async def cleanup(self):
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
    reader = BLE_RFIDReader()
    try:
        asyncio.run(reader.start())
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        reader.is_running = False
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        print("System shutdown complete.")