import streamlit as st
import os
import spacy
from parser import extract_text_from_file
from job_matcher import compute_similarity
from jd_manager import load_jds, add_jd, delete_jd, update_jd
import pandas as pd
from spacy.matcher import PhraseMatcher

# --- NLP Setup with synonym support ---
nlp = spacy.load("en_core_web_sm")

# Skill synonyms dictionary for normalization
skill_synonyms = {
    "python": ["python"],
    "java": ["java"],
    "sql": ["sql"],
    "nlp": ["natural language processing", "nlp"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "flask": ["flask"],
    "api": ["api"],
    "tensorflow": ["tensorflow"],
    "keras": ["keras"],
    "c++": ["c++"],
    "aws": ["aws"]
}

# Flatten synonym list for matcher
skill_list = []
for syns in skill_synonyms.values():
    skill_list.extend(syns)

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in skill_list]
matcher.add("SKILLS", patterns)

def normalize_skill(text):
    """Map extracted skill to base skill key using synonyms."""
    for base_skill, syns in skill_synonyms.items():
        if text.lower() in syns:
            return base_skill
    return text.lower()

def extract_skills(text):
    doc = nlp(text)
    matches = matcher(doc)
    skills_found = set()
    for _, start, end in matches:
        span = doc[start:end]
        normalized = normalize_skill(span.text)
        skills_found.add(normalized)
    return list(skills_found)

# --- Streamlit Page Setup ---
st.set_page_config(page_title="AI Resume Screening", page_icon="📄", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Go to", ["Resume Screening", "JD Library Management"])

if page == "Resume Screening":
    st.title("🔍 AI Resume Screening System")

    uploaded_files = st.file_uploader(
        "Upload Resumes", 
        type=["pdf", "docx"], 
        accept_multiple_files=True, 
        key="resume_upload"
    )

    jds = load_jds()
    jd_titles = [jd["title"] for jd in jds]

    st.subheader("📄 Job Description")

    selected_jd_text = ""
    if jd_titles:
        selected_title = st.selectbox("Or select from saved JD Library", jd_titles)
        selected_jd = next(jd for jd in jds if jd["title"] == selected_title)
        selected_jd_text = selected_jd["description"]
    else:
        st.info("No saved JDs available. Please add some in the JD Library Management section.")

    job_desc = st.text_area("Paste or edit the Job Description", value=selected_jd_text, height=200)

    if st.button("Match Resumes"):

        if not uploaded_files:
            st.error("❌ Please upload one or more resumes.")
        elif not job_desc.strip():
            st.error("❌ Please paste or select a Job Description.")
        else:
            st.info("🔄 Processing resumes...")
            os.makedirs("temp_resumes", exist_ok=True)

            resume_texts = []
            filenames = []
            all_skills = []

            progress_bar = st.progress(0)
            total_files = len(uploaded_files)

            for idx, file in enumerate(uploaded_files):
                try:
                    file_path = os.path.join("temp_resumes", file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.read())

                    text = extract_text_from_file(file_path)
                    if text and text.strip():
                        resume_texts.append(text)
                        filenames.append(file.name)
                        all_skills.append(extract_skills(text))
                    else:
                        st.warning(f"⚠️ {file.name} has no readable text.")
                except Exception as e:
                    st.error(f"❌ Error processing {file.name}: {e}")

                progress_bar.progress((idx + 1) / total_files)

            progress_bar.empty()

            if not resume_texts:
                st.error("❌ No valid resumes processed.")
            else:
                scores = compute_similarity(resume_texts, job_desc)

                # Detailed Match Analysis: skill match %
                jd_skills = set(extract_skills(job_desc))
                def skill_match_percentage(resume_skills):
                    if not jd_skills:
                        return 0
                    return len(set(resume_skills).intersection(jd_skills)) / len(jd_skills) * 100

                skill_matches = [skill_match_percentage(skills) for skills in all_skills]

                ranked = list(zip(filenames, scores, all_skills, skill_matches))

                # Filtering & Sorting UI
                st.subheader("Filter & Sort Results")
                min_score = st.slider("Minimum similarity score", 0.0, 1.0, 0.0, 0.01)
                min_skill_match = st.slider("Minimum skill match %", 0, 100, 0, 1)
                sort_by = st.selectbox("Sort by", ["Similarity Score", "Skill Match %"], index=0)

                filtered_ranked = [
                    item for item in ranked
                    if item[1] >= min_score and item[3] >= min_skill_match
                ]

                if sort_by == "Similarity Score":
                    filtered_ranked.sort(key=lambda x: x[1], reverse=True)
                else:
                    filtered_ranked.sort(key=lambda x: x[3], reverse=True)

                st.subheader("📊 Ranked Resumes with Skills and Match Analysis:")
                for name, score, skills, skill_pct in filtered_ranked:
                    skills_str = ", ".join(sorted(set(skills))) if skills else "No skills detected"
                    st.write(f"**{name}** — Similarity: `{score:.4f}`, Skill Match: `{skill_pct:.1f}%`")
                    st.write(f"🛠 Skills: {skills_str}")
                    st.markdown("---")

                # Export results to CSV
                export_data = []
                for name, score, skills, skill_pct in filtered_ranked:
                    export_data.append({
                        "Filename": name,
                        "Similarity Score": score,
                        "Skill Match %": skill_pct,
                        "Skills": ", ".join(sorted(set(skills)))
                    })
                df_export = pd.DataFrame(export_data)

                csv = df_export.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Export Results to CSV",
                    data=csv,
                    file_name='resume_screening_results.csv',
                    mime='text/csv'
                )

                # Resume Detail Viewer
                st.subheader("🔎 View Resume Details")
                selected_resume = st.selectbox("Select a resume to view full text:", filenames)
                if selected_resume:
                    index = filenames.index(selected_resume)
                    st.text_area("Full Resume Text", resume_texts[index], height=300)


elif page == "JD Library Management":
    st.title("📚 JD Library Management")

    jds = load_jds()

    # Display existing JDs
    if jds:
        st.subheader("Existing Job Descriptions")
        for jd in jds:
            with st.expander(jd["title"], expanded=False):
                new_title = st.text_input("Edit Job Title", value=jd["title"], key=f"title_{jd['id']}")
                new_desc = st.text_area("Edit Job Description", value=jd["description"], key=f"desc_{jd['id']}")
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.button("Update JD", key=f"update_{jd['id']}"):
                        if new_title.strip() and new_desc.strip():
                            update_jd(jd["id"], new_title.strip(), new_desc.strip())
                            st.success(f"Updated '{new_title}'")
                        else:
                            st.warning("Title and Description cannot be empty.")
                with col2:
                    if st.button("Delete JD", key=f"delete_{jd['id']}"):
                        delete_jd(jd["id"])
                        st.success(f"Deleted '{jd['title']}'")
                        st.experimental_rerun()
    else:
        st.info("No Job Descriptions saved yet.")

    st.markdown("---")

    # Add new JD
    st.subheader("➕ Add New Job Description")
    new_title = st.text_input("Job Title", key="new_jd_title")
    new_desc = st.text_area("Job Description", key="new_jd_desc")
    if st.button("Add JD"):
        if new_title.strip() and new_desc.strip():
            add_jd(new_title.strip(), new_desc.strip())
            st.success(f"Added new JD '{new_title}'")
            st.experimental_rerun()
        else:
            st.warning("Please fill in both Title and Description.")
