import pdfplumber
from llama_cpp import Llama
import json
import re

llm = Llama(model_path="models/models--TheBloke--Mistral-7B-Instruct-v0.2-GGUF/snapshots/3a6fbf4a41a1d52e415a4958cde6856d34b2db93/mistral-7b-instruct-v0.2.Q2_K.gguf", n_ctx=4096)

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def parse_resume_with_llm(resume_text: str) -> dict:
    # Limit the resume text to avoid token overflow
    resume_text = resume_text[:3000]  # Limit to first 3000 characters
    
    prompt = f"""
    Extract the following information from the resume text below. Return ONLY valid JSON without any additional text:
    
    {{
      "name": "full name",
      "email": "email address",
      "phone": "phone number",
      "summary": "professional summary",
      "skills": ["skill1", "skill2", "skill3"],
      "experience": [
        {{
          "company": "company name",
          "title": "job title",
          "start": "start date",
          "end": "end date",
          "bullets": ["achievement1", "achievement2"]
        }}
      ],
      "education": [
        {{
          "degree": "degree name",
          "school": "school name",
          "year": "graduation year"
        }}
      ]
    }}
    
    Resume text: {resume_text}
    
    JSON output:
    """
    
    try:
        output = llm(
            prompt, 
            max_tokens=1024, 
            stop=["```", "###", "---"],
            temperature=0.1,
            echo=False
        )
        
        response_text = output["choices"][0]["text"].strip()
        print(f"LLM Response: {response_text}")  # Debug output
        
        # Clean the response
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        # Try to parse JSON
        parsed = json.loads(response_text)
        return parsed
        
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        print(f"Raw response: {response_text}")
        return {}
    except Exception as e:
        print(f"LLM Error: {e}")
        return {}


# def parse_resume_with_llm(resume_text: str) -> dict:
#     # Temporary: return mock data for testing
#     return {
#         "name": "John Doe",
#         "email": "john.doe@email.com",
#         "phone": "+1-555-0123",
#         "summary": "Experienced software developer",
#         "skills": ["Python", "FastAPI", "PostgreSQL"],
#         "experience": [{
#             "company": "Tech Corp",
#             "title": "Senior Developer",
#             "start": "2020-01",
#             "end": "2023-12",
#             "bullets": ["Developed APIs", "Led team"]
#         }],
#         "education": [{
#             "degree": "BSc Computer Science",
#             "school": "University",
#             "year": "2019"
#         }]
#     }