import pandas as pd
from app.services.parser import ResumeParser
from app.services.matcher import ResumeMatcher
from app.models.job import JobDescription

# Load data
df = pd.read_csv("resume_parser/UpdatedResumeDataSet.csv", nrows=100)

# Initialize parser and matcher
parser = ResumeParser()
matcher = ResumeMatcher()

# Example job description (customize as needed)
job = JobDescription(
    title="Data Scientist",
    required_skills=["Python", "Machine Learning", "NLP"],
    preferred_skills=["Deep Learning"],
    experience_required="2 years",
    education_required="Bachelor's",
    description="Looking for a data scientist with experience in Python and NLP."
)

# Parse resumes
resumes = []
true_categories = []
for _, row in df.iterrows():
    parsed = parser.parse_resume(str(row["Resume"]))
    parsed.category = row["Category"]
    resumes.append(parsed)
    true_categories.append(row["Category"])

# Rank resumes
rankings = matcher.rank_resumes(resumes, job)

# Example: Print top 5 ranked resumes
for i, r in enumerate(rankings[:5]):
    print(f"Rank {i+1}: Score={r['score']:.2f}, Category={r['resume'].category}")

# You can add logic to compare rankings to true categories for accuracy if you have a ground truth
