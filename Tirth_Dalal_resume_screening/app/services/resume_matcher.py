# ... existing code ...

from transformers import AutoTokenizer, AutoModel
import torch
from typing import List, Dict
import numpy as np
from concurrent.futures import ThreadPoolExecutor

class ResumeMatcherService:
    def __init__(self):
        # Load model and tokenizer once during initialization
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model = AutoModel.from_pretrained('bert-base-uncased')
        self.model.eval()  # Set to evaluation mode
        self.max_length = 512
        
    def get_bert_embedding(self, text: str) -> np.ndarray:
        # Preprocess text
        inputs = self.tokenizer(text,
                               return_tensors='pt',
                               max_length=self.max_length,
                               padding='max_length',
                               truncation=True)
        
        # Get BERT embeddings
        with torch.no_grad():  # Disable gradient calculation
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :].numpy()
        
        return embeddings[0]
    
    def calculate_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        # Calculate cosine similarity
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        return float(similarity)
    
    def process_resume(self, resume: Dict, job_embedding: np.ndarray) -> Dict:
        # Combine relevant resume sections
        resume_text = f"{resume.get('summary', '')} "
        resume_text += f"{' '.join(resume.get('skills', []))} "
        resume_text += f"{' '.join(exp.get('description', '') for exp in resume.get('experience', []))}"
        
        # Get resume embedding
        resume_embedding = self.get_bert_embedding(resume_text)
        
        # Calculate similarity score
        similarity = self.calculate_similarity(resume_embedding, job_embedding)
        
        return {
            'resume': resume,
            'score': similarity * 100  # Convert to percentage
        }
    
    def match_resumes(self, job: Dict, resumes: List[Dict]) -> List[Dict]:
        # Prepare job description text
        job_text = f"{job['title']} {' '.join(job['required_skills'])} "
        job_text += f"{' '.join(job['preferred_skills'])} {job['description']}"
        
        # Get job embedding
        job_embedding = self.get_bert_embedding(job_text)
        
        # Process resumes in parallel
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(
                lambda resume: self.process_resume(resume, job_embedding),
                resumes
            ))
        
        # Sort by score in descending order
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results