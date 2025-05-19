import streamlit as st
import os
from parser import extract_text_from_file
from job_matcher import compute_similarity
import spacy
import spacy.cli

st.set_page_config(page_title="AI Resume Screening", page_icon="📄", layout="wide")
st.title("Welcome to the AI Resume Screening System")
st.markdown("Use the sidebar to navigate between pages.")

# Ensure the model is downloaded on app start
spacy.cli.download("en_core_web_sm")

# Now load the model
nlp = spacy.load("en_core_web_sm")

st.title("🔍 AI Resume Screening System")

uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
job_desc = st.text_area("Paste the Job Description")

if st.button("Match Resumes") and uploaded_files and job_desc:
    if not os.path.exists("temp"):
        os.mkdir("temp")

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

# You may want to remove or relocate this part if not needed here
from docx import Document
doc = Document("data/resumes/AjayKumar.docx")
