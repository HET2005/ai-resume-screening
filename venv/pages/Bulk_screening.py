import streamlit as st
import json
from collections import Counter
import spacy
from parser import extract_text_from_file
from job_matcher import compute_similarity

nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    tokens = [token.text.lower() for token in nlp(text) if not token.is_stop and not token.is_punct]
    common_skills = ['python', 'java', 'sql', 'nlp', 'flask', 'api', 'tensorflow', 'keras', 'c++', 'aws']
    return [skill for skill in tokens if skill in common_skills]

# -------------------------------
st.set_page_config(page_title="Bulk Screening", layout="wide")
st.title("📁 Bulk Resume Screening")

uploaded_files = st.file_uploader("Upload Resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
job_desc = st.text_area("📝 Paste Job Description", height=200)

if st.button("🚀 Start Screening") and job_desc.strip() and uploaded_files:
    st.info("🔄 Started resume processing...")

    resume_texts = []
    filenames = []

    for file in uploaded_files:
        try:
            st.text(f"Reading: {file.name}")
            # file is a BytesIO, pass it directly to your extract_text_from_file func
            text = extract_text_from_file(file)
            if text and text.strip():
                resume_texts.append(text)
                filenames.append(file.name)
            else:
                st.warning(f"⚠️ {file.name} has no readable text.")
        except Exception as e:
            st.warning(f"❌ {file.name} skipped — {e}")

    if not filenames:
        st.error("❌ No valid resumes found.")
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

        st.text("👉 Saving results.json...")
        with open("results.json", "w") as f:
            json.dump({
                "ranked": ranked[:20],
                "skills": skill_counts
            }, f)

        st.success(f"✅ {len(filenames)} resumes processed!")
        st.subheader("🏆 Top 20 Matches")
        for i, (name, score) in enumerate(ranked[:20], 1):
            st.write(f"**{i}. {name}** — Similarity: `{score:.4f}`")
