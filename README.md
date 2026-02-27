# 🤖 AI Financial Document Analyzer - Debug Challenge

A multi-agent financial analysis system built with **CrewAI**, **FastAPI**, and **Google Gemini**. This project was completed as part of a technical debug challenge to transform a broken, "hallucinating" codebase into a professional investment tool.

---

## 🛠️ Bugs Found and Fixed

### 1. Hallucination & Ethics Bug (Critical)
* **Problem**: The original agents were instructed to "make up facts" and recommend high-risk "meme stocks" regardless of the data.
* **Fix**: Rewrote agent backstories in `agents.py` to enforce data-driven objectivity and added a **Compliance Verifier Agent** to cross-check all AI claims against the source document.

### 2. Broken Tool Logic (Technical)
* **Problem**: The `FinancialDocumentTool` used an undefined `Pdf` class, making it impossible for the AI to read the uploaded files.
* **Fix**: Integrated `PyPDFLoader` from `langchain_community` and implemented proper `@tool` decorators in `tools.py` to allow text extraction from PDFs.

### 3. API & Connection Bugs
* **Problem**: The system lacked LLM initialization (causing crashes) and failed "CORS" checks (blocking browser requests).
* **Fix**: 
    * Initialized `ChatGoogleGenerativeAI` with secure environment variable support.
    * Added `CORSMiddleware` to `main.py` to enable seamless communication between the FastAPI backend and the Swagger UI frontend.

---

## 🚀 Setup and Usage Instructions

### 1. Prerequisites
* Python 3.10+ installed.
* A Google Gemini API Key.

### 2. Installation
Clone the repository and install the required libraries:
```bash
pip install fastapi uvicorn crewai langchain-google-genai pypdf python-dotenv langchain-community