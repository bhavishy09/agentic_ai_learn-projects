# Day 1: Agentic AI & Multi-Agent Workflows
## Study Guide, Framework Matrix & Code Explanations

This document summarizes the core topics, communication models, framework comparisons, and code implementations detailed in the *Agentic AI Complete Handbook*.

---

## 1. Core Architectural Concepts

### Single-Agent vs. Multi-Agent Systems
* **Single Agent Limitations:** Trying to handle research, coding, security audits, and formatting in a single prompt causes **context window bloat**, degradation of instruction following, and increased **hallucination rates**.
* **Multi-Agent Advantage:** Breaking a large task into a coordinated team of specialized agents, each having a single responsibility, specific tools, and clear context.
  * *Context Window Optimization:* Prevents performance degradation by giving few tools to specialized micro-agents.
  * *Cost & Speed Efficiency:* Allows routing simple tasks to cheaper/faster models (e.g., Claude 3.5 Haiku, GPT-4o-mini) and reserving reasoning models (e.g., Claude 3.5 Sonnet, o3) for complex synthesis.
  * *Cross-Validation:* Enables critic nodes (e.g., Agent B) to validate the outputs of generator nodes (e.g., Agent A).
  * *Fault Tolerance:* Allows updating or debugging a single node without affecting the entire system.

### 2. Multi-Agent Architectural Interaction Patterns

| Architecture Type | Mechanics | Strengths | Gotchas / Failure Modes | Real-World Example |
| :--- | :--- | :--- | :--- | :--- |
| **1. Sequential** | Deterministic assembly line: `Agent A` $\rightarrow$ `Agent B` $\rightarrow$ `Agent C` | Low latency, highly predictable, easy to debug | Error propagation (flawed output from A corrupts downstream agents) | **ETL Invoice Pipeline:** PDF Extractor $\rightarrow$ PII Sanitizer $\rightarrow$ Database Formatter |
| **2. Collaborative** | Shared scratchpad / thread read-write workspace | Complete visibility, dynamic co-editing | Context window bloat, high token costs from verbose logs | **Deep Research Draft Co-editing:** Fact Checker + Search Agent |
| **3. Hierarchical** | Central Supervisor agent dispatches sub-agents as tools | Modular delegation, clear authority structure | Supervisor bottlenecking or routing confusion with many sub-agents | **Customer Support Help Desk:** Supervisor $\rightarrow$ Billing / Support / Refund Agent |
| **4. Network** | Decentralized peer-to-peer handoffs between agents | Extremely flexible, handles dynamic loops naturally | Hard to debug; risk of infinite routing loops between agents | **Software Debugging Loop:** Coder Agent $\leftrightarrow$ Tester Agent $\rightarrow$ Deployment Agent |

---

## 3. Communication Models

1. **Shared Scratchpad Model:** All agents read from and write to a single message history. Very transparent, but passes unnecessary intermediate logs, leading to context bloat.
2. **Handoff-Based (`Command` Pattern):** Agents return structured `Command(goto="target_agent", update={...})` objects. Only targeted payloads are passed, preventing context bloat.
3. **Tool-Calling Architecture:** Sub-agents are wrapped inside function schemas, and the supervisor executes them as standard tool calls.

---

## 4. Framework Decision Matrix

| Framework | Mental Model / Paradigm | Best Use Case | Key Strengths | Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **LangGraph** | State Graph / Circuit Machine | Enterprise Production & Complex Workflows | Precise state control, `Command` handoffs, persistence, time-travel, LangSmith tracing | Steeper learning curve, requires explicit state schema design |
| **CrewAI** | Role-Based Team Abstractions | Rapid Prototyping & Business Processes | Human-like abstractions (`Agent`, `Task`, `Crew`), YAML configs, fast setup | Less granular execution control than low-level graphs |
| **AutoGen** | Conversational Group Chat | Research & Sandbox Experimentation | Intuitive chat metaphor, multi-model flexibility, built-in code sandboxes | Unstructured control flow, difficult deterministic guarantees |
| **Temporal** | Durable Execution Engine | Mission-Critical, Long-Running Systems | Crash-resilient state recovery, activity retries, timeouts across days/weeks | Not an LLM framework natively; wraps LLM calls in durable activities |
| **Google ADK** | Enterprise Software Framework | Google Cloud / Vertex AI Native Apps | Software-first architecture, `AgentEvaluator`, audio/video streaming support | Tightly coupled with Google Cloud ecosystem |
| **LlamaIndex Workflow** | Event-Driven RAG Workflows | Data-Heavy & Multi-Index RAG Systems | Deep vector index integration, handoffs as first-class tools | Focused mainly on retrieval-heavy workloads |
| **OpenAI Swarm** | Stateless Function Handoffs | Lightweight Prototyping & Educational Use | Minimalist API, lightweight routine handoffs | Experimental, single-loop control without built-in state persistence |

---

## 5. Important Code Snippets & Detailed Explanations

### 5.1 LangGraph Dynamic Routing with Loop Counter Guard (Python)
This snippet implements a code security audit loop. A security agent checks for vulnerabilities. If found, it routes to a refactoring agent to fix the code, which then routes back. 
An **Infinite Loop Guard** using `retry_count` is implemented to prevent the agents from ping-ponging forever if the vulnerability remains.

> [!IMPORTANT]
> **Developer Correction:** The original handbook snippet contained a syntax error where an f-string used unescaped newlines in standard double quotes. This has been corrected below using `\n` in the string literal.

