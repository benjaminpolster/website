from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.pdf_analyzer import analyze_pdf

app = FastAPI()

# Allow requests 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for MVP, allow all
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    result = analyze_pdf(file.file)
    return {"result": result}
