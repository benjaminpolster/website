#Benjamin Polster
#Proof of concept - Legal Document Analysis Tool with GPT 4.1 mini
#www.benjaminpolster.com
#v.0.01

#main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pdfplumber
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key="OPENAI_API_KEY")

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
        <body>
            <h2>Upload PDF</h2>
            <form action="/analyze" enctype="multipart/form-data" method="post">
                <input type="file" name="file" accept=".pdf" required>
                <br><br>
                <button type="submit">Analyze</button>
            </form>
        </body>
    </html>
    """

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(file: UploadFile = File(...)):
    #Text extraction
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    #GPT Call 
    prompt = f"""
    You are a legal document analysis assistant.
    Analyze the following document and summarize its key points in 200 words or less.

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

    result = response.choices[0].message.content

    #GPT Result print
    return f"""
    <html>
        <body>
            <h2>Analysis Result</h2>
            <pre style="white-space: pre-wrap;">{result}</pre>
            <br>
            <a href="/">Analyze another document</a>
        </body>
    </html>
    """
