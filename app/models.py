from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_filename = Column(String)
    resume_skills = Column(String)
    job_skills = Column(String)
    core_skills = Column(String)
    missing_skills = Column(String)
    match_percentage = Column(Float)
    explanation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

