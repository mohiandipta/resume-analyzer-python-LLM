import pdfplumber
from llama_cpp import Llama
import json

llm = Llama(model_path="./models/mistral-7b-instruct.Q4_K_M.gguf", n_ctx=4096)

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def parse_resume_with_llm(resume_text: str) -> dict:
    prompt = f"""
    Extract the following fields from the resume text into JSON:
    {{
      "name": string,
      "email": string,
      "phone": string,
      "summary": string,
      "skills": [string],
      "experience": [
        {{
          "company": string,
          "title": string,
          "start": string,
          "end": string,
          "bullets": [string]
        }}
      ],
      "education": [
        {{
          "degree": string,
          "school": string,
          "year": string
        }}
      ]
    }}
    Resume text:
    {resume_text}
    """
    output = llm(prompt, max_tokens=1024, stop=["}"])
    try:
        parsed = json.loads(output["choices"][0]["text"] + "}")
        return parsed
    except:
        return {}
