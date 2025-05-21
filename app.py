import streamlit as st
from register_face import register_face
from face_recognize import recognize_and_mark

st.title("Student Attendance System Using Face Recognition")
page = st.sidebar.selectbox("Choose Action", ["Register Face", "Mark Attendance"])

if page == "Register Face":
    register_face()
else:
    recognize_and_mark()