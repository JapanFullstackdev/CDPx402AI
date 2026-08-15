from __future__ import annotations
import os
from coinbase_agentkit import AgentKit, AgentKitConfig, x402_action_provider
from coinbase_agentkit.action_providers.x402 import X402Config
from agent.wallet.cdp_wallet import create_cdp_wallet_provider

MARKET_API_URL = os.getenv("MARKET_API_URL", "http://127.0.0.1:8000")
MARKET_SERVICE = MARKET_API_URL.rstrip("/") + "/"
MAX_PAYMENT_USDC = float(os.getenv("X402_MAX_PAYMENT_USDC", "0.01"))

def create_agentkit() -> AgentKit:
    wallet_provider = create_cdp_wallet_provider()
    x402_config = X402Config(
        registered_services=[MARKET_SERVICE],
        allow_dynamic_service_registration=False,
        max_payment_usdc=MAX_PAYMENT_USDC,
    )
    return AgentKit(AgentKitConfig(
        wallet_provider=wallet_provider,
        action_providers=[x402_action_provider(x402_config)],
    ))

def get_action(agentkit: AgentKit, action_name: str):
    actions = agentkit.get_actions()
    for action in actions:
        if action.name == action_name:
            return action
    raise RuntimeError(f"AgentKit action '{action_name}' was not found. Available actions: {[a.name for a in actions]}")

def get_x402_payment_action(agentkit: AgentKit):
    return get_action(agentkit, "make_http_request_with_x402")
