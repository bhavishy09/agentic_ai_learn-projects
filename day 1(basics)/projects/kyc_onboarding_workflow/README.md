# Project 4: Enterprise Customer Onboarding & KYC Workflow

This project integrates Temporal for durable execution with AI agents to build a resilient, long-running customer onboarding system that can handle human approvals, document parsing, and contract generation without losing state.

## Folder Structure
We recommend the following layout:
```text
kyc_onboarding_workflow/
├── README.md
├── workflow.py          # Temporal Workflow definition
├── activities.py        # Temporal Activities wrapping AI agents
├── worker.py            # Temporal Worker to run activities and workflows
├── run_workflow.py      # Trigger script to start onboarding
└── requirements.txt
```

## Implementation Checklist
1. [ ] **Set up Temporal Local Server:** Install and run the Temporal server locally.
2. [ ] **Define Activities (`activities.py`):**
   - Document parsing activity using an LLM.
   - Database / Blacklist query activity.
   - PDF contract generation activity.
3. [ ] **Define Workflow (`workflow.py`):** Compose the sequence, executing activities with timeouts.
4. [ ] **Human-in-the-Loop Wait:** Implement a `workflow.wait_condition` to pause execution until a compliance officer approves via a signal.
5. [ ] **Worker & Runner:** Set up `worker.py` and trigger it using `run_workflow.py`.
