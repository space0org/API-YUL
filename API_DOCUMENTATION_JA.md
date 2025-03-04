# API-YUL API ドキュメント

このドキュメントでは、API-YUL の API エンドポイントについて説明します。

## 基本情報

- ベース URL: `http://localhost:5002`
- コンテンツタイプ: `application/json`

## エンドポイント

### ヘルスチェック

```
GET /healthz
```

サーバーの状態を確認します。

**レスポンス例**:

```json
{
  "status": "ok"
}
```

### キーペアの作成

```
POST /api/keypair
```

新しい公開鍵と秘密鍵のペアを作成します。

**クエリパラメータ**:

- `network` (オプション): 使用するネットワーク（`jpy` または `lari`）。デフォルトは `jpy`。

**レスポンス例**:

```json
{
  "address": "mzzys5TuqrGLdL1WU3P5TN1QqvQY5VmDwX",
  "privateKey": "cNQKccYYQyGX9G9Qxq2DJev9jHygbZpb2UG7EvUapbtDx5XhkhYE",
  "network": "jpy"
}
```

### 残高確認

```
GET /api/balance/{address}
```

指定したアドレスの残高を確認します。

**クエリパラメータ**:

- `network` (オプション): 使用するネットワーク（`jpy` または `lari`）。デフォルトは `jpy`。

**レスポンス例**:

```json
{
  "address": "mzzys5TuqrGLdL1WU3P5TN1QqvQY5VmDwX",
  "balance": 100.0,
  "unspentOutputs": [
    {
      "txid": "7b5685ee3abc4df9a5d295c4fdb3b9b7f1c789a4f2f8df13c9b90b5d7b9c6e5d",
      "vout": 0,
      "address": "mzzys5TuqrGLdL1WU3P5TN1QqvQY5VmDwX",
      "account": "",
      "scriptPubKey": "76a914d8c43e6f68ca4ea1e9b93da2d1e6a0ceb5af8a8c88ac",
      "amount": 100.0,
      "confirmations": 1,
      "spendable": true,
      "solvable": true
    }
  ],
  "network": "jpy"
}
```

### 送金

```
POST /api/send
```

一つのアドレスから別のアドレスに送金します。

**リクエストボディ**:

```json
{
  "fromAddress": "mzzys5TuqrGLdL1WU3P5TN1QqvQY5VmDwX",
  "privateKey": "cNQKccYYQyGX9G9Qxq2DJev9jHygbZpb2UG7EvUapbtDx5XhkhYE",
  "toAddress": "n1ZCjTcPxX2zVyFH5BjmbHrQCJp3DxRKdU",
  "amount": 10.0,
  "network": "jpy"
}
```

**レスポンス例**:

```json
{
  "transactionId": "7b5685ee3abc4df9a5d295c4fdb3b9b7f1c789a4f2f8df13c9b90b5d7b9c6e5d",
  "fromAddress": "mzzys5TuqrGLdL1WU3P5TN1QqvQY5VmDwX",
  "toAddress": "n1ZCjTcPxX2zVyFH5BjmbHrQCJp3DxRKdU",
  "amount": 10.0,
  "network": "jpy"
}
```

### ノード情報

```
GET /api/node/info
```

ビットコインノードの情報を取得します。

**クエリパラメータ**:

- `network` (オプション): 使用するネットワーク（`jpy` または `lari`）。デフォルトは `jpy`。

**レスポンス例**:

```json
{
  "version": 100000,
  "protocolversion": 70015,
  "connections": 8,
  "chain": "regtest",
  "blocks": 100,
  "difficulty": 4.656542373906925e-10,
  "network": "jpy"
}
```

## トークンブリッジ API

トークンブリッジは別のサービスで、ポート 5001 で実行されています。

### ブリッジ情報

```
GET /bridge/info
```

トークンブリッジの情報を取得します。

**レスポンス例**:

```json
{
  "exchange_rate": "1 Lari = 55 Jpy",
  "networks": {
    "jpy_network": {
      "host": "jpynetwork-node",
      "name": "JpyNetwork",
      "port": 18332
    },
    "lari_network": {
      "host": "larinetwork-node",
      "name": "LariNetwork",
      "port": 18332
    }
  },
  "status": "operational"
}
```

### JPY から LARI への交換

```
POST /bridge/swap/jpy-to-lari
```

JPY トークンを LARI トークンに交換します。

**リクエストボディ**:

```json
{
  "fromAddress": "mzzys5TuqrGLdL1WU3P5TN1QqvQY5VmDwX",
  "privateKey": "cNQKccYYQyGX9G9Qxq2DJev9jHygbZpb2UG7EvUapbtDx5XhkhYE",
  "toAddress": "n1ZCjTcPxX2zVyFH5BjmbHrQCJp3DxRKdU",
  "amount": 55.0
}
```

**レスポンス例**:

```json
{
  "source_transaction": "7b5685ee3abc4df9a5d295c4fdb3b9b7f1c789a4f2f8df13c9b90b5d7b9c6e5d",
  "destination_transaction": "6a4574dd2bbc3ce8a4c295c4fdb3b9b7f1c789a4f2f8df13c9b90b5d7b9c6e5d",
  "source_amount": 55.0,
  "destination_amount": 1.0,
  "source_network": "jpy",
  "destination_network": "lari",
  "status": "completed"
}
```

### LARI から JPY への交換

```
POST /bridge/swap/lari-to-jpy
```

LARI トークンを JPY トークンに交換します。

**リクエストボディ**:

```json
{
  "fromAddress": "n1ZCjTcPxX2zVyFH5BjmbHrQCJp3DxRKdU",
  "privateKey": "cRQKccYYQyGX9G9Qxq2DJev9jHygbZpb2UG7EvUapbtDx5XhkhYF",
  "toAddress": "mzzys5TuqrGLdL1WU3P5TN1QqvQY5VmDwX",
  "amount": 1.0
}
```

**レスポンス例**:

```json
{
  "source_transaction": "6a4574dd2bbc3ce8a4c295c4fdb3b9b7f1c789a4f2f8df13c9b90b5d7b9c6e5d",
  "destination_transaction": "7b5685ee3abc4df9a5d295c4fdb3b9b7f1c789a4f2f8df13c9b90b5d7b9c6e5d",
  "source_amount": 1.0,
  "destination_amount": 55.0,
  "source_network": "lari",
  "destination_network": "jpy",
  "status": "completed"
}
```
