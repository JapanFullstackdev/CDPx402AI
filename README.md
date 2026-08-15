# AI DeFiエージェント

🇯🇵 [日本語](README.md) | 🇺🇸 [英語](README.en.md)

Strands Agents、Coinbase AgentKit、CDP管理EVMウォレット、x402マイクロペイメント、Base Sepolia、そしてCoinGeckoの実際の市場データを用いた、AIとWeb3を組み合わせたポートフォリオプロジェクトです。

## アーキテクチャ

ユーザー → Strands Agent + LLM → get_market_price() → 支出ポリシー → AgentKit x402アクション → CDP EVMウォレット → Base Sepolia USDC → x402 FastAPIセラー → CoinGecko

## 構造

```text

ai-defi-agent/

├── agent/

│ ├── agent.py

│ ├── agentkit.py

│ ├── wallet/cdp_wallet.py

│ ├── tools/market_data.py

│ └── policies/spending.py

├── server/market_api.py

├── tests/test_spending.py

├── .env.example

├── .gitignore

├── requirements.txt

├── pyproject.toml

└── README.md

```

## セットアップ

Python 3.10以降、Coinbase Developer Platformの認証情報、OpenAI APIキー、およびBase Sepoliaテストネットのアセットが必要です。

```bash

python3 -m venv .venv

source .venv/bin/activate

python -m pip install -r requirements.txt

cp .env.example .env
```

`OPENAI_API_KEY`、`CDP_API_KEY_ID`、`CDP_API_KEY_SECRET`、`CDP_WALLET_SECRET`、および`X402_PAY_TO`を設定してください。`.env`は絶対にコミットしないでください。

## 販売者

```bash

python -m uvicorn server.market_api:app --reload

curl -i "http://127.0.0.1:8000/market-price?symbol=ETH"

```

有効なX402決済が添付されるまで、保護されたエンドポイントはHTTP 402エラーを返す必要があります。


## エージェント

別のターミナルで、以下のコマンドを実行してください。

```bash

python agent/agent.py

```

次に、以下のコマンドを入力してください。

```text

現在のETH市場価格はいくらですか？

```

## ウォレットモデル

エージェントは`CdpEvmWalletProvider`を使用します。アプリケーションは秘密鍵を受け取ったり保存したりすることはありません。AgentKitのx402プロバイダは、設定済みのEVMウォレットプロバイダからウォレット署名者を取得し、x402決済フローを実行します。

## 開発チェーン

ベースチェーン：Sepolia `eip155:84532`

開発中はテストネットの資金のみを使用してください。

## セキュリティ対策

- 生の秘密鍵ではなく、CDP管理ウォレットを使用します。

- x402 HTTPリクエストのサービス許可リストを使用します。

- AgentKit x402プロバイダにおける決済ごとの最大限度額を設定します。

- アプリケーションレベルで独立した支出ポリシーを設定します。

- ソースコード管理に秘密値を含めません。


## 今後の拡張機能

プールメトリクス、過去の市場データ、ボラティリティ、トークンリスクチェックなどの有料DeFiエンドポイント、およびエージェントが外部サービスを選択できるリサーチ予算を追加します。

## 公式リファレンス

Coinbase AgentKit Python: https://pypi.org/project/coinbase-agentkit/

Coinbase AgentKit Strands拡張機能: https://pypi.org/project/coinbase-agentkit-strands-agents/

x402: https://docs.x402.org/

CoinGecko API: https://docs.coingecko.com/
