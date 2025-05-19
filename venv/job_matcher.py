import spacy
from spacy.cli import download
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure model is downloaded and loaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    if not text:
        return ""
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

def compute_similarity(resume_texts, job_desc):
    try:
        all_texts = [clean_text(t) for t in resume_texts]
        job_text = clean_text(job_desc)

        if not job_text.strip():
            raise ValueError("❌ Job description is empty after cleaning.")

        if all(len(t.strip()) == 0 for t in all_texts):
            raise ValueError("❌ All resumes are empty after cleaning.")

        combined = all_texts + [job_text]

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(combined)

        scores = cosine_similarity(vectors[-1], vectors[:-1])
        return scores.flatten()

    except Exception as e:
        raise RuntimeError(f"💥 compute_similarity failed: {e}")
