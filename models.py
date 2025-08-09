from sqlalchemy import Column, Integer, String, ARRAY, JSON
from .db import Base

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    summary = Column(String)
    skills = Column(ARRAY(String))
    experience = Column(JSON)
    education = Column(JSON)
