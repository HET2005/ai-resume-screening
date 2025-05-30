import streamlit as st

st.set_page_config(page_title="AI Resume Screener Home", layout="wide")

# --- Styles ---
st.markdown("""
    <style>
    .big-title {
        font-size: 48px;
        font-weight: 900;
        color: #007FFF;
        margin-bottom: 5px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .tagline {
        font-size: 22px;
        color: #444;
        margin-top: -5px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .card {
        background-color: #f0f8ff;
        padding: 25px 20px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0, 127, 255, 0.2);
        margin-bottom: 25px;
        transition: transform 0.2s ease-in-out;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 127, 255, 0.35);
    }
    .card-title {
        font-weight: 700;
        font-size: 26px;
        margin-bottom: 10px;
        color: #004f99;
    }
    .card-desc {
        font-size: 16px;
        color: #333;
        line-height: 1.4;
    }
    .cta-button {
        background-color: #007FFF;
        color: white;
        padding: 12px 25px;
        font-size: 20px;
        font-weight: 700;
        border-radius: 12px;
        text-align: center;
        cursor: pointer;
        border: none;
        transition: background-color 0.3s ease;
        margin-top: 20px;
        display: inline-block;
        text-decoration: none;
    }
    .cta-button:hover {
        background-color: #005bb5;
        text-decoration: none;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<p class="big-title">👋 Welcome to AI Resume Screener</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Upload resumes, analyze candidates, and match the best — all with the power of AI 🤖</p>', unsafe_allow_html=True)

st.markdown("---")

# --- Feature Cards ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">📂 Resume Upload</p>', unsafe_allow_html=True)
    st.markdown('<p class="card-desc">Upload 1 or 100 resumes in seconds. Supports DOCX and PDF. Handles complex layouts smartly.</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">🧠 AI Matching</p>', unsafe_allow_html=True)
    st.markdown('<p class="card-desc">NLP-powered ranking based on deep semantic similarity — no keyword spam needed.</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">📊 Insights Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="card-desc">Visualize skill trends and candidate scores. Export ranked lists easily. Instant, clean insights.</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# --- Call to Action ---
st.markdown('<h2 style="color:#007FFF;">🚀 Ready to start?</h2>', unsafe_allow_html=True)

if st.button("📤 Go to Upload & Match Resumes"):
    st.switch_page("pages/Upload.py")


