from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_pdf_report(model_id: str, results: list) -> str:
    # ensure pdfs directory exists
    os.makedirs('reports', exist_ok=True)
    file_path = f"reports/report_{model_id}.pdf"
    
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "ComplyAI - AI Governance Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Model ID: {model_id}")
    c.drawString(50, height - 90, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Summary
    passed = sum([1 for r in results if r['status'] == 'PASS'])
    total = len(results)
    score = (passed / total) * 100 if total > 0 else 0
    grade = "A" if score == 100 else "B" if score >= 80 else "C" if score >= 60 else "F"
    
    c.drawString(50, height - 130, f"Compliance Score: {score:.1f}%")
    c.drawString(50, height - 150, f"Grade: {grade}")
    
    # Table logic
    y_pos = height - 200
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_pos, "Test Results:")
    y_pos -= 20
    
    for r in results:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y_pos, f"[{r['status']}] {r['regulation_name']}")
        y_pos -= 15
        
        c.setFont("Helvetica", 10)
        c.drawString(70, y_pos, f"Details: {r['details']}")
        y_pos -= 15
        
        if r['status'] == "FAIL":
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(70, y_pos, f"Fix Suggestion: {r['suggestion']}")
            y_pos -= 15
            
        y_pos -= 10
        if y_pos < 50:
            c.showPage()
            y_pos = height - 50
            
    c.drawString(50, y_pos - 40, "Letter to Regulators:")
    c.setFont("Helvetica", 10)
    c.drawString(50, y_pos - 60, "To Whom It May Concern,")
    c.drawString(50, y_pos - 75, f"This document validates the testing of model '{model_id}' under standard protocols.")
    
    # Footer
    c.setFont("Helvetica", 8)
    c.drawString(50, 30, "Generated automatically by ComplyAI Sandbox")
    c.save()
    
    return file_path
