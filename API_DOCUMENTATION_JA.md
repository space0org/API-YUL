# API-YUL ドキュメント

## 概要

API-YULは、Bitcoin SVノードと対話するためのAPIです。JpyNetworkとLariNetworkの両方をサポートしています。

## APIエンドポイント

### 1. 公開鍵と秘密鍵のペア作成

**エンドポイント:** `/api/keypair`

**メソッド:** POST

**パラメータ:**
- `network` (オプション): 使用するネットワーク（`jpy`または`lari`）。デフォルトは`jpy`。

**リクエスト例:**
```bash
# デフォルトネットワーク（JpyNetwork）
curl -X POST http://localhost:5002/api/keypair

# ネットワーク指定
curl -X POST "http://localhost:5002/api/keypair?network=jpy"
curl -X POST "http://localhost:5002/api/keypair?network=lari"
```

**レスポンス例:**
```json
{
  "address": "mxyz123...",
  "privateKey": "cxyz123...",
  "network": "jpy"
}
```

### 2. 残高確認

**エンドポイント:** `/api/balance/{address}`

**メソッド:** GET

**パラメータ:**
- `address`: 残高を確認するBitcoinアドレス
- `network` (オプション): 使用するネットワーク（`jpy`または`lari`）。デフォルトは`jpy`。

**リクエスト例:**
```bash
# デフォルトネットワーク（JpyNetwork）
curl -X GET http://localhost:5002/api/balance/mxyz123...

# ネットワーク指定
curl -X GET "http://localhost:5002/api/balance/mxyz123...?network=jpy"
curl -X GET "http://localhost:5002/api/balance/mxyz123...?network=lari"
```

**レスポンス例:**
```json
{
  "address": "mxyz123...",
  "balance": 10.5,
  "unspentOutputs": [...],
  "network": "jpy"
}
```

### 3. 送金

**エンドポイント:** `/api/send`

**メソッド:** POST

**リクエストボディ:**
```json
{
  "fromAddress": "送信元アドレス",
  "privateKey": "秘密鍵",
  "toAddress": "送信先アドレス",
  "amount": 金額,
  "network": "jpy"  // オプション、デフォルトは"jpy"
}
```

**リクエスト例:**
```bash
curl -X POST http://localhost:5002/api/send \
  -H "Content-Type: application/json" \
  -d '{
    "fromAddress": "mxyz123...",
    "privateKey": "cxyz123...",
    "toAddress": "mabc123...",
    "amount": 1.5,
    "network": "jpy"
  }'
```

**レスポンス例:**
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

**エンドポイント:** `/api/node/info`

**メソッド:** GET

**パラメータ:**
- `network` (オプション): 使用するネットワーク（`jpy`または`lari`）。デフォルトは`jpy`。

**リクエスト例:**
```bash
# デフォルトネットワーク（JpyNetwork）
curl -X GET http://localhost:5002/api/node/info

# ネットワーク指定
curl -X GET "http://localhost:5002/api/node/info?network=jpy"
curl -X GET "http://localhost:5002/api/node/info?network=lari"
```

**レスポンス例:**
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

**エンドポイント:** `/healthz`

**メソッド:** GET

**リクエスト例:**
```bash
curl -X GET http://localhost:5002/healthz
```

**レスポンス例:**
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

## 環境変数

APIは以下の環境変数を使用してネットワーク設定を行います：

### JpyNetwork設定
- `JPY_RPC_USER`: JpyNetworkのRPCユーザー名
- `JPY_RPC_PASSWORD`: JpyNetworkのRPCパスワード
- `JPY_RPC_HOST`: JpyNetworkのホスト名またはIPアドレス
- `JPY_RPC_PORT`: JpyNetworkのRPCポート

### LariNetwork設定
- `LARI_RPC_USER`: LariNetworkのRPCユーザー名
- `LARI_RPC_PASSWORD`: LariNetworkのRPCパスワード
- `LARI_RPC_HOST`: LariNetworkのホスト名またはIPアドレス
- `LARI_RPC_PORT`: LariNetworkのRPCポート

環境変数が設定されていない場合は、デフォルト値が使用されます。
