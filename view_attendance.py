import streamlit as st
from database import get_attendance, get_all_sections, get_all_subjects
import datetime
import pandas as pd
def view_attendance():
    st.title("📅 View Attendance")

    sections = get_all_sections()
    subjects = get_all_subjects()

    section = st.selectbox("Select Section", sections)
    subject_name = st.selectbox("Select Subject", subjects)
    date = st.date_input("Select Date", datetime.date.today())

    if st.button("Show Attendance"):
        if section and subject_name and date:
            records = get_attendance(section, subject_name, date.strftime("%Y-%m-%d"))
            if records:
                st.success(f"Attendance for {subject_name} on {date} (Section {section})")
                df = pd.DataFrame(records,columns=["Name", "USN", "Subject", "Date", "Status"])
                df.index = df.index + 1
                df.index.name = "S.No"
                st.table(df)
            else:
                st.warning("No attendance records found for the selected inputs.")


