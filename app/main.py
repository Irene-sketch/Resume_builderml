from fastapi import FastAPI, UploadFile, File, Form, Depends
import pdfplumber
from skill_extractor import extract_skills
from matcher import match_skills
from fastapi import Body
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
from schemas import AnalysisResponse


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Resume Skill Intelligence API")

Base.metadata.create_all(bind=engine)



@app.get("/")
def root():
    return {"message": "API is running"}


@app.post("/analyze-resume/")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files allowed"}

    # Extract resume text
    resume_text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            resume_text += page.extract_text() or ""

    # NLP pipeline (already built earlier)
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    result = match_skills(resume_skills, job_skills, job_description)

    # Save to database
    analysis = models.Analysis(
    resume_filename=file.filename,
    resume_skills=", ".join(resume_skills),
    job_skills=", ".join(job_skills),

    core_skills=", ".join(result.get("core_skills", [])),
    missing_skills=", ".join(result.get("missing_skills", [])),

    match_percentage=result.get("match_percentage", 0),
    explanation=result.get("explanation", ""),
)


    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return {
        "analysis_id": analysis.id,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "result": result
    }


@app.get("/analysis", response_model=list[AnalysisResponse])
def get_all_analysis(db: Session = Depends(get_db)):
    return db.query(models.Analysis).all()


