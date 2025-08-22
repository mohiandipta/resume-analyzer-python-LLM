# main.py
import shutil
from fastapi import FastAPI, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import asyncio

# Change these from relative to absolute imports
from db import Base, engine, SessionLocal
from models import Resume
from schemas import ResumeCreate, ResumeOut
from resume_parser import extract_text_from_pdf, parse_resume_with_llm

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
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text_from_pdf(temp_path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Add timeout for LLM processing
        parsed_data = await asyncio.wait_for(
            asyncio.to_thread(parse_resume_with_llm, text),
            timeout=120.0  # 2 minutes timeout
        )
        
        if not parsed_data:
            raise HTTPException(status_code=400, detail="Could not parse resume data")
        
        resume = Resume(**parsed_data)
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume
        
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Resume processing timed out")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/")
async def root():
    return {"message": "Resume Analyzer API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/debug/extract-text")
async def debug_extract_text(file: UploadFile):
    temp_path = f"./temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        text = extract_text_from_pdf(temp_path)
        return {"extracted_text": text[:1000] + "..." if len(text) > 1000 else text}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)