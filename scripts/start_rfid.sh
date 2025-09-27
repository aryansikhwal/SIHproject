#!/bash
# AttenSync RFID Listener Startup Script

echo "Starting AttenSync RFID Listener..."
cd "$(dirname "$0")/../src/hardware"
python rfid_system.py
