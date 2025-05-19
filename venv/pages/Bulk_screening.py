import streamlit as st
import json
from collections import Counter
import spacy
from parser import extract_text_from_file
from job_matcher import compute_similarity
import tempfile
import os

nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    tokens = [token.text.lower() for token in nlp(text) if not token.is_stop and not token.is_punct]
    common_skills = ['python', 'java', 'sql', 'nlp', 'flask', 'api', 'tensorflow', 'keras', 'c++', 'aws']
    return [skill for skill in tokens if skill in common_skills]

st.title("📁 Bulk Resume Screening (Upload Resumes)")

job_desc = st.text_area("📝 Paste Job Description", height=200)

uploaded_files = st.file_uploader("Upload Resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

if st.button("🚀 Start Screening"):

    if not job_desc.strip():
        st.error("Please paste the Job Description.")
    elif not uploaded_files:
        st.error("Please upload one or more resumes.")
    else:
        st.info("🔄 Started resume processing...")

        resume_texts = []
        filenames = []
        progress = st.progress(0)

        for i, file in enumerate(uploaded_files):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp_file:
                tmp_file.write(file.read())
                tmp_path = tmp_file.name

            try:
                text = extract_text_from_file(tmp_path)
                if text and text.strip():
                    resume_texts.append(text)
                    filenames.append(file.name)
                else:
                    st.warning(f"⚠️ {file.name} has no readable text.")
            except Exception as e:
                st.warning(f"❌ {file.name} skipped — {e}")

            progress.progress((i + 1) / len(uploaded_files))

            # Delete temp file after processing
            os.unlink(tmp_path)

        if not filenames:
            st.error("❌ No valid resumes processed.")
        else:
            st.text("👉 Calculating similarity...")
            scores = compute_similarity(resume_texts, job_desc)
            st.text("✅ Similarity calculated")

            ranked = sorted(zip(filenames, scores), key=lambda x: x[1], reverse=True)

            st.text("👉 Extracting skills...")
            all_skills = []
            for text in resume_texts:
                all_skills.extend(extract_skills(text))

            skill_counts = dict(Counter(all_skills))

            st.text("👉 Showing results...")

            st.subheader("🏆 Top Matches")
            for i, (name, score) in enumerate(ranked, 1):
                st.write(f"**{i}. {name}** — Similarity: `{score:.4f}`")

            # Optionally save results.json to disk
            with open("results.json", "w") as f:
                json.dump({
                    "ranked": ranked,
                    "skills": skill_counts
                }, f)

            st.success(f"✅ {len(filenames)} resumes processed!")

