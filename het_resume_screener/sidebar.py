# sidebar.py
import streamlit as st

def show_sidebar():
    st.sidebar.title("📂 Navigation")
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/Upload.py", label="📤 Resume Screening")
    st.sidebar.page_link("pages/JD_Library.py", label="📚 JD Library Management")
