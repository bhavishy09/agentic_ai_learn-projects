# Project 1: Financial Loan Approval Pipeline

This project builds a stateful loan approval pipeline using LangGraph. It extracts data from application documents, verifies credit, and routes the application to automatic approval or manual review.

## Folder Structure
We recommend the following layout:
```text
loan_approval_pipeline/
├── README.md
├── app/
│   ├── __init__.py
│   ├── agents.py       # Extractor, Credit Check, Supervisor, Reviewer nodes
│   ├── state.py        # TypedDict Schema for graph state
│   ├── db.py           # PostgreSQL/Mock connection for credit checks
│   └── main.py         # Entrypoint to run the compiled LangGraph app
├── requirements.txt
└── test_applications/  # Mock PDFs/txt applications
```

## Implementation Checklist
1. [ ] **Define State Schema (`state.py`):** Use `TypedDict` to track applicant details, credit score, decision status, and review history.
2. [ ] **Extractor Agent (`agents.py`):** Use an LLM with Pydantic structured output (`with_structured_output`) to parse unstructured loan application text.
3. [ ] **Credit Check Agent (`agents.py`):** Implement database checks to retrieve mock credit scores.
4. [ ] **Supervisor Agent (`agents.py`):** Define dynamic routing using LangGraph's `Command` pattern.
5. [ ] **Run and Test (`main.py`):** Feed mock applications and verify routing behavior.
