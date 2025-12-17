from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from services.pdf_analyzer import analyze_pdf

app = FastAPI()

# CORS (MVP)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    doc_type: str = Form(...)
):
    result = analyze_pdf(file.file, doc_type)
    return {"result": result}
