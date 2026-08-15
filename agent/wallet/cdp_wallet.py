from __future__ import annotations
import os
from coinbase_agentkit import CdpEvmWalletProvider, CdpEvmWalletProviderConfig

def create_cdp_wallet_provider() -> CdpEvmWalletProvider:
    api_key_id = os.getenv("CDP_API_KEY_ID")
    api_key_secret = os.getenv("CDP_API_KEY_SECRET")
    wallet_secret = os.getenv("CDP_WALLET_SECRET")
    if not api_key_id:
        raise RuntimeError("CDP_API_KEY_ID is not configured.")
    if not api_key_secret:
        raise RuntimeError("CDP_API_KEY_SECRET is not configured.")
    if not wallet_secret:
        raise RuntimeError("CDP_WALLET_SECRET is not configured.")

    config = CdpEvmWalletProviderConfig(
        api_key_id=api_key_id,
        api_key_secret=api_key_secret,
        wallet_secret=wallet_secret,
        network_id=os.getenv("NETWORK_ID", "base-sepolia"),
        address=os.getenv("CDP_WALLET_ADDRESS") or None,
        idempotency_key=os.getenv("IDEMPOTENCY_KEY") or None,
    )
    return CdpEvmWalletProvider(config)
