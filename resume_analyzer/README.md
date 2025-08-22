# Resume Analyzer with FastAPI + PostgreSQL + Local LLM

This project is a Resume Analyzer web API built with **FastAPI**, **PostgreSQL**, and a free/open **local Large Language Model (LLM)** downloaded from Hugging Face. It extracts text from uploaded PDF resumes, parses the content using an LLM, and stores structured resume data in the database.

---

## Features

- Upload PDF resumes via REST API
- Extract text content from PDFs
- Parse resume data (name, email, skills, experience, etc.) using a local LLM model
- Store parsed resume data in PostgreSQL using SQLAlchemy ORM
- Run the app locally with FastAPI and Uvicorn

---

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn (ASGI server)
- PostgreSQL
- SQLAlchemy (ORM)
- Huggingface Hub (for downloading models)
- Local LLM model (e.g. Mistral 7B Instruct, or similar)
- PDF text extraction (using `pdfplumber` or similar)

---

## Getting Started

### Prerequisites

- Python 3.10 or later
- PostgreSQL installed and running locally
- Git

---

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/mohiandipta/resume-analyzer.git
cd resume-analyzer
