import pdfplumber
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_pdf(file, doc_type: str):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    if doc_type == "poa":
        prompt = f"""
You are a legal document analysis assistant.

Analyze the following Short Form Power of Attorney document and determine the eligibility of potential new agents.

Eligibility requirements:
1. The document must be signed and notarized in Illinois with at least one (1) witness.
2. The document must be valid with respect to its effective date, typically the date of signature.

Instructions:
- Evaluate each requirement.
- Return COMPLIANT or NON-COMPLIANT. 
- Explain compliance or non-compliance of items 1 and 2 in a list.

Document Text:
{text[:12000]}
"""

    elif doc_type == "will":
        prompt = f"""
You are a legal document analysis assistant.

Analyze the following Will and determine compliance.

Compliance requires:
1. The will has been filed with a court.
2. An executor has been appointed.

Instructions:
- Evaluate each requirement.
- Return COMPLIANT or NON-COMPLIANT. 
- Explain compliance or non-compliance of items 1 and 2 in a list.

Document Text:
{text[:12000]}
"""

    else:
        prompt = f"""
Analyze the following document and provide relevant findings.

Document Text:
{text[:12000]}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You analyze legal documents."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
