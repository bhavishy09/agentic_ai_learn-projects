# Project 3: Deep Research & Strategy Co-Editing System

This project builds a collaborative system where a planning agent breaks down a research question, multiple search agents write facts into a shared scratchpad concurrently, a fact checker validates claims, and a synthesizer compiles the final report.

## Folder Structure
We recommend the following layout:
```text
deep_research_system/
├── README.md
├── src/
│   ├── agents.py        # Planner, Web Search, Fact Checker, Synthesizer agents
│   ├── scratchpad.py    # Thread manager / shared database context
│   └── main.py          # Script to run the research crew
├── requirements.txt
└── output_reports/      # Directory where generated Markdown reports are saved
```

## Implementation Checklist
1. [ ] **Choose Framework:** Use CrewAI (with `Process.hierarchical` or custom tasks) or LangGraph (with a shared context thread).
2. [ ] **Search Agent Tool:** Integrate Tavily Search API or DuckDuckGo Search API tools to allow agents to crawl the web.
3. [ ] **Fact Checker Prompting:** Design a verification prompt that checks if claims in the draft are backed by the URLs retrieved by the search agents.
4. [ ] **Synthesizer Agent:** Formulate Markdown rendering rules to write structured, header-rich summaries with proper citations.
