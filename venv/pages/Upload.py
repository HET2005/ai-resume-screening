import streamlit as st
import os
from parser import extract_text_from_file
from job_matcher import compute_similarity

st.title("📤 Upload & Match Resumes")

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
