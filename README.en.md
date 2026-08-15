	# AI DeFi Agent

	🇯🇵 [日本語](README.md) | 🇺🇸 [英語](README.en.md)

	AI x Web3 portfolio project using Strands Agents, Coinbase AgentKit, a CDP-managed EVM wallet, x402 micropayments, Base Sepolia, and real CoinGecko market data.

	## Architecture

	User -> Strands Agent + LLM -> get_market_price() -> spending policy -> AgentKit x402 action -> CDP EVM wallet -> Base Sepolia USDC -> x402 FastAPI seller -> CoinGecko.

	## Structure

	```text
	ai-defi-agent/
	├── agent/
	│   ├── agent.py
	│   ├── agentkit.py
	│   ├── wallet/cdp_wallet.py
	│   ├── tools/market_data.py
	│   └── policies/spending.py
	├── server/market_api.py
	├── tests/test_spending.py
	├── .env.example
	├── .gitignore
	├── requirements.txt
	├── pyproject.toml
	└── README.md
	```

	## Setup

	Requires Python 3.10+, Coinbase Developer Platform credentials, an OpenAI API key, and Base Sepolia testnet assets.

	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	python -m pip install -r requirements.txt
	cp .env.example .env
	```

	Set `OPENAI_API_KEY`, `CDP_API_KEY_ID`, `CDP_API_KEY_SECRET`, `CDP_WALLET_SECRET`, and `X402_PAY_TO`. Never commit `.env`.

	## Seller

	```bash
	python -m uvicorn server.market_api:app --reload
	curl -i "http://127.0.0.1:8000/market-price?symbol=ETH"
	```

	The protected endpoint should return HTTP 402 until a valid x402 payment is attached.

	## Agent

	In another terminal:

	```bash
	python agent/agent.py
	```

	Then ask:

	```text
	What is the current ETH market price?
	```

	## Wallet model

	The agent uses `CdpEvmWalletProvider`; the application never receives or stores a private key. AgentKit's x402 provider obtains the wallet signer from the configured EVM wallet provider and performs the x402 payment flow.

	## Development chain

	Base Sepolia: `eip155:84532`.

	Use testnet funds only during development.

	## Security controls

	- CDP-managed wallet instead of a raw private key.
	- Service allowlist for x402 HTTP requests.
	- Maximum per-payment limit in the AgentKit x402 provider.
	- Independent application-level spending policy.
	- No secret values in source control.

	## Next extensions

	Add paid DeFi endpoints such as pool metrics, historical market data, volatility, token-risk checks, and a research budget that allows the agent to choose which external services to buy.

	## Official references

	Coinbase AgentKit Python: https://pypi.org/project/coinbase-agentkit/

	Coinbase AgentKit Strands extension: https://pypi.org/project/coinbase-agentkit-strands-agents/

	x402: https://docs.x402.org/

	CoinGecko API: https://docs.coingecko.com/
