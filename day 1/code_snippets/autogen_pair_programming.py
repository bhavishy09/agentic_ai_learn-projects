from autogen import AssistantAgent, UserProxyAgent

# 1. Define Coder Agent
coder = AssistantAgent(
    name="Coder",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": "mock-api-key"}]}
)

# 2. Define User Proxy Agent (represents user, runs code)
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding", "use_docker": False}
)

if __name__ == "__main__":
    print("[AutoGen Setup] Instantiated Coder and UserProxy agents.")
    print("To run this successfully, ensure you have python dependencies installed:")
    print("  pip install pyautogen")
    print("And set the appropriate API configuration list.")
    # Example call:
    # user_proxy.initiate_chat(
    #     coder, 
    #     message="Write a Python script to fetch stock prices from Yahoo Finance."
    # )
