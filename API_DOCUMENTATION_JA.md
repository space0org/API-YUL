# BSVノードAPI ドキュメント

このAPIは、Bitcoin SVノードと対話するためのエンドポイントを提供します。

## 公開URL

APIは以下のURLで公開されています：
https://app-fhxknmbw.fly.dev/

## エンドポイント

### 1. 公開鍵と秘密鍵のペア作成 (POST /api/keypair)

新しい公開鍵（アドレス）と秘密鍵のペアを生成します。

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

### 2. 残高確認 (GET /api/balance/{address})

特定のアドレスの残高を取得します。

**リクエスト:**
```bash
curl -X GET https://app-fhxknmbw.fly.dev/api/balance/mxyz123...
```

**レスポンス:**
```json
{
  "address": "mxyz123...",
  "balance": 10.5,
  "unspentOutputs": [...]
}
```

### 3. 送金 (POST /api/send)

あるアドレスから別のアドレスにBSVを送金します。

**リクエスト:**
```bash
curl -X POST https://app-fhxknmbw.fly.dev/api/send \
  -H "Content-Type: application/json" \
  -d '{
    "fromAddress": "mxyz123...",
    "privateKey": "cxyz123...",
    "toAddress": "mabc123...",
    "amount": 1.5
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

### 4. ノード情報 (GET /api/node/info)

BSVノードに関する情報を取得します。

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

### 5. ヘルスチェック (GET /healthz)

APIの健全性を確認します。

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

## コマンドリスト

以下は、APIを使用するためのcurlコマンドのリストです：

### 1. 公開鍵と秘密鍵のペア作成
```bash
curl -X POST https://app-fhxknmbw.fly.dev/api/keypair
```

### 2. 残高確認
```bash
curl -X GET https://app-fhxknmbw.fly.dev/api/balance/<アドレス>
```

### 3. 送金
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

### 4. ノード情報取得
```bash
curl -X GET https://app-fhxknmbw.fly.dev/api/node/info
```

### 5. ヘルスチェック
```bash
curl -X GET https://app-fhxknmbw.fly.dev/healthz
```
