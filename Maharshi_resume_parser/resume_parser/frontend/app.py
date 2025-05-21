import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Resume Screener", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {background: #181c24; color: #f5f6fa;}
    .stButton>button {border-radius: 8px; font-weight: 600;}
    .stProgress>div>div {background: linear-gradient(90deg,#00c6ff,#0072ff);}
    .resume-card {background: #23272f; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 2px 8px #0002;}
    .dashboard-title {font-size: 2rem; font-weight: 700; margin-bottom: 1rem;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='dashboard-title'>AI Resume Screener 🚀</div>", unsafe_allow_html=True)
st.info("Upload resumes, analyze candidates, and match the best – all with the power of AI.")

API_BASE = "http://localhost:8000"

job_desc = st.text_area("Paste Job Description", placeholder="e.g. Web development, Python, React, ...", height=120)
uploaded_files = st.file_uploader("Upload Resumes (DOCX, PDF)", accept_multiple_files=True)

if st.button("Start Screening", type="primary"):
    if not job_desc or not uploaded_files:
        st.warning("Please provide a job description and upload at least one resume.")
    else:
        with st.spinner("Processing resumes..."):
            files = [("files", (f.name, f, f.type)) for f in uploaded_files]
            data = {"job_description": job_desc}
            try:
                response = requests.post(f"{API_BASE}/screen", data=data, files=files)
                response.raise_for_status()
                results = response.json()
                st.success("Screening complete!")
                df = pd.DataFrame(results["ranked_resumes"])
                st.metric("Top Ranked Resume", f"{df.iloc[0]['name']} - {df.iloc[0]['score']:.1f}")
                st.bar_chart(df.set_index("name")["score"])
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error during screening: {e}")