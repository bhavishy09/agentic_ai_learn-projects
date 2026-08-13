import os
from crewai import Agent, Task, Crew, Process

# CrewAI requires an LLM provider configuration. 
# By default, it looks for OPENAI_API_KEY. We can set a placeholder here.
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "mock-key-for-demonstration"

# 1. Define Agent with Role, Goal and Backstory
researcher = Agent(
    role="Senior Security Analyst",
    goal="Scan Pull Request diffs for security vulnerabilities",
    backstory="Cybersecurity veteran specializing in automated static analysis."
)

# 2. Define Task
task = Task(
    description="Analyze PR diff for SQL injection risks. Code: 'SELECT * FROM users WHERE username = ' + user_input",
    expected_output="Detailed vulnerability breakdown and risk score",
    agent=researcher
)

# 3. Assemble and Run Crew
crew = Crew(agents=[researcher], tasks=[task], process=Process.sequential)

if __name__ == "__main__":
    print("[CrewAI Setup] Assembling security agent and task...")
    print("To run this successfully, ensure you have python dependencies installed:")
    print("  pip install crewai")
    print("And set the appropriate API key environment variable.")
    # We won't call kickoff here to avoid network errors unless run intentionally by user
    # result = crew.kickoff()
