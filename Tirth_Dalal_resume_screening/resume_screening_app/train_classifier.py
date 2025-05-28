from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np

# 1. Load your labeled training data here
# For example:
# resumes = ["resume text1", "resume text2", ...]
# job_descs = ["job desc1", "job desc2", ...]
# labels = [0, 1, ...]  # 0 = no match, 1 = match

# --- Replace below with your actual data loading ---
resumes = ["sample resume text 1", "sample resume text 2"]
job_descs = ["sample job description 1", "sample job description 2"]
labels = [1, 0]
# ----------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Create feature vectors by encoding texts and computing absolute difference
features = []
for r, j in zip(resumes, job_descs):
    emb = model.encode([r, j])
    diff = np.abs(emb[0] - emb[1])
    features.append(diff)
features = np.array(features)

# 3. Train classifier
clf = LogisticRegression()
clf.fit(features, labels)

# 4. Save the trained classifier
joblib.dump(clf, "models/bert_similarity_model/classifier.pkl")
print("Model trained and saved successfully.")
