from pydantic import BaseModel
from typing import List

class JobDescription(BaseModel):
    title: str
    required_skills: List[str]
    preferred_skills: List[str]
    experience_required: str
    education_required: str
    description: str