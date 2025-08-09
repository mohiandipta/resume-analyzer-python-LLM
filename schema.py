from pydantic import BaseModel
from typing import List, Optional

class Experience(BaseModel):
    company: str
    title: str
    start: str
    end: str
    bullets: List[str]

class Education(BaseModel):
    degree: str
    school: str
    year: str

class ResumeCreate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    summary: Optional[str]
    skills: List[str] = []
    experience: List[Experience] = []
    education: List[Education] = []

class ResumeOut(ResumeCreate):
    id: int
    class Config:
        orm_mode = True
