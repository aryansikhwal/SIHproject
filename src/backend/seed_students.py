from app import app, db, Student

rfid_tags = [
    "2E401405",  # Add more tags here as needed
]

with app.app_context():
    for idx, tag in enumerate(rfid_tags, start=1):
        student = Student(
            rfid_tag=tag,
            full_name=f"Student {idx}",
            class_id=1,
            roll_number=idx
        )
        db.session.add(student)
    db.session.commit()
    print(f"Added {len(rfid_tags)} students with RFID tags.")
