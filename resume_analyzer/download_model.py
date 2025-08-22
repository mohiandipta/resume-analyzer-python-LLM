import os
import requests
from huggingface_hub import hf_hub_download

# Create models directory if not exists
os.makedirs("models", exist_ok=True)

repo_id = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"

# Corrected API URL to list files in repo
api_url = f"https://huggingface.co/api/models/{repo_id}/tree/main"
response = requests.get(api_url)
response.raise_for_status()
files = response.json()

# Filter model files by extension
model_files = [f['path'] for f in files if f['path'].endswith(('.gguf', '.bin', '.ggml'))]

if not model_files:
    raise Exception("No suitable model files found in the repo.")

filename = model_files[0]
print(f"Found model file: {filename}")

model_path = hf_hub_download(repo_id=repo_id, filename=filename, cache_dir="models")
print(f"Model downloaded to: {model_path}")
