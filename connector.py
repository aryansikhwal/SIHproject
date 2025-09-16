import mysql.connector
from mysql.connector import Error

# --- Database Connection Configuration (from your config.py) ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # UPDATE with your MySQL password
    'database': 'attendance_system'
}

# --- Database Connection Function ---
def create_connection():
    """Create a database connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✅ Connection to MySQL database successful")
            return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL database: {e}")
    return None

# --- Main Program Logic ---

def get_all_users(connection):
    """Fetch all users from the 'users' table."""
    cursor = connection.cursor()
    query = "SELECT id, username, full_name, role FROM users;"
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        print("\n📋 All Users:")
        for row in records:
            print(f"ID: {row[0]}, Username: {row[1]}, Name: {row[2]}, Role: {row[3]}")
    except Error as e:
        print(f"❌ Error fetching users: {e}")
    finally:
        cursor.close()

def insert_new_student(connection, student_data):
    """
    Inserts a new student record into the 'students' table.
    student_data is a tuple: (student_id, full_name, class_id, roll_number, ...)
    """
    cursor = connection.cursor()
    sql_insert = """
    INSERT INTO students 
    (student_id, full_name, class_id, roll_number, phone, enrollment_date, consent_given) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(sql_insert, student_data)
        connection.commit()
        print(f"✅ Student '{student_data[1]}' inserted successfully!")
        return cursor.lastrowid
    except Error as e:
        print(f"❌ Error inserting student: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()

def record_attendance(connection, attendance_data):
    """
    Records a new attendance entry.
    attendance_data is a tuple: (student_id, class_id, teacher_id, attendance_date, method)
    """
    cursor = connection.cursor()
    sql_insert = """
    INSERT INTO attendance 
    (student_id, class_id, teacher_id, attendance_date, method)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(sql_insert, attendance_data)
        connection.commit()
        print("✅ Attendance record created successfully.")
    except Error as e:
        print(f"❌ Error recording attendance: {e}")
        connection.rollback()
    finally:
        cursor.close()

# --- Example Usage ---
if __name__ == "__main__":
    db_connection = create_connection()

    if db_connection:
        # Example 1: Fetch and display all users
        get_all_users(db_connection)

        print("\n--- Inserting a New Student ---")
        # Ensure a valid class_id exists (e.g., from a pre-existing class)
        # Assuming Class 10 A (id=1) and Class 9 A (id=3) from your SQL
        student_info = ('SIH002', 'Jane Smith', 1, '02', '9876543210', '2024-07-15', True)
        new_student_id = insert_new_student(db_connection, student_info)

        if new_student_id:
            print(f"New student ID: {new_student_id}")

            print("\n--- Recording Attendance for the New Student ---")
            # Assuming a teacher_id exists (e.g., 'admin' is id=1)
            attendance_info = (new_student_id, 1, 1, '2025-09-16', 'manual')
            record_attendance(db_connection, attendance_info)

        # Always close the connection
        db_connection.close()
        print("\n🔒 Database connection closed.")