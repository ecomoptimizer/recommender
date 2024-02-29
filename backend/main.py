import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import uvicorn
from fastapi import FastAPI
import json

from backend.inputs import inputs
from src.generate import generate_emails

app = FastAPI()

@app.get("/")
def index():
    return {"message": "hello, world"}

@app.post("/generate")
def generate(inputs: inputs):
    email_inputs = inputs.email_inputs
    api_key = inputs.api_key

    if api_key == "openai":
        api_key = "google-generativeai" # Replace OpenAI key with Google GenerativeAI key
    elif api_key == "gemini-pro":
        api_key = "gemini-pro"  # Keep Gemini-Pro key as is

    answer = generate_emails(email_inputs, api_key)
    return answer

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
