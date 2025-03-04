# MacBook Pro での Multi-Bsv-Network セットアップガイド

このガイドでは、MacBook Pro に Multi-Bsv-Network と API-YUL をセットアップする手順を説明します。

## 前提条件

- MacBook Pro（macOS 10.15以上）
- [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop) がインストールされていること
- [Git](https://git-scm.com/download/mac) がインストールされていること
- [Python 3.9以上](https://www.python.org/downloads/macos/) がインストールされていること

## 1. Multi-Bsv-Network のセットアップ

### リポジトリのクローン

```bash
git clone https://github.com/space0org/Multi-Bsv-Network.git
cd Multi-Bsv-Network
```

### ネットワークの起動

```bash
cd one-click-setup
chmod +x setup.sh
./setup.sh
chmod +x start.sh
./start.sh
```

これにより、JpyNetwork と LariNetwork の両方のノードが起動し、トークンブリッジも設定されます。

### ネットワークの確認

```bash
docker ps
```

以下のコンテナが実行されていることを確認してください：
- jpynetwork-node
- larinetwork-node
- token-bridge

## 2. API-YUL のセットアップ

### リポジトリのクローン

```bash
cd ~/
git clone https://github.com/space0org/API-YUL.git
cd API-YUL
```

### Poetry のインストール

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 依存関係のインストール

```bash
poetry install
```

### API の起動

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 5002 --reload
```

## 3. API の使用方法

### ウォレットの作成

```bash
# JPYネットワーク用のウォレット作成
curl -X POST "http://localhost:5002/api/keypair?network=jpy"

# LARIネットワーク用のウォレット作成
curl -X POST "http://localhost:5002/api/keypair?network=lari"
```

### 残高確認

```bash
# JPYネットワークでの残高確認
curl "http://localhost:5002/api/balance/{アドレス}?network=jpy"

# LARIネットワークでの残高確認
curl "http://localhost:5002/api/balance/{アドレス}?network=lari"
```

### 送金

```bash
curl -X POST "http://localhost:5002/api/send" \
  -H "Content-Type: application/json" \
  -d '{
    "fromAddress": "送金元アドレス",
    "privateKey": "送金元の秘密鍵",
    "toAddress": "送金先アドレス",
    "amount": 1.0,
    "network": "jpy"
  }'
```

### ノード情報の取得

```bash
# JPYネットワークのノード情報
curl "http://localhost:5002/api/node/info?network=jpy"

# LARIネットワークのノード情報
curl "http://localhost:5002/api/node/info?network=lari"
```

### トークンブリッジ情報の取得

```bash
curl "http://localhost:5001/bridge/info"
```

### クロスチェーン交換

```bash
# JPYからLARIへの交換
curl -X POST "http://localhost:5001/bridge/swap/jpy-to-lari" \
  -H "Content-Type: application/json" \
  -d '{
    "fromAddress": "JPYネットワークの送金元アドレス",
    "privateKey": "JPYネットワークの送金元の秘密鍵",
    "toAddress": "LARIネットワークの送金先アドレス",
    "amount": 55.0
  }'

# LARIからJPYへの交換
curl -X POST "http://localhost:5001/bridge/swap/lari-to-jpy" \
  -H "Content-Type: application/json" \
  -d '{
    "fromAddress": "LARIネットワークの送金元アドレス",
    "privateKey": "LARIネットワークの送金元の秘密鍵",
    "toAddress": "JPYネットワークの送金先アドレス",
    "amount": 1.0
  }'
```

## 4. トラブルシューティング

### コンテナが起動しない場合

```bash
docker logs jpynetwork-node
docker logs larinetwork-node
docker logs token-bridge
```

### API が応答しない場合

```bash
# API-YULのログを確認
docker logs api-yul

# トークンブリッジのログを確認
docker logs token-bridge
```

### ネットワーク接続の問題

```bash
# ネットワーク設定の確認
docker network ls
docker network inspect multi-bsv-network_default
```

## 5. システムの停止

```bash
# Multi-Bsv-Networkの停止
cd ~/Multi-Bsv-Network/one-click-setup
./stop.sh

# API-YULの停止
# Ctrl+Cでuvicornプロセスを停止
```
