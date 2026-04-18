from pathlib import Path

import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout,style_background_home
def home_screen():
    assets_root = Path(__file__).resolve().parents[2]
    teacher_image = assets_root / "teacher.png"
    student_image = assets_root / "student.png"

    header_home()
    style_background_home()
    style_base_layout()
    col1 , col2=st.columns(2,gap='large')
    with col1:
        st.header("I'm Student")
        if student_image.exists():
            st.image(str(student_image),width='content')
        if st.button("Student Portal",type='primary',icon=":material/arrow_outward:",icon_position='right'):
            
            st.session_state['login_type']='student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        if teacher_image.exists():
            st.image(str(teacher_image),width='content')
        if st.button("Teacher Portal",type='primary',icon=":material/arrow_outward:",icon_position='right'):
            st.session_state['login_type']='teacher'
            st.rerun()

    footer_home()