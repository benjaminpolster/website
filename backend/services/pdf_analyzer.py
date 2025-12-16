import pdfplumber
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    prompt = f"""
    You are a legal document analysis assistant.
    Identify the following document type and state it's purpose in 50 words or less.

    DOCUMENT:
    {text[:12000]}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You analyze legal documents."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
