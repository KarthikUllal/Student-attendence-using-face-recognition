import streamlit as st
import cv2
import face_recognition
import numpy as np
from database import add_student
from database import get_all_courses, get_all_sections
from util import draw_face_box

def register_face():
    st.title("Register New Student")

    
    courses = get_all_courses()
    sections = get_all_sections()

    with st.form("registration_form"):
        name = st.text_input("Enter Student Name:")
        usn = st.text_input("Enter USN:")
        course = st.selectbox("Select Course", courses if courses else ["MCA", "MBA", "BTech"])
        section = st.selectbox("Select Section", sections if sections else ["A", "B"])
        year = st.text_input("Enter Year:")
        sem = st.text_input("Enter Semester:")
        submitted = st.form_submit_button("Start Face Registration")

    if submitted:
        # Check all fields
        if not all([name.strip(), usn.strip(), course.strip(), section.strip(), year.strip(), sem.strip()]):
            st.warning("Please fill all fields.")
            return

        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            st.error("Error: Could not access webcam.")
            return

        st.info("Capturing face... Please stay still.")
        encodings = []
        frame_placeholder = st.empty()

        while len(encodings) < 5:
            ret, frame = cam.read()
            if not ret:
                st.error("Failed to read from webcam.")
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb)

            for box in boxes:
                draw_face_box(frame, box)

            frame_placeholder.image(frame, channels="BGR", caption=f"Encodings Captured: {len(encodings)}/5")

            if boxes:
                encoding = face_recognition.face_encodings(rgb, boxes)[0]
                encodings.append(encoding)

        cam.release()
        cv2.destroyAllWindows()

        if encodings:
            avg_encoding = np.mean(encodings, axis=0)
            encoding_blob = avg_encoding.tobytes()

            add_student(name, usn, course, section, year, sem, encoding_blob)
            st.success(f"{name} ({usn}) registered successfully!")
        else:
            st.error("No face detected. Try again.")

if __name__ == "__main__":
    register_face()
