import os
from dotenv import load_dotenv
from crewai.tools import tool
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

class FinancialDocumentTool:
    @tool("read_data_tool")
    def read_data_tool(path: str):
        """Reads and extracts text from a financial PDF document."""
        try:
            loader = PyPDFLoader(path)
            docs = loader.load()
            
            full_report = ""
            for data in docs:
                content = data.page_content
                # Clean up formatting
                content = " ".join(content.split())
                full_report += content + "\n"
            
            return full_report
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
