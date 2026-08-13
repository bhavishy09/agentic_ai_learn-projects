from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

# 1. State Definition with Loop Guard
class AuditState(TypedDict):
    code_diff: str
    vulnerabilities_found: bool
    retry_count: int
    summary: str

# 2. Security Inspector Agent
def security_agent(state: AuditState):
    diff = state["code_diff"]
    # Check if code has unsafe constructs
    has_vuln = "eval(" in diff or "exec(" in diff
    
    # Check if max retries (3) exceeded
    if has_vuln and state.get("retry_count", 0) < 3:
        target = "refactoring_agent"
    else:
        target = "reporter_agent" # Fallback if clean or max retries hit
        
    print(f"[Security Agent] Checked diff. Vulnerabilities found: {has_vuln}. Routing to: {target}")
    return Command(goto=target, update={"vulnerabilities_found": has_vuln})

# 3. Refactoring Agent with Loop Increment
def refactoring_agent(state: AuditState):
    retries = state.get("retry_count", 0) + 1
    # Replace unsafe 'eval(' with a placeholder 'safe_eval('
    fixed_code = state["code_diff"].replace("eval(", "safe_eval(")
    
    print(f"[Refactoring Agent] Attempt {retries} to refactor code. Routing back to: security_agent")
    # Handoff back to security agent for verification
    return Command(
        goto="security_agent", 
        update={"code_diff": fixed_code, "retry_count": retries}
    )

# 4. Reporter Agent
def reporter_agent(state: AuditState):
    if state["vulnerabilities_found"] and state.get("retry_count", 0) >= 3:
        summary = "CRITICAL: Auto-refactoring retry limit reached (3 attempts). Manual review required."
    elif not state["vulnerabilities_found"]:
        summary = "Code Security Passed successfully. PR approved for merge!"
    else:
        summary = f"Refactored Code:\n{state['code_diff']}"
        
    print(f"[Reporter Agent] Final Summary:\n{summary}")
    return {"summary": summary}

# 5. Build Graph
workflow = StateGraph(AuditState)
workflow.add_node("security_agent", security_agent)
workflow.add_node("refactoring_agent", refactoring_agent)
workflow.add_node("reporter_agent", reporter_agent)

workflow.add_edge(START, "security_agent")
workflow.add_edge("reporter_agent", END)

app = workflow.compile()

# Example execution to demonstrate workflow
if __name__ == "__main__":
    print("--- Running security audit graph with clean code ---")
    initial_state_clean = {
        "code_diff": "def add(a, b):\n    return a + b\n",
        "vulnerabilities_found": False,
        "retry_count": 0,
        "summary": ""
    }
    result_clean = app.invoke(initial_state_clean)
    
    print("\n--- Running security audit graph with vulnerable code ---")
    initial_state_vuln = {
        "code_diff": "def execute_code(user_input):\n    eval(user_input)\n",
        "vulnerabilities_found": False,
        "retry_count": 0,
        "summary": ""
    }
    result_vuln = app.invoke(initial_state_vuln)
