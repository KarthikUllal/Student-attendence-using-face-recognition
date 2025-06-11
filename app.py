import streamlit as st
from register_face import register_face
from face_recognize import  recognize_and_mark
from add_subject import create_subject
from enroll_student import enroll_student
from view_attendance import view_attendance

st.set_page_config(page_title="Face Recognition Attendance System", layout="centered")
st.title("🎓 Student Attendance System Using Face Recognition")

st.sidebar.header("🔧 Navigation")
st.sidebar.markdown("Choose an action to get started:")

page = st.sidebar.radio(
    "Select Action",
    [
        "🧍 Register Face",
        "📝 Enroll Student",
        "🛠️ Add Subjects",
        "✅ Mark Attendance",
        "View Attendance"
    ]
)

if page == "🧍 Register Face":
    register_face()
elif page == "📝 Enroll Student":
    enroll_student()
elif page == "🛠️ Add Subjects":
    create_subject()
elif page == "View Attendance":
    view_attendance()
else:
    recognize_and_mark()
