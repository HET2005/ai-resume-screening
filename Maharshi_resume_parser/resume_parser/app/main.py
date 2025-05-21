from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from .services.parser import ResumeParser
from .services.matcher import ResumeMatcher
from .models.resume import Resume
from .models.job import JobDescription
from typing import List
import pandas as pd

app = FastAPI(title="Resume Parser API")
resume_parser = ResumeParser()
resume_matcher = ResumeMatcher()

@app.post("/parse-resume/", response_model=Resume)
async def parse_resume(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode("utf-8")
        return resume_parser.parse_resume(text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/match-resumes/", response_model=List[dict])
async def match_resumes(job: JobDescription, resumes: List[Resume]):
    try:
        rankings = resume_matcher.rank_resumes(resumes, job)
        return rankings
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/screen")
async def screen_resumes(request: Request):
    try:
        data = await request.form()
        job_description = data.get("job_description", "")
        if not job_description:
            raise HTTPException(status_code=400, detail="Job description is required.")
        # Load only the first 100 resumes from CSV for speed
        df = pd.read_csv("resume_parser/UpdatedResumeDataSet.csv", nrows=100)
        resumes = []
        for _, row in df.iterrows():
            resume_text = str(row["Resume"])
            parsed = resume_parser.parse_resume(resume_text)
            parsed.category = row["Category"]
            resumes.append(parsed)
        job = JobDescription(
            title="",
            required_skills=[],
            preferred_skills=[],
            experience_required="",
            education_required="",
            description=job_description
        )
        rankings = resume_matcher.rank_resumes(resumes, job)
        ranked_resumes = [
            {"name": f"Candidate {i+1}", "score": r["score"], "category": r["resume"].category, "skills": r["resume"].skills, "raw_text": r["resume"].raw_text}
            for i, r in enumerate(rankings)
        ]
        return {"ranked_resumes": ranked_resumes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))