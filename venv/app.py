import streamlit as st
import os
import subprocess
import sys

MODEL_NAME = "en_core_web_sm"
MODEL_DIR = os.path.join(os.path.expanduser("~"), f".{MODEL_NAME}")

def ensure_spacy_model():
    # Check if model dir exists, if not, download
    if not os.path.exists(MODEL_DIR):
        try:
            subprocess.check_call(
                [sys.executable, "-m", "spacy", "download", MODEL_NAME, "-d", MODEL_DIR]
            )
            st.success(f"Downloaded spaCy model '{MODEL_NAME}' successfully!")
        except Exception as e:
            st.error(f"Failed to download spaCy model: {e}")
            st.stop()

ensure_spacy_model()

# Now import after model ensured
from job_matcher import compute_similarity

st.title("🔍 AI Resume Screening System")

uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
job_desc = st.text_area("Paste the Job Description")

if st.button("Match Resumes") and uploaded_files and job_desc:
    if not os.path.exists("temp"):
        os.mkdir("temp")

    from parser import extract_text_from_file

    resume_texts = []
    filenames = []

    for file in uploaded_files:
        file_path = os.path.join("temp", file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
        text = extract_text_from_file(file_path)
        resume_texts.append(text)
        filenames.append(file.name)

    scores = compute_similarity(resume_texts, job_desc)
    ranked = sorted(zip(filenames, scores), key=lambda x: x[1], reverse=True)

    st.subheader("📊 Ranked Resumes:")
    for name, score in ranked:
        st.write(f"**{name}** — Similarity: `{score:.4f}`")
