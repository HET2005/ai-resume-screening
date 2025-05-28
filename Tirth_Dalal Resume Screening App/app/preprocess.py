import re
import spacy
import subprocess
import sys

MODEL_NAME = "en_core_web_sm"

try:
    nlp = spacy.load(MODEL_NAME)
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", MODEL_NAME], check=True)
    nlp = spacy.load(MODEL_NAME)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove excess whitespace
    text = re.sub(r'[^\w\s.,]', '', text)  # Remove special chars
    return text.strip()

def lemmatize_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])
