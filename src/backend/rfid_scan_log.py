from app import db
from datetime import datetime

class RFIDScanLog(db.Model):
    __tablename__ = 'rfid_scan_log'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), nullable=False)
    student_name = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<RFIDScanLog {self.tag} {self.student_name} @ {self.timestamp}>'
