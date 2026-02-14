import pdfplumber

def parse_pdf(file):
    text = ""
    # Use .file to access the actual stream from FastAPI's UploadFile
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text