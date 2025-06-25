import mysql.connector

#db connection function

def get_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "attendance_system"
    )

def add_student(name, usn, course, section, year, semester, face_encoding_blob):
    con = get_connection()
    cur = con.cursor()
    q = """
        INSERT INTO students (name, usn, course, section, year, semester, face_encoding)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(q, (name, usn, course, section, year, semester, face_encoding_blob))
    con.commit()
    con.close()

def add_subject(subject_name, course, semester):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO subjects (subject_name, course, semester) VALUES (%s, %s, %s)",
        (subject_name, course, semester)
    )
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
        SELECT status FROM attendance 
        WHERE student_id = %s AND subject_id = %s AND date = %s
    """, (student_id, subject_id, date))
    result = cursor.fetchone()

    if result:
        conn.close()
        return "already_marked"  # Attendance already present

    cursor.execute("""
        INSERT INTO attendance (student_id, subject_id, date, status)
        VALUES (%s, %s, %s, %s)
    """, (student_id, subject_id, date, status))
    conn.commit()
    conn.close()
    return "marked"


def get_subjects_by_course_and_semester(course, semester):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id, subject_name FROM subjects WHERE course = %s AND semester = %s", (course, semester))
    result = cur.fetchall()
    con.close()
    return result


def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, usn FROM students")
    students = cursor.fetchall()
    conn.close()
    return students

def get_students(course, section): # To get students for displaying their details according to course and section
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, usn, course, section from students where course = %s and section = %s",(course, section))
    students = cursor.fetchall()
    conn.close()
    return students

def get_student_by_usn(usn):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, course, semester FROM students WHERE usn = %s", (usn,))
    student = cursor.fetchone()
    conn.close()
    return student



# def get_students_in_subject(subject_id):
#     conn = get_connection()
#     cursor = conn.cursor()
#     query = """
#         SELECT students.id, students.name, students.usn, students.face_encoding
#         FROM students
#         JOIN student_subjects ON students.id = student_subjects.student_id
#         WHERE student_subjects.subject_id = %s
#     """
#     cursor.execute(query, (subject_id,))
#     result = cursor.fetchall()
#     conn.close()
#     return result

def get_students_in_subject(subject_id, year, semester):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT students.id, students.name, students.usn, students.face_encoding
        FROM students
        JOIN student_subjects ON students.id = student_subjects.student_id
        WHERE student_subjects.subject_id = %s
          AND students.year = %s
          AND students.semester = %s
    """
    cursor.execute(query, (subject_id, year, semester))
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

def get_all_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT course FROM students")
    courses = [row[0] for row in cursor.fetchall()]
    conn.close()
    defaults = {"MCA", "MBA"}
    return sorted(defaults.union(courses))

def get_all_sections():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT section FROM students")
    sections = [row[0] for row in cursor.fetchall()]
    conn.close()
    defaults = {"A", "B"}
    return sorted(defaults.union(sections))

def get_all_subjects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT subject_name FROM subjects")
    subjects = [row[0] for row in cursor.fetchall()]
    conn.close()
    return subjects

def get_attendance(section, subject_name, date=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            students.name, 
            students.usn, 
            subjects.subject_name, 
            attendance.date, 
            attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        JOIN subjects ON attendance.subject_id = subjects.id
        WHERE students.section = %s AND subjects.subject_name = %s
    """

    params = [section, subject_name]

    if date:
        query += " AND attendance.date = %s"
        params.append(date)

    query += " ORDER BY attendance.date DESC"

    cursor.execute(query, params)
    records = cursor.fetchall()
    conn.close()

    return records
