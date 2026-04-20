import streamlit as st
from src.ui.base_layout import style_base_layout,style_background_dashboard
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.database.db import check_teacher_exists,create_teacher,teacher_login
def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_register()

def teacher_dashboard():
    teacher_data=st.session_state.teacher_data
    st.header(f"""Welcome , {teacher_data['name']}""")
def login_teacher(username,password):
    if not username or not password:
        return False
    teacher=teacher_login(username,password)
    if teacher:
        st.session_state.user_role="teacher"
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True
    return False



def register_teacher(teacher_username,teacher_name,teacher_password,teacher_pass_confirm):
    if not teacher_username or not teacher_password or not teacher_name:
        return False , "All Fields are required !!"
    if check_teacher_exists(teacher_username):
        return False,"Username already taken!!"

    if teacher_password != teacher_pass_confirm:
        return False,"Password must be same !!"
    try:
        create_teacher(teacher_username,teacher_password,teacher_name)
        return True,"Registered Sucessfully !! Login Now"
    except Exception as e:
        return False,"Unexpected Error !!"

def teacher_screen_login():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go Back",type='secondary',key='loginbackbtn',shortcut='control+backspace',width='stretch'):
            st.session_state["login_type"]=None
            st.rerun()
    st.header("Login Using Passwrod",text_alignment='center')
    st.space()
    st.space()
    teacher_username=st.text_input("Enter username",placeholder='Charlie')


    teacher_password=st.text_input("Enter password",type='password',placeholder="Enter Password")
    btncol1,btncol2=st.columns(2)
    st.divider()
    with btncol1:
        if st.button("Login",icon=":material/passkey:",shortcut='control+enter',width='stretch'):
            if login_teacher(teacher_username,teacher_password):
                st.toast("Welcome Back !! 👋 ")
                import time
                time.sleep(2)
                st.rerun()
            else:
                st.error("Invalid username and Password Combo !!")

    with btncol2:
        if st.button("Register Instead",type='primary',icon=":material/passkey:",width='stretch'):
            st.session_state.teacher_login_type='register'
    footer_dashboard()
    

def teacher_screen_register():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    st.header("Register Your Teacher Profile")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go Back",type='secondary',key='registerbackbtn',shortcut='control+backspace',width='stretch'):
            st.session_state['login_type']=None
            st.rerun()
        st.space()
    st.space()
    teacher_username=st.text_input("Enter username",placeholder='Charlie')
    teacher_name=st.text_input("Enter Name",placeholder='Charlie fox')


    teacher_password=st.text_input("Enter password",type='password',placeholder="Enter Password")
    teacher_pass_confirm=st.text_input("Confirm password",type='password',placeholder="Enter Password")
    btncol1,btncol2=st.columns(2)
    with btncol1:
        if st.button("Register Now",icon=":material/passkey:",shortcut='control+enter',width='stretch'):
            success,message= register_teacher(teacher_username,teacher_name,teacher_password,teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)
    with btncol2:
        if st.button("Login Instead",type='primary',icon=":material/passkey:",width='stretch'):
            st.session_state.teacher_login_type='login'
    st.divider()
    footer_dashboard()