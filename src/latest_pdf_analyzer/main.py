import os
import json
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from crew import ResumeAnalyzerCrew
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import uvicorn

app = FastAPI()

SAVE_DIR = "/Users/dikshanta/Documents/CREWAI-PDF-ANALYZER/resume_updated"
os.makedirs(SAVE_DIR, exist_ok=True)

def create_pdf(resume_text, filename):
    file_path = os.path.join(SAVE_DIR, filename)
    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    for line in resume_text.split("\n"):
        elements.append(Paragraph(line, normal_style))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    return file_path

@app.post("/upload") # analyzed file 
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    resume_text = content.decode("utf-8", errors="ignore")

    crew_instance = ResumeAnalyzerCrew()
    result = crew_instance.crew().kickoff(inputs={"resume": resume_text})

    # Use structured task outputs instead of splitting the raw string
    task_outputs = getattr(result, "tasks_output", None)
    if not task_outputs or len(task_outputs) < 3:
        return JSONResponse(
            status_code=500,
            content={"detail": "Unexpected crew output format. Expected 3 task outputs."},
        )

    structured_json = str(task_outputs[0].raw)
    hr_evaluation = str(task_outputs[1].raw)
    rewritten_resume = str(task_outputs[2].raw)

    print("\n===== HR EVALUATION =====\n")
    print(hr_evaluation)

    pdf_path = create_pdf(rewritten_resume, "optimized_resume.pdf")

    return JSONResponse({
        "hr_evaluation": hr_evaluation,
        "pdf_saved_at": pdf_path
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
