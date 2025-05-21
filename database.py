import mysql.connector

#db connection function

def get_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "attendance_system"
    )

def add_student(name,usn,course,section,face_encoding_blob):
    con = get_connection()
    cur = con.cursor()
    q = "INSERT INTO students (name,usn,course,section,face_encoding) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(q,(name, usn, course, section, face_encoding_blob))
    con.commit()
    con.close()

def add_subject(subject_name,course):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO subjects (subject_name, course) VALUES (%s, %s)", (subject_name, course))
    con.commit()
    con.close()

def enroll_student_in_subject(student_id,subject_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT IGNORE INTO student_subjects (student_id,subject_id) VALUES (%s,%s)",(student_id,subject_id))
    con.commit()
    con.close()

def mark_attendance(student_id, subject_id, date, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attendance (student_id, subject_id, date, status)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE status = %s
    """, (student_id, subject_id, date, status, status))
    conn.commit()
    conn.close()

def get_all_subjects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, subject_name FROM subjects")
    subjects = cursor.fetchall()
    conn.close()
    return subjects

def get_students_in_subject(subject_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT students.id, students.name, students.usn, students.face_encoding
        FROM students
        JOIN student_subjects ON students.id = student_subjects.student_id
        WHERE student_subjects.subject_id = %s
    """
    cursor.execute(query, (subject_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def get_all_face_encodings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, usn, face_encoding FROM students")
    data = cursor.fetchall()
    conn.close()
    return data
