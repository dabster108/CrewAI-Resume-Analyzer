from crew import ResumeAnalyzerCrew
from pypdf import PdfReader


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


if __name__ == "__main__":

    pdf_path = "/Users/dikshanta/Documents/CREWAI-PDF-ANALYZER/prabesh_cv.pdfc"

    resume_text = extract_text_from_pdf(pdf_path)

    result = ResumeAnalyzerCrew().crew().kickoff(
        inputs={"resume": resume_text}
    )

    print("\n RESUME ANALYSIS \n")
    print(result)
