from app import app, db
from rfid_scan_log import RFIDScanLog

with app.app_context():
    db.create_all()
    print("All tables created successfully.")
