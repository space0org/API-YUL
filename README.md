# BSVノードAPI

Bitcoin SVノードと対話するためのAPIです。JpyNetworkとLariNetworkの両方をサポートしています。

## 機能

- 公開鍵と秘密鍵のペア作成
- 残高確認（ネットワーク指定可能）
- 送金（ネットワーク指定可能）
- ノード情報取得（ネットワーク指定可能）

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
# JpyNetwork設定
export JPY_RPC_USER=jpyuser
export JPY_RPC_PASSWORD=jpypassword
export JPY_RPC_HOST=localhost
export JPY_RPC_PORT=18332

# LariNetwork設定
export LARI_RPC_USER=lariuser
export LARI_RPC_PASSWORD=laripassword
export LARI_RPC_HOST=localhost
export LARI_RPC_PORT=19332
```

### 起動方法

#### 開発モード
```bash
poetry run fastapi dev app/main.py
```

#### 本番モード
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 5002
```

#### Dockerを使用する場合
```bash
docker build -t bsv-node-api .
docker run -p 5002:5002 \
  -e JPY_RPC_USER=jpyuser \
  -e JPY_RPC_PASSWORD=jpypassword \
  -e JPY_RPC_HOST=localhost \
  -e JPY_RPC_PORT=18332 \
  -e LARI_RPC_USER=lariuser \
  -e LARI_RPC_PASSWORD=laripassword \
  -e LARI_RPC_HOST=localhost \
  -e LARI_RPC_PORT=19332 \
  bsv-node-api
```

## APIエンドポイント

### 1. 公開鍵と秘密鍵のペア作成

**リクエスト:**
```bash
# デフォルトネットワーク（JpyNetwork）
curl -X POST http://localhost:5002/api/keypair

# ネットワーク指定
curl -X POST "http://localhost:5002/api/keypair?network=jpy"
curl -X POST "http://localhost:5002/api/keypair?network=lari"
```

**レスポンス:**
```json
{
  "address": "mxyz123...",
  "privateKey": "cxyz123...",
  "network": "jpy"
}
```

### 2. 残高確認

**リクエスト:**
```bash
# デフォルトネットワーク（JpyNetwork）
curl -X GET http://localhost:5002/api/balance/<アドレス>

# ネットワーク指定
curl -X GET "http://localhost:5002/api/balance/<アドレス>?network=jpy"
curl -X GET "http://localhost:5002/api/balance/<アドレス>?network=lari"
```

**レスポンス:**
```json
{
  "address": "mxyz123...",
  "balance": 10.5,
  "unspentOutputs": [...],
  "network": "jpy"
}
```

### 3. 送金

**リクエスト:**
```bash
curl -X POST http://localhost:5002/api/send \
  -H "Content-Type: application/json" \
  -d '{
    "fromAddress": "<送信元アドレス>",
    "privateKey": "<秘密鍵>",
    "toAddress": "<送信先アドレス>",
    "amount": <金額>,
    "network": "jpy"
  }'
```

**レスポンス:**
```json
{
  "transactionId": "txyz123...",
  "fromAddress": "mxyz123...",
  "toAddress": "mabc123...",
  "amount": 1.5,
  "network": "jpy"
}
```

### 4. ノード情報

**リクエスト:**
```bash
# デフォルトネットワーク（JpyNetwork）
curl -X GET http://localhost:5002/api/node/info

# ネットワーク指定
curl -X GET "http://localhost:5002/api/node/info?network=jpy"
curl -X GET "http://localhost:5002/api/node/info?network=lari"
```

**レスポンス:**
```json
{
  "version": 101000800,
  "subversion": "/Bitcoin SV:1.0.8/",
  "connections": 2,
  "chain": "regtest",
  "blocks": 265,
  "difficulty": 4.656542373906925e-10,
  "network": "jpy"
}
```

### 5. ヘルスチェック

**リクエスト:**
```bash
curl -X GET http://localhost:5002/healthz
```

**レスポンス:**
```json
{
  "status": "ok"
}
```

## ネットワーク設定

APIは以下の2つのネットワークをサポートしています：

1. **JpyNetwork**
   - ネットワークパラメータ: `jpy`
   - P2Pポート: 18444
   - RPCポート: 18332

2. **LariNetwork**
   - ネットワークパラメータ: `lari`
   - P2Pポート: 19444
   - RPCポート: 19332

ネットワークパラメータを指定しない場合は、デフォルトでJpyNetworkが使用されます。
