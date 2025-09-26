#!/usr/bin/env python3
"""
Update all student names to Indian names and register RFID tags
"""

from backend import app, db, Student
from datetime import datetime

def update_to_indian_names():
    """Update all student names to Indian names and assign RFID tags"""
    
    # Indian names and corresponding data
    indian_students = [
        {
            'id': 1,
            'full_name': 'Arjun Sharma',
            'first_name': 'Arjun',
            'last_name': 'Sharma',
            'roll_number': '2024001',
            'email': 'arjun.sharma@student.edu.in',
            'rfid_tag': 'E4F8E400',  # Your first RFID card
            'phone': '+91 9876543210',
            'address': 'Mumbai, Maharashtra'
        },
        {
            'id': 2,
            'full_name': 'Priya Patel',
            'first_name': 'Priya',
            'last_name': 'Patel',
            'roll_number': '2024002',
            'email': 'priya.patel@student.edu.in',
            'rfid_tag': '2E401405',  # Your second RFID card
            'phone': '+91 9876543211',
            'address': 'Ahmedabad, Gujarat'
        },
        {
            'id': 3,
            'full_name': 'Rajesh Kumar',
            'first_name': 'Rajesh',
            'last_name': 'Kumar',
            'roll_number': '2024003',
            'email': 'rajesh.kumar@student.edu.in',
            'rfid_tag': 'RFID003C',
            'phone': '+91 9876543212',
            'address': 'Delhi, Delhi'
        },
        {
            'id': 4,
            'full_name': 'Sneha Gupta',
            'first_name': 'Sneha',
            'last_name': 'Gupta',
            'roll_number': '2024004',
            'email': 'sneha.gupta@student.edu.in',
            'rfid_tag': 'RFID004D',
            'phone': '+91 9876543213',
            'address': 'Pune, Maharashtra'
        },
        {
            'id': 5,
            'full_name': 'Vikram Singh',
            'first_name': 'Vikram',
            'last_name': 'Singh',
            'roll_number': '2024005',
            'email': 'vikram.singh@student.edu.in',
            'rfid_tag': 'RFID005E',
            'phone': '+91 9876543214',
            'address': 'Jaipur, Rajasthan'
        },
        {
            'id': 6,
            'full_name': 'Kavya Reddy',
            'first_name': 'Kavya',
            'last_name': 'Reddy',
            'roll_number': '2024006',
            'email': 'kavya.reddy@student.edu.in',
            'rfid_tag': 'RFID006F',
            'phone': '+91 9876543215',
            'address': 'Hyderabad, Telangana'
        },
        {
            'id': 7,
            'full_name': 'Aditya Joshi',
            'first_name': 'Aditya',
            'last_name': 'Joshi',
            'roll_number': '2024007',
            'email': 'aditya.joshi@student.edu.in',
            'rfid_tag': 'RFID007G',
            'phone': '+91 9876543216',
            'address': 'Bangalore, Karnataka'
        },
        {
            'id': 8,
            'full_name': 'Meera Nair',
            'first_name': 'Meera',
            'last_name': 'Nair',
            'roll_number': '2024008',
            'email': 'meera.nair@student.edu.in',
            'rfid_tag': 'RFID008H',
            'phone': '+91 9876543217',
            'address': 'Kochi, Kerala'
        },
        {
            'id': 9,
            'full_name': 'Rohit Verma',
            'first_name': 'Rohit',
            'last_name': 'Verma',
            'roll_number': '2024009',
            'email': 'rohit.verma@student.edu.in',
            'rfid_tag': 'RFID009I',
            'phone': '+91 9876543218',
            'address': 'Lucknow, Uttar Pradesh'
        },
        {
            'id': 10,
            'full_name': 'Ananya Mishra',
            'first_name': 'Ananya',
            'last_name': 'Mishra',
            'roll_number': '2024010',
            'email': 'ananya.mishra@student.edu.in',
            'rfid_tag': 'RFID010J',
            'phone': '+91 9876543219',
            'address': 'Bhopal, Madhya Pradesh'
        }
    ]
    
    with app.app_context():
        print("🔄 Updating all students to Indian names...")
        
        for student_data in indian_students:
            # Find existing student by ID
            student = Student.query.get(student_data['id'])
            
            if student:
                # Update existing student
                student.full_name = student_data['full_name']
                student.first_name = student_data['first_name']
                student.last_name = student_data['last_name']
                student.roll_number = student_data['roll_number']
                student.email = student_data['email']
                student.rfid_tag = student_data['rfid_tag']
                student.phone = student_data['phone']
                student.address = student_data['address']
                student.updated_at = datetime.utcnow()
                
                print(f"✓ Updated: {student.full_name} (Roll: {student.roll_number}) -> RFID: {student.rfid_tag}")
            else:
                print(f"⚠️  Student with ID {student_data['id']} not found")
        
        try:
            db.session.commit()
            print(f"\n🎉 Successfully updated all students with Indian names!")
            
            # Display the updated list
            print("\n📋 Updated Student List:")
            print("=" * 80)
            students = Student.query.all()
            for student in students:
                rfid_status = "🟢 (Your RFID)" if student.rfid_tag in ['E4F8E400', '2E401405'] else "🔵"
                print(f"{rfid_status} {student.full_name:<20} | Roll: {student.roll_number} | RFID: {student.rfid_tag}")
            
            print("\n🏷️  Your Physical RFID Cards:")
            print("   • E4F8E400 -> Arjun Sharma")
            print("   • 2E401405 -> Priya Patel")
            print("\n✅ Ready for RFID scanning with Indian student names!")
            
        except Exception as e:
            print(f"❌ Error updating students: {e}")
            db.session.rollback()

if __name__ == "__main__":
    update_to_indian_names()