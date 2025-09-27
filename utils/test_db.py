import sqlite3

db = sqlite3.connect('../instance/attendance_system.db')
cursor = db.cursor()

# Check RFID attendance records
cursor.execute("SELECT COUNT(*) FROM attendance WHERE method = 'rfid'")
count = cursor.fetchone()[0]
print(f'RFID attendance records: {count}')

if count > 0:
    cursor.execute("""SELECT a.student_id, s.full_name, s.rfid_tag, a.attendance_date, a.time_marked 
                     FROM attendance a JOIN students s ON a.student_id = s.id 
                     WHERE a.method = 'rfid' 
                     ORDER BY a.time_marked DESC LIMIT 3""")
    records = cursor.fetchall()
    print('Recent RFID scans:')
    for r in records:
        print(f'  Student: {r[1]}, RFID: {r[2]}, Date: {r[3]}, Time: {r[4]}')

db.close()