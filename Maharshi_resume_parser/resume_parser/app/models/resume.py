from pydantic import BaseModel
from typing import List, Optional

class Education(BaseModel):
    degree: str
    institution: str
    year: Optional[str]

class Experience(BaseModel):
    company: str
    position: str
    duration: Optional[str]
    description: Optional[str]

class Resume(BaseModel):
    category: str
    skills: List[str]
    education: List[Education]
    experience: List[Experience]
    raw_text: str