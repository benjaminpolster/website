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

from fastapi import Form

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), doc_type: str = Form(...)):
    pdf_text = analyze_pdf(file.file)

    if doc_type == "poa":
        prompt = f"Analyze this Short Form Power of Attorney and determine eligibility of potential new agents. In order to be eligible to become an agent under the bank owner's 
        account, the Power of Attorney document must be signed and notarized in Illinois with at least one witness (1). In order for the document to be valid, it must be in alignment 
        with the effective date listed on the document (2). The effective date is typically the date of signature. List the findings (compliance or non-compliance) of items (1) and (2) in a list. 
        For each item that is non-compliant, provide a brief message indicating the reason for non-compliance and the proper requirements of the action the user is attempting to take with respect to that item.
        For each item that is compliant, provide a brief message confirming that requirements were met.\n{pdf_text}"
    elif doc_type == "will":
        prompt = f"Analyze this Will and determine compliance. Compliance is met when the will is filed with a court (1) and executor appointed (2). If one or both of these is not satisfied, the will is not in compliance.
        List the findings of items (1) and (2) For each item that is non-compliant, provide a brief message indicating the reason for non-compliance and the requirements of that item. 
        For each item that is compliant, provide a brief message confirming that requirements were met.\n{pdf_text}"
    else:
        prompt = f"Analyze this document:\n{pdf_text}"

    # Call GPT
    result = openai_call(prompt)
    return {"result": result}
