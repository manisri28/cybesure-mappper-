from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
from datetime import datetime

# Local imports (ensure these files exist in your /parsers/ folder)
# Change these lines in backend/main.py:
# Updated imports in backend/main.py
# Inside backend/main.py
from parsers.pdf_parser import parse_pdf
from parsers.json_parser import parse_json
from parsers.sql_parser import parse_sql
from analyzer import analyze_text
app = FastAPI()

# Essential for the Frontend to communicate with the Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = {}

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    filename = file.filename.lower()
    
    try:
        # 1. Read the raw bytes first
        content = await file.read()
        
        # 2. Route to the correct parser based on extension
        if filename.endswith(".pdf"):
            text = parse_pdf(content)
        elif filename.endswith(".json"):
            text = parse_json(content)
        elif filename.endswith(".sql"):
            text = parse_sql(content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        if not text:
            raise HTTPException(status_code=422, detail="Could not extract text from file")

        # 3. Process findings
        findings = analyze_text(text)
        
        # 4. Create structured response
        doc_id = str(uuid.uuid4())[:8]
        response = {
            "document_id": doc_id,
            "findings": findings,
            "timestamp": datetime.utcnow().isoformat()
        }

        DB[doc_id] = response
        return {"analysis_id": doc_id}

    except Exception as e:
        # This catches library errors (e.g. PDF is corrupted)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/api/results/{doc_id}")
async def get_results(doc_id: str):
    if doc_id not in DB:
        raise HTTPException(status_code=404, detail="Analysis ID not found")
    return DB[doc_id]