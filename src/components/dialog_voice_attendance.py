import streamlit as st
from src.components.dialog_attendance_results import show_attendance_results
from src.database.config import supabase
from src.pipelines.voice_pipeline import process_bulk_audio,identify_speaker
import numpy as np
from datetime import datetime
import pandas as pd

@st.dialog("Voice Attendance")

def Voice_attendance_dialog(subject_id):
    st.write("Record a short audio to mark attendance using voice recognition.")
    audio_data=None
    audio_data=st.audio_input("Record classroom Audio")
    if st.button("Analyze Audio",type='primary',width='stretch'):
        with st.spinner("Processing Audio..."):
            enrolled_res=supabase.table('subjects_students').select("*,students(*)").eq("subject_id",selected_subject_id).execute()
            enrolled_students=enrolled_res.data
            if not enrolled_students:
                st.warning("No student has enrolled this course")
                return
            candidates_dict={
                s['students']['id']:s['students']['voice_embeddings'] for s in enrolled_students if s['students'].get['voice_embeddings']
            }

            if not candidates_dict:
                st.warning("No enrolled students have voice data available")
                return
            audio_bytes=audio_data.read()
            detected_scores=process_bulk_audio(audio_bytes,candidates_dict)

            results,attendance_to_log=[],[]
            current_timestamps=datetime.now().isoformat(timespec="seconds")
            for node in enrolled_students:
                student=node.get('students')
                if not student:
                    continue
                scores=detected_scores.get(student['student_id'],0.0)
                is_present=bool(scores>0)
                
                results.append({
                    "Name":student['name'],
                    "ID":student['student_id'],
                    "Source":scores if is_present else"-",
                    "Status":"✅ Present" if is_present else "❌ Absent"

                })

                attendance_to_log.append({
                    'student_id':student['student_id'],
                    'subject_id':seleted_subject_id,
                    'timestamps':current_timestamps,
                    "is_present":bool(is_present)
                })

            st.session_state.voice_attendance_results=(pd.DataFrame(results),attendance_to_log)
    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df,logs=st.session_state.voice_attendance_results
        show_attendance_results(df,logs)
