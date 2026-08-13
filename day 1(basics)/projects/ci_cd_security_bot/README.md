# Project 2: Autonomous CI/CD Code Security Audit & Refactoring Bot

This project runs inside a GitHub Action workflow to check code changes on new Pull Requests, automatically suggest fixes for any vulnerabilities, verify the fixes, and write back to the PR comments.

## Folder Structure
We recommend the following layout:
```text
ci_cd_security_bot/
├── README.md
├── .github/
│   └── workflows/
│       └── security_audit.yml  # GitHub Actions trigger script
├── src/
│   ├── agents.py               # Security Agent, Refactoring Agent, Reporter Agent
│   ├── graph.py                # Graph composition and loop guard logic
│   └── main.py                 # Action runner entry point
├── tests/                      # Vulnerable dummy code files for testing
├── Dockerfile                  # To package the agent runner
└── requirements.txt
```

## Implementation Checklist
1. [ ] **GitHub Webhook Integration:** Read PR diff contents from environmental variables in GitHub Actions.
2. [ ] **State Graph & Loop Guard:** Implement `AuditState` including a `retry_count`. Ensure that if vulnerabilities persist after 3 refactoring attempts, the graph escalates to manual review.
3. [ ] **Audit Agent:** Leverage basic string checks or static analysis tools (e.g., Semgrep) to identify unsafe API calls.
4. [ ] **Refactoring Agent:** Program the LLM to output ONLY corrected, working python code with the vulnerabilities patched.
5. [ ] **Reporter Agent:** Use the GitHub REST API (or PyGithub library) to post comments onto the target PR thread.
