#!/usr/bin/env python3
"""
Register Your RFID Cards
"""
from models import *
from backend import app

with app.app_context():
    print("🏷️ Registering Your RFID Cards...")
    print("=" * 40)
    
    # Option 1: Assign to existing students
    student1 = Student.query.filter_by(full_name='Alice Johnson').first()
    student2 = Student.query.filter_by(full_name='Bob Smith').first()
    
    if student1:
        # Update Alice with your first card
        old_tag = student1.rfid_tag
        student1.rfid_tag = 'E4F8E400'
        print(f"✅ Updated Alice Johnson: {old_tag} → E4F8E400")
    
    if student2:
        # Update Bob with your second card  
        old_tag = student2.rfid_tag
        student2.rfid_tag = '2E401405'
        print(f"✅ Updated Bob Smith: {old_tag} → 2E401405")
    
    db.session.commit()
    
    print("\n🎯 Your cards are now registered!")
    print("Next time you scan, attendance will be marked automatically!")
    
    # Show updated registrations
    print("\n📱 Your RFID Cards:")
    for tag in ['E4F8E400', '2E401405']:
        student = Student.query.filter_by(rfid_tag=tag).first()
        if student:
            print(f"   🏷️ {tag} → {student.full_name} ({student.class_info.name})")
        else:
            print(f"   ❌ {tag} → Not assigned")