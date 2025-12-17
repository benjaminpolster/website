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
    prompt = f"""
Analyze the following Short Form Power of Attorney document and determine the eligibility of potential new agents.

In order to be eligible to become an agent under the bank owner's account, the following requirements must be satisfied:

1. The Power of Attorney document must be signed and notarized in the state of Illinois, with at least one (1) witness.
2. The document must be valid with respect to its effective date. The effective date must align with the date of execution, which is typically the date of signature.

Your task:
- Review the document text provided below.
- Determine whether each of the above requirements (1) and (2) is compliant or non-compliant.
- Return your findings as a clear, numbered list corresponding to each requirement.
- For each non-compliant item, provide a brief explanation indicating the reason for non-compliance and the proper requirements for the action the user is attempting to take.
- For each compliant item, provide a brief confirmation stating that the requirement was met.

Document Text:
{pdf_text}
"""

elif doc_type == "will":
    prompt = f"""
Analyze the following Will document and determine whether it is compliant.

Compliance is defined as meeting all of the following requirements:

1. The will has been filed with a court.
2. An executor has been formally appointed.

Your task:
- Review the document text provided below.
- Determine whether each of the above requirements (1) and (2) is compliant or non-compliant.
- Return your findings as a clear, numbered list corresponding to each requirement.
- For each non-compliant item, provide a brief explanation indicating the reason for non-compliance and the requirements that must be satisfied.
- For each compliant item, provide a brief confirmation stating that the requirement was met.

Document Text:
{pdf_text}
"""

else:
    prompt = f"""
Analyze the following document and provide relevant findings.

Document Text:
{pdf_text}
"""

    # Call GPT
    result = openai_call(prompt)
    return {"result": result}
