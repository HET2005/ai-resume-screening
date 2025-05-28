import streamlit as st
import os

# Internal module imports
from app.resume_parser import extract_resume_text
from app.preprocess import clean_text, lemmatize_text
from app.similarity import get_similarity_score, get_model_prediction, generate_user_friendly_result
from app.utils import allowed_file

# ---------------------------- Streamlit UI Setup ----------------------------
st.set_page_config(page_title="AI Resume Matcher", layout="wide")
st.title("🔍 AI-Powered Resume Screening System")
st.markdown("### Step 1: Enter the Job Description")

# ---------------------------- Step 1: Job Description ----------------------------
job_input = st.text_area("📝 Paste the job description here:", height=200)

# ---------------------------- Step 2: Upload Resume ----------------------------
st.markdown("### Step 2: Upload the Candidate Resume")
uploaded_file = st.file_uploader("📄 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

# ---------------------------- Main Analysis Logic ----------------------------
if uploaded_file and job_input.strip():
    file_ext = uploaded_file.name.split(".")[-1]
    resume_path = f"temp_resume.{file_ext}"

    # Save uploaded file temporarily
    with open(resume_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("🔍 Analyzing resume..."):
        try:
            # Step 1: Resume extraction & cleaning
            resume_text = extract_resume_text(resume_path)
            cleaned_resume = lemmatize_text(clean_text(resume_text))

            # Step 2: Job description cleaning
            cleaned_job = lemmatize_text(clean_text(job_input))

            # Step 3: Get similarity and ML prediction
            similarity = get_similarity_score(cleaned_resume, cleaned_job)
            prediction, prob = get_model_prediction(cleaned_resume, cleaned_job)

            # Step 4: Generate result labels
            label, explanation = generate_user_friendly_result(similarity, prediction, prob)

            # Display results
            st.success("✅ Analysis complete!")
            st.markdown(f"**🔗 Match Result:** {label}")
            st.write(explanation)

        except Exception as e:
            st.error(f"❌ Error during analysis: {e}")

    # Cleanup temp file
    os.remove(resume_path)

# ---------------------------- Input Validation States ----------------------------
elif uploaded_file and not job_input.strip():
    st.warning("⚠️ Please enter a job description before uploading a resume.")

elif job_input.strip() and not uploaded_file:
    st.info("📎 Please upload a resume file to begin analysis.")

else:
    st.info("📋 Enter a job description and upload a resume to start.")
