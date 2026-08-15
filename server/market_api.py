from datetime import datetime, timezone
import os
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption
from x402.http.middleware.fastapi import PaymentMiddlewareASGI
from x402.http.types import RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme
from x402.server import x402ResourceServer

X402_PAY_TO = os.getenv("X402_PAY_TO")
if not X402_PAY_TO:
    raise RuntimeError("X402_PAY_TO environment variable is required.")

X402_NETWORK = "eip155:84532"
X402_PRICE = f"${os.getenv('MARKET_PRICE_API_COST_USD', '0.001')}"
X402_FACILITATOR_URL = "https://x402.org/facilitator"
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

app = FastAPI(title="AI DeFi Agent - Market API", version="0.2.0")

class MarketPriceResponse(BaseModel):
    symbol: str
    price_usd: float
    source: str
    timestamp: datetime

COIN_IDS: dict[str, str] = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "USDC": "usd-coin",
}

facilitator = HTTPFacilitatorClient(FacilitatorConfig(url=X402_FACILITATOR_URL))
x402_server = x402ResourceServer(facilitator)
x402_server.register(X402_NETWORK, ExactEvmServerScheme())

routes = {
    "GET /market-price": RouteConfig(
        accepts=[PaymentOption(scheme="exact", pay_to=X402_PAY_TO, price=X402_PRICE, network=X402_NETWORK)],
        mime_type="application/json",
        description="Current cryptocurrency market price in USD",
    )
}
app.add_middleware(PaymentMiddlewareASGI, routes=routes, server=x402_server)

async def fetch_market_price(symbol: str) -> float:
    coin_id = COIN_IDS.get(symbol)
    if coin_id is None:
        raise HTTPException(status_code=404, detail=f"Unsupported symbol: {symbol}")

    headers = {"Accept": "application/json"}
    api_key = os.getenv("COINGECKO_API_KEY")
    if api_key:
        headers["x-cg-demo-api-key"] = api_key

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{COINGECKO_BASE_URL}/simple/price",
                params={"ids": coin_id, "vs_currencies": "usd"},
                headers=headers,
            )
        response.raise_for_status()
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="Market-data provider timed out.") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"Market-data provider returned HTTP {exc.response.status_code}.") from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail="Could not connect to market-data provider.") from exc

    data: dict[str, Any] = response.json()
    try:
        return float(data[coin_id]["usd"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=502, detail="Unexpected response from market-data provider.") from exc

@app.get("/market-price", response_model=MarketPriceResponse)
async def get_market_price(symbol: str = Query(..., min_length=2, max_length=10)) -> MarketPriceResponse:
    symbol = symbol.upper().strip()
    price = await fetch_market_price(symbol)
    return MarketPriceResponse(
        symbol=symbol,
        price_usd=price,
        source="CoinGecko",
        timestamp=datetime.now(timezone.utc),
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
