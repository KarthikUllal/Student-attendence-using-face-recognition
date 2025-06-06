import streamlit as st
from database import (
    get_all_students, 
    get_student_by_usn,
    get_subjects_by_course_and_semester,
    enroll_student_in_subject
)

def enroll_student():
    st.title("Enroll Student in Subject")

    students = get_all_students()
    usn_list = [s[2] for s in students]  # s[2] is USN
    selected_usn = st.selectbox("Select Student USN", usn_list)

    if selected_usn:
        student = get_student_by_usn(selected_usn)
        if student:
            student_id = student["id"]
            name = student["name"]
            course = student["course"]
            semester = student["semester"]

            st.info(f"Name: {name}\n\nCourse: {course}\n\nSemester: {semester}")

            subjects = get_subjects_by_course_and_semester(course, semester)
            if subjects:
                subject_options = {name: sid for sid, name in subjects}
                subject_names = list(subject_options.keys())
                selected_subject_name = st.selectbox("Select Subject", subject_names)

                selected_subject_id = subject_options.get(selected_subject_name)
                if st.button("Enroll"):
                    enroll_student_in_subject(student_id, selected_subject_id)
                    st.success(f"{name} enrolled in '{selected_subject_name}'")
            else:
                st.warning("No subjects available for this course and semester.")
        else:
            st.error("Student not found.")
