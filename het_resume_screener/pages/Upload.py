import streamlit as st
import os
from parser import extract_text_from_file
from job_matcher import compute_similarity

st.set_page_config(page_title="Upload & Match Resumes", layout="wide")

st.markdown("""
    <style>
    .page-title {
        font-size: 38px;
        font-weight: 800;
        color: #007FFF;
        margin-bottom: 20px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .section-header {
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
        color: #004f99;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .info-text {
        font-size: 16px;
        color: #444;
        margin-bottom: 15px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .result-card {
        background-color: #f0f8ff;
        border-radius: 16px;
        padding: 15px 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0, 127, 255, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">📤 Upload & Match Resumes</h1>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF or DOCX, multiple files allowed):", 
    type=["pdf", "docx"], 
    accept_multiple_files=True
)

job_desc = st.text_area(
    "Paste the Job Description below:",
    height=180
)

if st.button("🔍 Match Resumes"):
    if not uploaded_files:
        st.error("❌ Please upload at least one resume file.")
    elif not job_desc.strip():
        st.error("❌ Please enter the job description to match against.")
    else:
        with st.spinner("Processing resumes..."):
            os.makedirs("temp", exist_ok=True)

            resume_texts = []
            filenames = []
            errors = []

            for file in uploaded_files:
                try:
                    file_path = os.path.join("temp", file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.read())
                    text = extract_text_from_file(file_path)
                    if text and text.strip():
                        resume_texts.append(text)
                        filenames.append(file.name)
                    else:
                        errors.append(f"⚠️ {file.name} has no readable text.")
                except Exception as e:
                    errors.append(f"❌ Failed to process {file.name}: {e}")

            if errors:
                for err in errors:
                    st.warning(err)

            if not resume_texts:
                st.error("❌ No valid resumes to process.")
            else:
                try:
                    scores = compute_similarity(resume_texts, job_desc)
                    ranked = sorted(zip(filenames, scores), key=lambda x: x[1], reverse=True)

                    st.markdown('<h2 class="section-header">📊 Ranked Resumes</h2>', unsafe_allow_html=True)

                    for name, score in ranked:
                        st.markdown(f'''
                        <div class="result-card">
                            <b>{name}</b> — Similarity Score: <code>{score:.4f}</code>
                        </div>
                        ''', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Error during matching: {e}")

# Optional: Add a back button to go to home
st.markdown("---")
if st.button("🏠 Back to Home"):
    st.experimental_set_query_params(page="home")
    st.experimental_rerun()
