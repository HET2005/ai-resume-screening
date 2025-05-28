from sentence_transformers import SentenceTransformer, util
import joblib
import os
import numpy as np

# Load sentence transformer model
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

# Load ML classifier model
model_path = os.path.join("models", "bert_similarity_model", "classifier.pkl")

try:
    clf = joblib.load(model_path)
except FileNotFoundError:
    raise FileNotFoundError(f"Classifier model not found at: {model_path}")

def get_similarity_score(resume_text, job_desc_text):
    """
    Compute cosine similarity between resume and job description using BERT embeddings.
    """
    embeddings = model.encode([resume_text, job_desc_text], convert_to_tensor=True)
    sim_score = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    return float(sim_score[0])

def get_model_prediction(resume_text, job_desc_text):
    """
    Use trained ML model to classify whether resume matches the job description.
    """
    emb = model.encode([resume_text, job_desc_text])
    features = np.abs(emb[0] - emb[1]).reshape(1, -1)
    prediction = clf.predict(features)[0]
    prob = clf.predict_proba(features)[0][1]
    return prediction, prob

def generate_user_friendly_result(similarity_score, prediction, prob, threshold=0.75):
    """
    Returns a user-friendly label and explanation based on similarity and ML prediction.
    """
    # Label
    label = "✅ Strong Match" if prediction == 1 and similarity_score >= threshold else \
            "⚠️ Moderate Match" if prediction == 1 else \
            "❌ Not a Match"

    # Explanation
    explanation = f"""
    **🔍 BERT Similarity Score:** `{similarity_score:.2f}`  
    **🧠 ML Match Probability:** `{prob:.2f}`  

    - {"BERT indicates strong semantic alignment." if similarity_score >= threshold else
       "BERT indicates moderate or weak similarity."}
    - {"ML model predicts this resume is a match." if prediction == 1 else
       "ML model predicts this resume does not match."}
    """

    return label, explanation
