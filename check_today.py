import sqlite3
from datetime import date

db = sqlite3.connect('instance/attendance_system.db')
c = db.cursor()

today = date.today().strftime('%Y-%m-%d')
print(f'Checking scans for: {today}')

c.execute('SELECT rfid_tag, scan_time, status FROM rfid_scan_logs WHERE DATE(scan_time) = ? ORDER BY scan_time DESC LIMIT 10', (today,))
scans = c.fetchall()
print(f'Today scans: {len(scans)}')
for scan in scans:
    print(f'  {scan[1]} - {scan[0]} - {scan[2]}')

db.close()