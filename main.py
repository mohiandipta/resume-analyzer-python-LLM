import shutil
from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.orm import Session
from .db import Base, engine, SessionLocal
from .models import Resume
from .schemas import ResumeCreate, ResumeOut
from .resume_parser import extract_text_from_pdf, parse_resume_with_llm

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/analyze", response_model=ResumeOut)
async def analyze_resume(file: UploadFile, db: Session = Depends(get_db)):
    temp_path = f"./temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(temp_path)
    parsed_data = parse_resume_with_llm(text)

    resume = Resume(**parsed_data)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume
