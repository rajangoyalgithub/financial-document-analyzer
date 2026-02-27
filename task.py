from crewai import Task
from agents import financial_analyst, verifier

analyze_financial_document = Task(
    description=(
        "Analyze the financial document provided at {file_path}. "
        "Focus on answering the user's specific query: {query}. "
        "Extract key financial metrics, revenue trends, and operational highlights."
    ),
    expected_output=(
        "A detailed financial summary including: "
        "1. Direct answer to the user query. "
        "2. Key metrics (Revenue, Profit, etc.). "
        "3. Notable trends found in the document."
    ),
    agent=financial_analyst
)

verification = Task(
    description=(
        "Review the analysis produced by the Financial Analyst. "
        "Cross-reference all numbers and claims with the original document. "
        "Ensure no investment advice is given without a disclaimer."
    ),
    expected_output=(
        "A verification report confirming the accuracy of the data. "
        "If hallucinations are found, list them for correction."
    ),
    agent=verifier
)