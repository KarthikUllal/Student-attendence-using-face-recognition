import streamlit as st
from database import add_subject, get_all_courses

def create_subject():
    st.title("📚 Add New Subject")

    subject_name = st.text_input("Subject Name:")

    # Dropdown for Course (fetched from existing data)
    courses = get_all_courses()
    course = st.selectbox("Select Course:", courses if courses else ["MCA", "MBA", "BTech"])

    semester = st.text_input("Semester:")

    if st.button( "Add Subject"):
        if not all([subject_name.strip(), course.strip(), semester.strip()]):
            st.warning("⚠️ Please fill all fields.")
        else:
            add_subject(subject_name, course, semester)
            st.success(f"✅ Subject '{subject_name}' added for {course} - Semester {semester}.")

if __name__ == "__main__":
    create_subject()
