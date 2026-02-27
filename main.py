from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst, verifier
from task import analyze_financial_document, verification

# 1. Initialize FastAPI
app = FastAPI(title="Financial Document Analyzer")

# 2. Fix "Failed to fetch" - Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_crew(query: str, file_path: str):
    """To run the whole crew"""
    financial_crew = Crew(
        agents=[financial_analyst, verifier],
        tasks=[analyze_financial_document, verification],
        process=Process.sequential,
    )
    
    # Passing query and file_path as inputs
    result = financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_financial_document_api(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"
            
        # Run the CrewAI process
        response = run_crew(query=query.strip(), file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        # Provide a more detailed error message
        print(f"Server Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass 

if __name__ == "__main__":
    import uvicorn
    # Use 127.0.0.1 and port 8000 for local testing
    uvicorn.run(app, host="127.0.0.1", port=8000)