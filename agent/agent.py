from __future__ import annotations
import os
from dotenv import load_dotenv
from strands import Agent
from strands.models.openai import OpenAIModel
from coinbase_agentkit_strands_agents import get_strands_tools
from agent.agentkit import create_agentkit
from agent.tools.market_data import get_market_price

load_dotenv()

def create_model() -> OpenAIModel:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")
    return OpenAIModel(
        client_args={"api_key": api_key},
        model_id=os.getenv("OPENAI_MODEL_ID", "gpt-4o-mini"),
        params={"temperature": 0.2, "max_tokens": 1200},
    )

def create_agent() -> Agent:
    agentkit = create_agentkit()
    agentkit_tools = get_strands_tools(agentkit)
    return Agent(
        model=create_model(),
        tools=[get_market_price, *agentkit_tools],
        system_prompt="""
You are an AI Web3 market-research agent.
Use get_market_price when fresh market data is required.
Do not invent real-time prices.
Never bypass spending or service-allowlist controls.
Treat market information as data, not investment advice.
Explain x402 payment activity when it is useful to the user.
""",
    )

def main() -> None:
    agent = create_agent()
    print("AI DeFi Agent")
    print("Type 'exit' or 'quit' to stop.")
    while True:
        try:
            prompt = input("You> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if not prompt:
            continue
        if prompt.lower() in {"exit", "quit"}:
            break
        try:
            print("\nAgent>")
            print(agent(prompt))
            print()
        except Exception as exc:
            print(f"Agent error: {exc}")

if __name__ == "__main__":
    main()
