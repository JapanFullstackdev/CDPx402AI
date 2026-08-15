from __future__ import annotations
import os
from decimal import Decimal
from strands import tool
from agent.agentkit import create_agentkit, get_x402_payment_action
from agent.policies.spending import spending_manager

MARKET_API_URL = os.getenv("MARKET_API_URL", "http://127.0.0.1:8000")
PRICE_USD = Decimal(os.getenv("MARKET_PRICE_API_COST_USD", "0.001"))

def validate_symbol(symbol: str) -> str:
    normalized = symbol.upper().strip()
    if not 2 <= len(normalized) <= 10:
        raise ValueError("Invalid cryptocurrency symbol length.")
    if not normalized.isalnum():
        raise ValueError("Cryptocurrency symbol must contain only letters/numbers.")
    return normalized

async def _call_paid_market_api(symbol: str) -> str:
    spending_manager.authorize(PRICE_USD)
    agentkit = create_agentkit()
    action = get_x402_payment_action(agentkit)
    return action.invoke({
        "url": f"{MARKET_API_URL.rstrip('/')}/market-price",
        "method": "GET",
        "query_params": {"symbol": symbol},
    })

@tool
async def get_market_price(symbol: str) -> str:
    """Buy current cryptocurrency market data from the project's x402-protected market API."""
    return await _call_paid_market_api(validate_symbol(symbol))