```python
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
    # Simplistic static check for vulnerable functions
    has_vuln = "eval(" in diff or "exec(" in diff
    
    # Check if max retries (3) exceeded
    if has_vuln and state.get("retry_count", 0) < 3:
        target = "refactoring_agent"
    else:
        target = "reporter_agent" # Fallback if clean or max retries hit
        
    return Command(goto=target, update={"vulnerabilities_found": has_vuln})

# 3. Refactoring Agent with Loop Increment
def refactoring_agent(state: AuditState):
    retries = state.get("retry_count", 0) + 1
    # Apply a replacement to simulate code refactoring
    fixed_code = state["code_diff"].replace("eval(", "safe_eval(")
    
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
        # Corrected from original PDF syntax error: used '\n' instead of direct line break in string
        summary = f"Refactored Code:\n{state['code_diff']}"
        
    return {"summary": summary}

# 5. Build Graph
workflow = StateGraph(AuditState)
workflow.add_node("security_agent", security_agent)
workflow.add_node("refactoring_agent", refactoring_agent)
workflow.add_node("reporter_agent", reporter_agent)

workflow.add_edge(START, "security_agent")
workflow.add_edge("reporter_agent", END)

app = workflow.compile()
```

#### Code Walkthrough:
* **`AuditState` (TypedDict):** Holds the application state. It acts as the database for this workflow.
* **`Command` Primitive:** This is LangGraph's native handoff object. It updates the state (`update`) and dynamically directs the flow of execution (`goto`) to another node in the graph, skipping standard routing logic.
* **Loop Guard (`retry_count`):** The `security_agent` routes to `refactoring_agent` only if the vulnerability exists and `retry_count < 3`. Otherwise, it routes to `reporter_agent` to raise a warning. This prevents infinite cycles.

---

### 5.2 LangGraph Financial Loan Pipeline with Dynamic Branching
This workflow implements a loan evaluation process where applications are evaluated based on a credit score. If the score is low ($< 650$), execution routes to a human reviewer. If high, it goes to auto-approval.

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

class LoanState(TypedDict):
    applicant_id: str
    credit_score: int
    decision: str

def credit_agent(state: LoanState):
    target = "manual_reviewer" if state["credit_score"] < 650 else "auto_approval"
    return Command(goto=target, update={"decision": "Pending Evaluation"})

def auto_approval(state: LoanState):
    return {"decision": "APPROVED"}

def manual_reviewer(state: LoanState):
    return {"decision": "ESCALATED_TO_HUMAN_OFFICER"}

workflow = StateGraph(LoanState)
workflow.add_node("credit_agent", credit_agent)
workflow.add_node("auto_approval", auto_approval)
workflow.add_node("manual_reviewer", manual_reviewer)

workflow.add_edge(START, "credit_agent")
workflow.add_edge("auto_approval", END)
workflow.add_edge("manual_reviewer", END)

app = workflow.compile()
```

#### Code Walkthrough:
* **Dynamic Routing:** Instead of defining fixed edges between nodes, `credit_agent` decides the next node (`manual_reviewer` vs `auto_approval`) dynamically based on `state["credit_score"]`.

---

### 5.3 CrewAI Role-Based Team Setup
CrewAI abstracts multi-agent systems as a corporate crew with roles, goals, and backstories.

```python
from crewai import Agent, Task, Crew, Process

# 1. Define Agent with Role & Backstory
researcher = Agent(
    role="Senior Security Analyst",
    goal="Scan Pull Request diffs for security vulnerabilities",
    backstory="Cybersecurity veteran specializing in automated static analysis."
)

# 2. Define Task
task = Task(
    description="Analyze PR diff for SQL injection risks",
    expected_output="Detailed vulnerability breakdown and risk score",
    agent=researcher
)

# 3. Assemble and Run Crew
crew = Crew(agents=[researcher], tasks=[task], process=Process.sequential)
result = crew.kickoff()
```

#### Code Walkthrough:
* **`Agent` class:** Uses high-level human metaphors (`role`, `goal`, `backstory`) which are translated into system prompts under the hood.
* **`Crew` execution:** The `kickoff()` method starts execution, passing the output of previous tasks to subsequent ones (here configured as a `Process.sequential` workflow).

---

### 5.4 AutoGen Conversational Pair-Programming Loop
AutoGen uses agent conversations to solve tasks. It features built-in code execution sandboxes.

```python
from autogen import AssistantAgent, UserProxyAgent

# 1. Coder Agent
coder = AssistantAgent(
    name="Coder",
    llm_config={"config_list": [{"model": "gpt-4o"}]}
)

# 2. User Proxy Agent (represents user, runs code)
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding", "use_docker": False}
)

# 3. Start Chat
user_proxy.initiate_chat(
    coder, 
    message="Write a Python script to fetch stock prices from Yahoo Finance."
)
```

#### Code Walkthrough:
* **`UserProxyAgent`:** Can execute the python scripts written by the `AssistantAgent` locally or inside a Docker container, feeding output back into the chat context.

---

### 5.5 Temporal Durable Workflow Activity Wrapper
Temporal ensures durable execution. If a server crashes mid-execution, Temporal resumes exactly where it stopped.

```python
from datetime import timedelta
from temporalio import workflow

@workflow.defn
class CustomerOnboardingWorkflow:
    @workflow.run
    async def run(self, user_id: str) -> str:
        # Executes an agent activity reliably
        parsed_doc = await workflow.execute_activity(
            "run_doc_parser_agent",
            user_id,
            schedule_to_close_timeout=timedelta(minutes=5)
        )
        return f"Completed onboarding for {user_id}"
```

#### Code Walkthrough:
* **`@workflow.defn` & `@workflow.run`:** Standard temporal decorators that define a stateful, durable workflow.
* **`execute_activity`:** Invokes long-running actions (such as parsing a passport using an LLM) with built-in retries, timeouts, and checkpointing.
