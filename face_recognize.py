import streamlit as st
import numpy as np
import cv2
import face_recognition
from database import get_subjects_by_course_and_semester, get_students_in_subject, mark_attendance,get_all_courses
from util import convert_bgr_to_rgb, draw_face_box
import datetime

def recognize_and_mark():
    st.title("Face Recognition Attendance")

    # Select course and semester first
    courses = get_all_courses()
    course = st.selectbox("Select Course", courses)

    semesters = ["1", "2", "3", "4", "5", "6", "7", "8"]
    semester = st.selectbox("Select Semester", semesters)

    subjects = get_subjects_by_course_and_semester(course, semester)
    if not subjects:
        st.warning("No subjects found for this course and semester.")
        return
    subject_id, subject_name = st.selectbox("Select Subject", subjects, format_func=lambda x: x[1])

    st.write(f"### Subject: {subject_name}")

    # Load students enrolled in this subject + year/sem (same as semester)
    students = get_students_in_subject(subject_id, int(semester), int(semester))
    if not students:
        st.warning("No students enrolled in this subject and semester.")
        return

    known_encodings = []
    known_names = []
    student_ids = []

    for student_id, name, usn, face_encoding in students:
        encoding = np.frombuffer(face_encoding, dtype=np.float64)
        known_encodings.append(encoding)
        known_names.append(f"{name} ({usn})")
        student_ids.append(student_id)

    st.write("Look at the camera to mark your attendance:")

    img_file_buffer = st.camera_input("Capture")

    if img_file_buffer is not None:
        # Convert to OpenCV image
        file_bytes = np.asarray(bytearray(img_file_buffer.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        rgb_frame = convert_bgr_to_rgb(frame)

        boxes = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, boxes)

        for box, encoding in zip(boxes, encodings):
            draw_face_box(frame, box)

            matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(known_encodings, encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                matched_id = student_ids[best_match_index]
                matched_name = known_names[best_match_index]

                # Mark attendance with today's date
                today = datetime.date.today().strftime("%Y-%m-%d")
                mark_attendance(matched_id, subject_id, today, "Present")
                st.success(f"✅ Attendance marked for {matched_name}")
            else:
                st.warning("Face not recognized.")

        st.image(frame, channels="BGR")

if __name__ == "__main__":
    from database import get_all_courses  # ensure imported
    recognize_and_mark()
