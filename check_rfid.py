import sqlite3

db = sqlite3.connect('instance/attendance_system.db')
c = db.cursor()

# Check RFID tables
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%rfid%'")
print('RFID tables:', c.fetchall())

# Check if rfid_scan_log has data
try:
    c.execute('SELECT COUNT(*) FROM rfid_scan_log')
    print('RFIDScanLog records:', c.fetchone()[0])
    
    c.execute('SELECT * FROM rfid_scan_log ORDER BY scan_time DESC LIMIT 3')
    records = c.fetchall()
    print('Recent scans:', records)
except Exception as e:
    print('Error:', e)

db.close()