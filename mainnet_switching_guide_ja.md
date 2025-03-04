# Multi-Bsv-Networkのネットワークモード切り替えガイド

## Multi-Bsv-Networkについて

Multi-Bsv-Networkは、JpyNetworkとLariNetworkの2つのチェーンを持つカスタムBitcoin SVネットワークです。このネットワークは以下の3つのモードで動作することができます：

1. **Regtestモード（リグレッションテストモード）**
   - 開発・テスト用のプライベートネットワーク
   - マイニング報酬は6.25 BSVに設定されています（テスト結果より）
   - ブロック生成が簡単で、即時に取引が確認される
   - JpyNetwork: ポート18332
   - LariNetwork: ポート19332

2. **Testnetモード（テストネットワーク）**
   - テスト用の公開ネットワーク
   - JpyNetwork: ポート18333
   - LariNetwork: ポート19333

3. **Mainnetモード（メインネットワーク）**
   - Multi-Bsv-Networkのメインネットワーク
   - JpyNetwork: ポート18444
   - LariNetwork: ポート19444
   - 注意: これは実際のBitcoin SVネットワークではなく、Multi-Bsv-Network独自のメインネットワークです

## API経由でのモード切り替えの制限

現在のAPI実装では、`/api/network/mode`エンドポイントを使用してネットワークモードの切り替えをリクエストすることができますが、**完全な切り替えには以下の制限があります**：

1. Bitcoin SVノードの設定ファイル（bitcoin.conf）の変更が必要
2. ノードの再起動が必要
3. ブロックチェーンデータの再同期が必要な場合がある

これらの操作はAPI経由では完全に自動化できないため、実際のモード切り替えには手動での設定変更が必要です。

## Mainnetモードへの切り替え方法

### 1. API経由でのリクエスト（部分的な切り替え）

```bash
curl -X POST "http://localhost:5002/api/network/mode" \
  -H "Content-Type: application/json" \
  -d '{"mode":"mainnet","network":"jpy"}'
```

このリクエストは内部的にMainnetモードへの接続を試みますが、完全なモード切り替えは行われません。

### 2. 手動での完全な切り替え（推奨）

#### 2.1. Bitcoin SVノードの設定ファイルを編集

JpyNetworkの場合：
```bash
# bitcoin.confファイルを編集
nano /path/to/jpynetwork/bitcoin.conf

# 以下の行を削除または無効化
regtest=1
testnet=0

# 以下の行を追加（必要に応じて）
regtest=0
testnet=0
```

LariNetworkの場合も同様に設定を変更します。

#### 2.2. ノードを再起動

```bash
# Dockerを使用している場合
docker restart jpynetwork-node
docker restart larinetwork-node
```

#### 2.3. ブロックチェーンの同期

Mainnetモードに切り替えた後、ブロックチェーンの同期が必要です。これには時間がかかる場合があります。

## 注意事項

1. **ネットワーク要件**: Mainnetモードでは大量のデータ転送が発生する場合があるため、高速で安定したネットワーク接続が必要です。

2. **ストレージ要件**: Mainnetの完全なブロックチェーンデータは大量のストレージを必要とする場合があります。

3. **セキュリティ**: Mainnetモードでは、適切なセキュリティ対策を講じることが重要です。

## 推奨事項

開発・テスト目的では、Regtestモードの使用を推奨します。Regtestモードでは：

- ブロック生成が簡単で即時に取引が確認される
- ネットワーク接続やストレージの要件が低い

テストが完了し、本番環境への移行準備ができた場合にのみ、Mainnetモードへの切り替えを検討してください。

## Multi-Bsv-Networkの特徴

Multi-Bsv-Networkは、実際のBitcoin SVネットワークとは別の独自のネットワークで、以下の特徴があります：

1. **2つのチェーン**: JpyNetworkとLariNetworkの2つの独立したチェーンを持ちます。

2. **カスタム設定**: 各チェーンは独自のポート設定を持ち、異なるネットワークモードで動作することができます。

3. **トークンブリッジ**: JpyNetworkとLariNetwork間でトークンを交換するためのブリッジ機能があります。

4. **APIサポート**: 各チェーンに対して、ウォレット作成、残高確認、送金、マイニングなどの操作をAPIを通じて行うことができます。

## APIの使用例

### 現在のネットワークモードを確認

```bash
# JpyNetworkの現在のモードを確認
curl "http://localhost:5002/api/network/mode?network=jpy"

# LariNetworkの現在のモードを確認
curl "http://localhost:5002/api/network/mode?network=lari"
```

### ネットワークモードを切り替え

```bash
# JpyNetworkをMainnetモードに切り替え
curl -X POST "http://localhost:5002/api/network/mode" \
  -H "Content-Type: application/json" \
  -d '{"mode":"mainnet","network":"jpy"}'

# LariNetworkをMainnetモードに切り替え
curl -X POST "http://localhost:5002/api/network/mode" \
  -H "Content-Type: application/json" \
  -d '{"mode":"mainnet","network":"lari"}'
```

### ノード情報を取得

```bash
# JpyNetworkのノード情報を取得
curl "http://localhost:5002/api/node/info?network=jpy"

# LariNetworkのノード情報を取得
curl "http://localhost:5002/api/node/info?network=lari"
```
