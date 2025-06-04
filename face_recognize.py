import streamlit as st
import numpy as np
import cv2
import face_recognition
import datetime
from util import convert_bgr_to_rgb, draw_face_box
from database import get_subjects_by_course_and_semester, get_students_in_subject, mark_attendance, get_all_courses

def recognize_and_mark():
    st.title("🎯 Real-time Face Recognition Attendance")

    course = st.selectbox("Select Course", get_all_courses())
    semester = st.selectbox("Select Semester", ["1", "2", "3", "4", "5", "6", "7", "8"])
    subjects = get_subjects_by_course_and_semester(course, semester)

    if not subjects:
        st.warning("No subjects found for this course and semester.")
        return

    subject_id, subject_name = st.selectbox("Select Subject", subjects, format_func=lambda x: x[1])
    st.write(f"### Subject: {subject_name}")

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

    stframe = st.empty()
    cam = cv2.VideoCapture(0)

    recognized = False

    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            st.error("Failed to read from webcam.")
            break

        rgb_frame = convert_bgr_to_rgb(frame)
        boxes = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, boxes)

        for box, encoding in zip(boxes, encodings):
            matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(known_encodings, encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                matched_id = student_ids[best_match_index]
                matched_name = known_names[best_match_index]

                draw_face_box(frame, box, matched_name)

                # Mark attendance
                today = datetime.date.today().strftime("%Y-%m-%d")
                mark_attendance(matched_id, subject_id, today, "Present")

                st.success(f"✅ Attendance marked for {matched_name}")

                recognized = True
                break
            else:
                draw_face_box(frame, box, "Unknown")

       # Show frame in Streamlit
        stframe.image(frame, channels="BGR")

        if recognized:
            cam.release()  # Ensure camera is released
            stframe.empty()  # Clear video display
            st.success("✅ Attendance marked. Thank you!")
            break

    # Final cleanup in case loop exits without recognition
    if cam.isOpened():
        cam.release()

if __name__ == "__main__":
    recognize_and_mark()
