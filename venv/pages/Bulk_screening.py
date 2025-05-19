import streamlit as st
import os
import json
from collections import Counter
import spacy
from parser import extract_text_from_file
from job_matcher import compute_similarity

# Load spacy model
nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    tokens = [token.text.lower() for token in nlp(text) if not token.is_stop and not token.is_punct]
    common_skills = ['python', 'java', 'sql', 'nlp', 'flask', 'api', 'tensorflow', 'keras', 'c++', 'aws']
    return [skill for skill in tokens if skill in common_skills]

def load_resumes(folder_path, limit=100):
    if not os.path.exists(folder_path):
        st.error(f"Folder not found: {folder_path}")
        return [], []

    resume_texts = []
    filenames = []

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".docx")]
    total = min(len(files), limit)
    progress = st.progress(0)

    for i, file in enumerate(files[:limit]):
        path = os.path.join(folder_path, file)
        try:
            st.text(f"Reading: {file}")
            text = extract_text_from_file(path)
            if text and text.strip():
                resume_texts.append(text)
                filenames.append(file)
            else:
                st.warning(f"⚠️ {file} has no readable text.")
        except Exception as e:
            st.warning(f"❌ {file} skipped — {e}")

        progress.progress((i + 1) / total)

    st.write(f"✅ Loaded {len(filenames)} resumes")
    return filenames, resume_texts

# ------------------------------

st.set_page_config(page_title="Bulk Screening", layout="wide")
st.title("📁 Bulk Resume Screening")

job_desc = st.text_area("📝 Paste Job Description", height=200)

# <-- SET YOUR ACTUAL RESUME FOLDER PATH HERE -->
RESUME_FOLDER = r"data\Resumes"

if st.button("🚀 Start Screening") and job_desc.strip():
    st.info("🔄 Started resume processing...")

    try:
        filenames, resume_texts = load_resumes(RESUME_FOLDER, limit=100)

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

    except Exception as e:
        st.error(f"💥 Fatal error: {e}")
