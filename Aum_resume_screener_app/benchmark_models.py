import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

# Models to benchmark
MODEL_NAMES = [
    "all-MiniLM-L6-v2",
    "paraphrase-MiniLM-L6-v2",
    "multi-qa-MiniLM-L6-cos-v1",
]

# Paths to data
RESUME_CSV = "datasets/merged.csv"
JOB_DESC_CSV = "datasets/job_descriptions.csv"

# Load data
resumes = pd.read_csv(RESUME_CSV)
jobs = pd.read_csv(JOB_DESC_CSV)

# For demonstration, we'll use the 'Top Skills' column as the resume text
resume_texts = resumes["Top Skills"].astype(str).tolist()
# Use the first N job descriptions for benchmarking
job_texts = jobs["Job Description"].astype(str).tolist()[:10]

results = []

for model_name in MODEL_NAMES:
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)
    print("Encoding resumes...")
    resume_emb = model.encode(
        resume_texts, convert_to_tensor=True, show_progress_bar=True
    )
    print("Encoding job descriptions...")
    job_emb = model.encode(job_texts, convert_to_tensor=True, show_progress_bar=True)

    print(f"Calculating similarities for {model_name}...")
    # For each job description, find the most similar resume
    for i, job_vec in enumerate(job_emb):
        scores = util.cos_sim(job_vec, resume_emb)[0].cpu().numpy()
        top_idx = np.argmax(scores)
        results.append(
            {
                "model": model_name,
                "job_idx": i,
                "job_desc": job_texts[i][:100],
                "top_resume_idx": top_idx,
                "top_resume_score": scores[top_idx],
                "top_resume_text": resume_texts[top_idx][:100],
            }
        )

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv("benchmark_results.csv", index=False)
print("Benchmarking complete. Results saved to benchmark_results.csv.")

# --- Visualization ---
# Load results (in case running separately)
results_df = pd.read_csv("benchmark_results.csv")

# Boxplot of top similarity scores for each model
plt.figure(figsize=(10, 6))
sns.boxplot(x="model", y="top_resume_score", data=results_df)
plt.title("Distribution of Top Resume Similarity Scores by Model")
plt.ylabel("Top Resume Similarity Score")
plt.xlabel("Model")
plt.tight_layout()
plt.savefig("benchmark_boxplot.png")
plt.show()

# Barplot: Average top similarity score per model
plt.figure(figsize=(8, 5))
avg_scores = results_df.groupby("model")["top_resume_score"].mean().reset_index()
sns.barplot(x="model", y="top_resume_score", data=avg_scores)
plt.title("Average Top Resume Similarity Score by Model")
plt.ylabel("Average Top Similarity Score")
plt.xlabel("Model")
plt.tight_layout()
plt.savefig("benchmark_avg_barplot.png")
plt.show()

print(
    "Visualization complete. Plots saved as benchmark_boxplot.png and benchmark_avg_barplot.png."
)
