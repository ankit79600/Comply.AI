from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TestResultBase(BaseModel):
    regulation_name: str
    status: str
    details: str
    suggestion: str

class TestResultOut(TestResultBase):
    id: int
    model_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReportOut(BaseModel):
    id: int
    model_id: str
    score: float
    grade: str
    file_path: str
    
    class Config:
        from_attributes = True

class RunTestRequest(BaseModel):
    model_id: str
    regulations: List[str]

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    detected_language: str
