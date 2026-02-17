from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from crew import ResumeAnalyzerCrew
from pypdf import PdfReader
import uvicorn 

app = FastAPI(title="CrewAI Resume Analyzer")

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

@app.post("/analyze_resume")
async def analyze_resume(pdf_file: UploadFile = File(...)):
    try:
        # Extract PDF text
        resume_text = extract_text_from_pdf(pdf_file.file)

        # Run CrewAI analysis
        result = ResumeAnalyzerCrew().crew().kickoff(
            inputs={"resume": resume_text}
        )

        # Ensure response is JSON-serializable
        return JSONResponse(content={"analysis": str(result)})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)