import os
import re
import torch
from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader
from docx import Document
import streamlit as st
import numpy as np


# --- Model Loading (Cached) ---
@st.cache_resource  # Caches the model across reruns and sessions for efficiency
def load_model(model_name="all-MiniLM-L6-v2"):
    """Loads the Sentence Transformer model."""
    try:
        model = SentenceTransformer(model_name)
        return model
    except Exception as e:
        st.error(f"Error loading model {model_name}: {e}")
        return None


# --- Text Extraction Functions ---
def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        st.error(f"Error reading PDF {uploaded_file.name}: {e}")
    return text


def extract_text_from_docx(uploaded_file):
    text = ""
    try:
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        st.error(f"Error reading DOCX {uploaded_file.name}: {e}")
    return text


def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name
    try:
        if file_name.lower().endswith(".pdf"):
            return extract_text_from_pdf(uploaded_file)
        elif file_name.lower().endswith(".docx"):
            return extract_text_from_docx(uploaded_file)
        elif file_name.lower().endswith(".txt"):
            return uploaded_file.read().decode("utf-8")
        else:
            st.warning(
                f"Unsupported file format: {file_name}. Only PDF, DOCX, TXT are supported."
            )
            return ""
    except Exception as e:
        st.error(f"Failed to extract text from {file_name}: {e}")
        return ""


# --- Text Preprocessing Function ---
def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()  # Lowercase
    text = re.sub(r"\s+", " ", text)  # Replace multiple whitespaces with single
    text = re.sub(
        r"[\r\n]+", " ", text
    )  # Replace newlines and carriage returns with space
    # Minimal punctuation removal, as sentence transformers can often handle it.
    # text = re.sub(r'[^\w\s]', '', text)
    return text.strip()


# --- Embedding Generation Function ---
def get_embeddings(texts, model):
    if model is None:
        st.error("Embedding model is not loaded.")
        return None
    if isinstance(texts, str):
        texts = [texts]

    # Ensure all items in texts are strings
    processed_texts = [str(t) if t is not None else "" for t in texts]

    try:
        embeddings = model.encode(processed_texts, convert_to_tensor=True)
        return embeddings
    except Exception as e:
        st.error(f"Error generating embeddings: {e}")
        return None


# --- Cosine Similarity Function ---
def calculate_cosine_similarity(embedding1, embedding2):
    if embedding1 is None or embedding2 is None:
        return np.array([[0.0]])  # Return a default low score if embeddings failed

    # Ensure embeddings are 2D for util.cos_sim
    if len(embedding1.shape) == 1:
        embedding1 = embedding1.unsqueeze(0)
    if len(embedding2.shape) == 1:
        embedding2 = embedding2.unsqueeze(0)

    try:
        cosine_scores = util.cos_sim(embedding1, embedding2)
        return cosine_scores.cpu().numpy()
    except Exception as e:
        st.error(f"Error calculating cosine similarity: {e}")
        return np.array([[0.0]])  # Return a default low score
