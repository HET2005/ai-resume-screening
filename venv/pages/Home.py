import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

st.markdown("""
    <style>
    .big-title {
        font-size: 45px;
        font-weight: 800;
        color: #007FFF;
        margin-bottom: 0px;
    }
    .tagline {
        font-size: 20px;
        color: #555;
        margin-top: -10px;
    }
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">👋 Welcome to AI Resume Screener</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Upload resumes, analyze candidates, and match the best — all with the power of AI 🤖</p>', unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📂 Resume Upload")
    st.write("Upload 1 or 100 resumes in seconds. DOCX supported. Smart handling of complex formats.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🧠 AI Matching")
    st.write("Our NLP model ranks candidates based on job description similarity — no keyword spam needed.")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 Dashboard")
    st.write("Visualize skill trends, candidate scores, and export ranked lists. Instant insights, clean UI.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("## 🚀 Ready to start?")
st.page_link("pages/Upload.py", label="Go to Upload Page", icon="📤")

