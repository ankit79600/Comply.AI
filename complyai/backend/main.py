from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os

from complyai.backend.database import engine, Base, get_db
from complyai.backend import models, schemas
from complyai.backend.test_runner import run_compliance_tests
from complyai.backend.report_generator import generate_pdf_report
from complyai.backend.conversation_bot import process_chat

from fastapi.middleware.cors import CORSMiddleware

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ComplyAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_model(file: UploadFile = File(...)):
    # Mocking file upload since we auto-generate mock Model in MVP
    return {"message": f"Successfully uploaded {file.filename}", "model_id": file.filename}

@app.post("/test", response_model=List[schemas.TestResultOut])
def run_tests(request: schemas.RunTestRequest, db: Session = Depends(get_db)):
    results = run_compliance_tests(request.model_id, request.regulations)
    
    saved_results = []
    for r in results:
        db_res = models.TestResult(
            model_id=request.model_id,
            regulation_name=r['regulation_name'],
            status=r['status'],
            details=r['details'],
            suggestion=r['suggestion']
        )
        db.add(db_res)
        db.commit()
        db.refresh(db_res)
        saved_results.append(db_res)
        
    return saved_results

@app.get("/results/{model_id}", response_model=List[schemas.TestResultOut])
def get_results(model_id: str, db: Session = Depends(get_db)):
    return db.query(models.TestResult).filter(models.TestResult.model_id == model_id).all()

@app.get("/report/{model_id}")
def generate_report(model_id: str, db: Session = Depends(get_db)):
    results = db.query(models.TestResult).filter(models.TestResult.model_id == model_id).all()
    # Serialize for report generator
    formatted_results = [
        {"regulation_name": r.regulation_name, "status": r.status, "details": r.details, "suggestion": r.suggestion}
        for r in results
    ]
    file_path = generate_pdf_report(model_id, formatted_results)
    
    # Calculate score
    passed = sum(1 for r in formatted_results if r['status'] == 'PASS')
    total = len(formatted_results)
    score = (passed / total) * 100 if total > 0 else 0
    grade = "A" if score == 100 else "B" if score >= 80 else "C" if score >= 60 else "F"
    
    db_rep = models.Report(model_id=model_id, score=score, grade=grade, file_path=file_path)
    db.add(db_rep)
    db.commit()
    
    absolute_path = os.path.abspath(file_path)
    return {"message": "Report generated", "file_path": absolute_path, "score": score, "grade": grade}

@app.get("/download/{model_id}")
def download_report(model_id: str, db: Session = Depends(get_db)):
    db_rep = db.query(models.Report).filter(models.Report.model_id == model_id).order_by(models.Report.id.desc()).first()
    if db_rep and os.path.exists(db_rep.file_path):
        return FileResponse(path=db_rep.file_path, filename=f"Compliance_Report_{model_id}.pdf", media_type='application/pdf')
    return {"error": "Report not found"}

@app.post("/chat", response_model=schemas.ChatResponse)
def chat_endpoint(request: schemas.ChatRequest):
    return process_chat(request.message)

@app.get("/regulations")
def get_regulations():
    return {
        "regulations": [
            "Fair Lending Act",
            "Model Risk Management",
            "Anti-Money Laundering (AML)"
        ]
    }
