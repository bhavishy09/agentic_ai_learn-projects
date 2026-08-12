from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

class LoanState(TypedDict):
    applicant_id: str
    credit_score: int
    decision: str

def credit_agent(state: LoanState):
    target = "manual_reviewer" if state["credit_score"] < 650 else "auto_approval"
    print(f"[Credit Agent] Credit score is {state['credit_score']}. Routing application to: {target}")
    return Command(goto=target, update={"decision": "Pending Evaluation"})

def auto_approval(state: LoanState):
    print("[Auto Approval Agent] Automatically approving loan request.")
    return {"decision": "APPROVED"}

def manual_reviewer(state: LoanState):
    print("[Manual Review Agent] Escolating application for human verification.")
    return {"decision": "ESCALATED_TO_HUMAN_OFFICER"}

workflow = StateGraph(LoanState)
workflow.add_node("credit_agent", credit_agent)
workflow.add_node("auto_approval", auto_approval)
workflow.add_node("manual_reviewer", manual_reviewer)

workflow.add_edge(START, "credit_agent")
workflow.add_edge("auto_approval", END)
workflow.add_edge("manual_reviewer", END)

app = workflow.compile()

if __name__ == "__main__":
    print("--- Evaluating High Credit Score Applicant ---")
    high_score = app.invoke({"applicant_id": "APP_001", "credit_score": 720, "decision": ""})
    print(f"Final Decision: {high_score['decision']}")
    
    print("\n--- Evaluating Low Credit Score Applicant ---")
    low_score = app.invoke({"applicant_id": "APP_002", "credit_score": 580, "decision": ""})
    print(f"Final Decision: {low_score['decision']}")
