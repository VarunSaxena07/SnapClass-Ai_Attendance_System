import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")

def create_subject_dialog(teacher_id):
    st.write("Enter New  Subject Details")
    subject_code=st.text_input("Subject Code",placeholder="CS101")
    subject_name=st.text_input("Subject Name",placeholder="Introduction To Computer Science")

    subject_section=st.text_input("Section",placeholder="A")
    if st.button("Create Subject Now",type='primary',width='stretch'):
        if subject_code and subject_name and subject_section:
            try:
                create_subject(subject_code,subject_name,subject_section,teacher_id)
                st.toast("Subject Created Succesfully !")
                st.rerun()

            except Exception as e:
                st.error(f"Error : {str(e)}")
        else:
            st.warning("All Fields Are Required !!")
