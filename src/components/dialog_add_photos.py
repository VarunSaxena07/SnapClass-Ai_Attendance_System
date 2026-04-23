import streamlit as st
from PIL import Image




@st.dialog("Capture or upload Photos")

def add_photos_dialog():
    st.write("Add Classroom Photos to take Ai Attendance")
    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab='camera'

    t1,t2=st.columns(2)


    with t1:
        type_camera="primary" if st.session_state.photo_tab=='camera' else "tertiary"
        if st.button('Camera',type=type_camera,width='stretch'):
            st.session_state.photo_tab='camera'

    
    with t2:
        type_upload="primary" if st.session_state.photo_tab=='Upload' else "tertiary"
        if st.button('Upload Photos',type=type_upload,width='stretch'):
            st.session_state.photo_tab='Upload'

    if st.session_state.photo_tab=='camera':
        cam_photo=st.camera_input('Take Snapshot',key='dialog_cam')
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast("Photo Captured !!")

            st.rerun()

    
    if st.session_state.photo_tab=='Upload':
        upload_files=st.file_uploader("Choose Image files",type=['jpg','png','jpeg'],accept_multiple_files=True,key='dialog_upload')
        
        if upload_files:
            for f in upload_files:
                st.session_state.attendance_images.append(Image.open(f))

            st.toast("Photos Uploaded Sucessfully !")
            st.rerun()
    st.divider()

    if st.button("Done",type='primary',width='stretch'):
        st.rerun()
