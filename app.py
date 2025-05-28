import streamlit as st
from register_face import register_face
from face_recognize import recognize_and_mark
from admin import create_subject

st.title("Student Attendance System Using Face Recognition")
page = st.sidebar.selectbox("Choose Action", ["Register Face","Admin(for adding subject)", "Mark Attendance"])

if page == "Register Face":
    register_face()
elif page == "Admin(for adding subject)":
    create_subject()

else:
    recognize_and_mark()