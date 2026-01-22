from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnalysisResponse(BaseModel):
    id: int
    resume_filename: str

    resume_skills: Optional[str] = ""
    job_skills: Optional[str] = ""
    core_skills: Optional[str] = ""
    missing_skills: Optional[str] = ""
    match_percentage: float = 0
    explanation: str = ""

    created_at: datetime

    class Config:
        from_attributes = True