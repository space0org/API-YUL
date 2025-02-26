# BSVノードAPI

Bitcoin SVノードと対話するためのAPIです。

## 機能

- 公開鍵と秘密鍵のペア作成
- 残高確認
- 送金

## セットアップ手順

### 前提条件

- Python 3.12以上
- Poetry
- Docker（オプション）

### インストール

1. リポジトリをクローン
```bash
git clone https://github.com/space0org/API-YUL.git
cd API-YUL
```

2. 依存関係のインストール
```bash
poetry install
```

3. 環境変数の設定
```bash
export RPC_USER=bitcoin
export RPC_PASSWORD=bitcoin
export RPC_HOST=<BSVノードのIPアドレス>
export RPC_PORT=18332
```

### 起動方法

#### 開発モード
```bash
poetry run fastapi dev app/main.py
```

#### 本番モード
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 5000
```

#### Dockerを使用する場合
```bash
docker build -t bsv-node-api .
docker run -p 5000:5000 -e RPC_USER=bitcoin -e RPC_PASSWORD=bitcoin -e RPC_HOST=<BSVノードのIPアドレス> -e RPC_PORT=18332 bsv-node-api
```

## APIエンドポイント

### 1. 公開鍵と秘密鍵のペア作成

**リクエスト:**
```bash
curl -X POST https://app-fhxknmbw.fly.dev/api/keypair
```

**レスポンス:**
```json
{
  "address": "mxyz123...",
  "privateKey": "cxyz123..."
}
```

### 2. 残高確認

**リクエスト:**
```bash
curl -X GET https://app-fhxknmbw.fly.dev/api/balance/<アドレス>
```

**レスポンス:**
```json
{
  "address": "mxyz123...",
  "balance": 10.5,
  "unspentOutputs": [...]
}
```

### 3. 送金

**リクエスト:**
```bash
curl -X POST https://app-fhxknmbw.fly.dev/api/send \
  -H "Content-Type: application/json" \
  -d '{
    "fromAddress": "<送信元アドレス>",
    "privateKey": "<秘密鍵>",
    "toAddress": "<送信先アドレス>",
    "amount": <金額>
  }'
```

**レスポンス:**
```json
{
  "transactionId": "txyz123...",
  "fromAddress": "mxyz123...",
  "toAddress": "mabc123...",
  "amount": 1.5
}
```

### 4. ノード情報

**リクエスト:**
```bash
curl -X GET https://app-fhxknmbw.fly.dev/api/node/info
```

**レスポンス:**
```json
{
  "version": 101000800,
  "subversion": "/Bitcoin SV:1.0.8/",
  "connections": 2,
  "chain": "regtest",
  "blocks": 265,
  "difficulty": 4.656542373906925e-10
}
```

### 5. ヘルスチェック

**リクエスト:**
```bash
curl -X GET https://app-fhxknmbw.fly.dev/healthz
```

**レスポンス:**
```json
{
  "status": "ok"
}
```
