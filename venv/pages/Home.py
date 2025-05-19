import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    .big-title {
        font-size: 48px;
        font-weight: 700;
        color: #007FFF;
        margin-bottom: 0;
        font-family: 'Inter', sans-serif;
    }
    .tagline {
        font-size: 22px;
        color: #444;
        margin-top: 4px;
        margin-bottom: 30px;
        font-family: 'Inter', sans-serif;
    }
    .card {
        background-color: #f5f7ff;
        padding: 25px 20px;
        border-radius: 20px;
        box-shadow: 0 6px 20px rgba(0, 127, 255, 0.15);
        margin-bottom: 25px;
        font-family: 'Inter', sans-serif;
        transition: transform 0.2s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0, 127, 255, 0.25);
    }
    h3 {
        color: #004a99;
        font-weight: 700;
        margin-bottom: 10px;
    }
    p {
        font-size: 16px;
        line-height: 1.5;
        color: #333;
    }
    hr {
        border: 1px solid #eee;
        margin: 40px 0;
    }
    .start-section {
        margin-top: 40px;
        text-align: center;
        font-family: 'Inter', sans-serif;
    }
    .start-button {
        background-color: #007FFF;
        color: white;
        padding: 14px 28px;
        font-size: 18px;
        border-radius: 30px;
        border: none;
        cursor: pointer;
        text-decoration: none;
        font-weight: 700;
        display: inline-block;
        transition: background-color 0.3s ease;
    }
    .start-button:hover {
        background-color: #005bb5;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">👋 Welcome to AI Resume Screener</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Upload resumes, analyze candidates, and match the best — all with the power of AI 🤖</p>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📂 Resume Upload")
    st.markdown("<p>Upload 1 or 100 resumes in seconds. DOCX supported. Smart handling of complex formats.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🧠 AI Matching")
    st.markdown("<p>Our NLP model ranks candidates based on job description similarity — no keyword spam needed.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 Dashboard")
    st.markdown("<p>Visualize skill trends, candidate scores, and export ranked lists. Instant insights, clean UI.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("""
<div class="start-section">
    <h2>🚀 Ready to start?</h2>
    <a href="/Upload" class="start-button" target="_self">Go to Upload Page 📤</a>
</div>
""", unsafe_allow_html=True)
