from transformers import AutoTokenizer, AutoModel
import torch
from typing import List, Dict
from ..models.resume import Resume
from ..models.job import JobDescription
import numpy as np
from concurrent.futures import ThreadPoolExecutor

class ResumeMatcher:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        self.model = AutoModel.from_pretrained("distilbert-base-uncased")
        self.model.eval()
        self.max_length = 512

    def get_embedding(self, text: str) -> np.ndarray:
        print(f"Generating embedding for: {text[:30]}")
        if not text or not isinstance(text, str):
            # Return a zero vector if text is empty or invalid
            return np.zeros(self.model.config.hidden_size)
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_length,
            padding="max_length"
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
            embedding = outputs.last_hidden_state[:, 0, :].numpy()
        return embedding[0]

    def calculate_similarity(self, resume_emb: np.ndarray, job_emb: np.ndarray) -> float:
        norm_resume = np.linalg.norm(resume_emb)
        norm_job = np.linalg.norm(job_emb)
        if norm_resume == 0 or norm_job == 0:
            return 0.0
        similarity = np.dot(resume_emb, job_emb) / (norm_resume * norm_job)
        return float(similarity)

    def process_resume(self, resume: Resume, job_emb: np.ndarray) -> Dict:
        try:
            resume_text = getattr(resume, "raw_text", "")
            resume_emb = self.get_embedding(resume_text)
            score = self.calculate_similarity(resume_emb, job_emb)
            return {"resume": resume, "score": score * 100}
        except Exception as e:
            return {"resume": resume, "score": 0.0, "error": str(e)}

    def rank_resumes(self, resumes: List[Resume], job: JobDescription) -> List[Dict]:
        job_text = f"{job.description} {' '.join(job.required_skills)} {' '.join(getattr(job, 'preferred_skills', []))}"
        job_emb = self.get_embedding(job_text)
        results = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_resume, resume, job_emb) for resume in resumes]
            for future in futures:
                results.append(future.result())
        ranked = sorted(results, key=lambda x: x["score"], reverse=True)
        return ranked