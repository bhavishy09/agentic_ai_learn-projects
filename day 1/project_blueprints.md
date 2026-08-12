# Capstone Project Blueprints

This document outlines the four production-grade multi-agent capstone projects described in the *Agentic AI Complete Handbook*. 

---

## 1. Project Blueprint 1: Financial Loan Approval Pipeline
### Architecture Pattern: Hierarchical Supervisor + Dynamic Routing

```mermaid
graph TD
    Start([Applicant submits Loan Application]) --> Extractor[Extractor Agent]
    Extractor --> CreditCheck[Credit Check Agent]
    CreditCheck --> Supervisor{Supervisor Node}
    
    Supervisor -->|Credit Score >= 650| AutoApprove[Auto-Approval Agent]
    Supervisor -->|Credit Score < 650| ManualReview[Manual Reviewer Node]
    
    AutoApprove --> Approved([APPROVED])
    ManualReview -->|Human Decision| Approved
    ManualReview -->|Human Decision| Rejected([REJECTED])
```

* **Workflow Mechanics:**
  1. **Extractor Agent:** Receives unstructured loan applications (PDFs) and uses structured output parsing (e.g., Pydantic) to extract names, IDs, income, and requested loan amount into structured JSON.
  2. **Credit Check Agent:** Queries credit databases/APIs to evaluate the applicant's credit score and history.
  3. **Supervisor Node:** Evaluates the credit profile. If the credit score is $\ge 650$, it dynamically routes the execution to the `Auto-Approval Agent`. If the credit score is $< 650$, it routes the flow to the `Manual Reviewer Node`, pausing execution for human compliance verification.
* **Tech Stack:** LangGraph, Pydantic, PostgreSQL, FastAPI.

---

## 2. Project Blueprint 2: Autonomous CI/CD Code Security Audit & Refactoring Bot
### Architecture Pattern: Network State Graph with Infinite Loop Counter Guards

```mermaid
graph TD
    Trigger([GitHub Webhook: Pull Request Created]) --> Parallel[Run Audits in Parallel]
    Parallel --> Security[Security Audit Agent]
    Parallel --> Performance[Performance Audit Agent]
    
    Security & Performance --> Decision{Vulnerabilities Found?}
    Decision -->|No| Summary[PR Summary Agent]
    Decision -->|Yes| Refactor[Refactoring Agent]
    
    Refactor --> Increment[Increment retry_count]
    Increment --> CheckRetry{retry_count >= 3?}
    
    CheckRetry -->|Yes| ManualEscalation[Manual Escalation Node]
    CheckRetry -->|No| Security
    
    Summary --> PRComment([Post Markdown Comment to GitHub PR])
    ManualEscalation --> PRComment
```

* **Workflow Mechanics:**
  1. **Trigger:** Activated via a GitHub Action Webhook when a developer creates a new Pull Request.
  2. **Parallel Audit:** The `Security Audit Agent` and `Performance Audit Agent` run in parallel to scan the code diff for security flaws (e.g., SQL injections, remote code execution) and performance bottlenecks.
  3. **Self-Correction Loop:** If vulnerabilities are found, the `Refactoring Agent` generates code fixes, updates the graph state, increments a `retry_count`, and loops back to the audit agents.
  4. **Loop Guard:** If `retry_count >= 3`, the loop stops and routes to a human reviewer node to prevent infinite ping-pong loops.
  5. **Reporting:** A `PR Summary Agent` compiles the results into a clean markdown table and posts it as a PR comment.
* **Tech Stack:** LangGraph, GitHub REST API, Semgrep, Python REPL, Docker.

---

## 3. Project Blueprint 3: Deep Research & Strategy Co-Editing System
### Architecture Pattern: Collaborative Shared Scratchpad + Supervisor Synthesis

```mermaid
graph TD
    Query([User Research Query]) --> Planner[Planner Agent]
    Planner -->|Deconstructs into 5 plans| SharedScratchpad[Shared Scratchpad / Context Thread]
    
    SharedScratchpad <--> Search1[Web Search Agent 1]
    SharedScratchpad <--> Search2[Web Search Agent 2]
    SharedScratchpad <--> Search3[Web Search Agent 3]
    
    SharedScratchpad --> FactChecker[Fact Checker Agent]
    FactChecker -->|Validates Claims| SharedScratchpad
    
    SharedScratchpad --> Synthesizer[Synthesizer Agent]
    Synthesizer --> Report([Final Markdown/LaTeX Report])
```

* **Workflow Mechanics:**
  1. **Planner Agent:** Takes a broad research topic from a user and deconstructs it into 5 sub-topic research plans.
  2. **Web Search Agents:** Three concurrent web search agents fetch real-time search engine results and dump raw facts/summaries into a shared scratchpad message thread.
  3. **Fact Checker Agent:** Reads the shared scratchpad and validates statements against source URLs to filter out hallucinated content.
  4. **Synthesizer Agent:** Synthesizes the verified facts into a polished, comprehensive research paper/report in Markdown or LaTeX format.
* **Tech Stack:** CrewAI or LangGraph, Tavily Search API, Claude 3.5 Sonnet.

---

## 4. Project Blueprint 4: Enterprise Customer Onboarding & KYC Workflow
### Architecture Pattern: Temporal Durable Execution wrapping Multi-Agent Nodes

```mermaid
graph TD
    Start([User Registration]) --> Parser[Document Parser Agent]
    Parser --> KYC[KYC Verification Agent]
    KYC --> Sleep[Durable Sleep Node]
    Sleep -->|Webhook Trigger| HumanApproval{Human Compliance Approval?}
    
    HumanApproval -->|Approved| Contract[Contract Generation Agent]
    HumanApproval -->|Rejected| Terminate([Send Rejection Email])
    
    Contract --> PDF([Generate Custom Agreement PDF])
```

* **Workflow Mechanics:**
  1. **Document Parser Agent:** Extracts and validates passport/ID details from uploaded documents.
  2. **KYC Verification Agent:** Performs checks (blacklist search, address verification, database query).
  3. **Durable Wait Node:** Execution enters a durable sleep node (powered by Temporal) waiting for human compliance webhook approval (can sleep safely for days/weeks without losing state).
  4. **Contract Generation Agent:** Upon approval, it constructs a customized customer onboarding agreement and compiles it into a downloadable PDF format.
* **Tech Stack:** Temporal Python SDK, LangChain, WeasyPrint, Redis.
