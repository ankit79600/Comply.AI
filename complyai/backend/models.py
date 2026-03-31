from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from complyai.backend.database import Base

class TestResult(Base):
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(String, index=True)
    regulation_name = Column(String)
    status = Column(String) # PASS or FAIL
    details = Column(String)
    suggestion = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(String, index=True)
    score = Column(Float)
    grade = Column(String)
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
