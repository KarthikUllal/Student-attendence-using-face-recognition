from database import get_all_courses,get_all_sections,get_students
import streamlit as st
import pandas as pd

def view_students():
    st.title("View Students")

    courses = get_all_courses()
    sections = get_all_sections()

    course = st.selectbox("Select Course",courses if courses else ["MCA", "MBA"])

    section = st.selectbox("Select Section",sections if sections else ["A","B"])

    view = st.button("View Student List")

    if view:
        if course and section:
            details = get_students(course, section)
            
            if details:
                df = pd.DataFrame(details,columns=["USN", "NAME", "COURSE", "SECTION"])
                df.index = df.index + 1
                df.index.name = "S.No"
                st.table(df)
            else:
                st.warning("Oops...No Records found...")



if __name__ == "__main__":
    view_students()
