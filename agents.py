import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from tools import FinancialDocumentTool

load_dotenv()

# We specify the model using the 'google/' prefix to ensure the correct provider is used
gemini_llm = LLM(
    model="google/gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)

# Senior Financial Analyst Agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide accurate, data-driven investment insights based on: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous financial analyst. You rely strictly on "
        "provided financial data to give objective analysis."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=gemini_llm,
    max_iter=3
)

# Compliance Verifier Agent
verifier = Agent(
    role="Compliance & Document Verifier",
    goal="Ensure the analysis matches the source document exactly and check for errors.",
    verbose=True,
    backstory=(
        "You are an expert in financial accuracy. Your job is to prevent "
        "hallucinations and ensure all data is grounded in the report."
    ),
    llm=gemini_llm,
    allow_delegation=False
)