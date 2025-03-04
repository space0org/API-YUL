# Bitcoin SVのマイニング報酬について

## マイニング報酬の仕組み

Bitcoin SVのマイニング報酬は、ネットワークモードによって異なります：

1. **Regtestモード（リグレッションテストモード）**
   - 通常、マイニング報酬は**50 BSV**に固定されています
   - 半減期の影響を受けません
   - 開発・テスト用のプライベートネットワークで使用されます

2. **Testnetモード（テストネットワーク）**
   - マイニング報酬はメインネットと同様に半減期があります
   - 現在の報酬は**6.25 BSV**です（4回の半減期後）
   - テスト用の公開ネットワークで使用されます

3. **Mainnetモード（メインネットワーク）**
   - マイニング報酬はブロック高に応じて半減します
   - 現在の報酬は**6.25 BSV**です（4回の半減期後）
   - 本番環境の公開ネットワークで使用されます

## Multi-Bsv-Networkでのマイニング報酬

Multi-Bsv-Networkでは、JpyNetworkとLariNetworkの2つのチェーンがあります：

1. **JpyNetwork**
   - 現在のテスト結果では、マイニング報酬は**6.25 BSV**です
   - これは、Regtestモードの標準的な報酬（50 BSV）ではなく、現在のメインネット報酬と同じです

2. **LariNetwork**
   - 現在のテスト結果では、マイニング報酬は**6.25 BSV**です
   - これは、Regtestモードの標準的な報酬（50 BSV）ではなく、現在のメインネット報酬と同じです

## 報酬が50 BSVではなく6.25 BSVである理由

通常、Bitcoin SVのRegtestモードでは、マイニング報酬は50 BSVに固定されています。しかし、現在のMulti-Bsv-Networkの実装では、以下の理由により報酬が6.25 BSVになっていると考えられます：

1. **カスタム設定**: Bitcoin SVノードの設定で、Regtestモードでも現在のメインネット報酬（6.25 BSV）を使用するように設定されている可能性があります。

2. **最新のBitcoin SVバージョン**: 使用しているBitcoin SVのバージョンによっては、Regtestモードでもメインネットの報酬ルールを適用する場合があります。

3. **半減期シミュレーション**: 開発・テスト目的で、Regtestモードでも半減期をシミュレートするように設定されている可能性があります。

## 101ブロックのマイニング後の合計報酬

現在の設定では、101ブロックをマイニングした場合の合計報酬は以下のようになります：

- 報酬 = 101 × 6.25 BSV = 631.25 BSV

これは、標準的なRegtestモードの場合（101 × 50 BSV = 5,050 BSV）とは異なります。

## マイニング報酬の生成方法

APIを使用して、指定したアドレスにマイニング報酬を生成することができます：

```bash
curl -X POST "http://localhost:5002/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"address":"YOUR_ADDRESS","numBlocks":1,"network":"jpy"}'
```

または、LariNetworkの場合：

```bash
curl -X POST "http://localhost:5002/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"address":"YOUR_ADDRESS","numBlocks":1,"network":"lari"}'
```

## 注意事項

1. **ブロック成熟度**: マイニング報酬は100ブロックの成熟期間後に使用可能になります。テスト環境では、この制限を回避するために追加のブロックを生成することができます：

```bash
curl -X POST "http://localhost:5002/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"address":"YOUR_ADDRESS","numBlocks":101,"network":"jpy"}'
```

2. **セーフモード**: ノードがセーフモードの場合、残高の取得やトランザクションの送信ができない場合があります。セーフモードを解除するには、十分な数のブロックを生成する必要があります。

## カスタムMainnetモードについて

Multi-Bsv-Networkのカスタムメインネットモードは、実際のBitcoin SVネットワークとは別の独自のネットワークです。このモードでは：

1. JpyNetworkとLariNetworkの2つのチェーンが独立して動作します
2. それぞれのチェーンは独自のポート設定を持ちます：
   - JpyNetwork: ポート18444
   - LariNetwork: ポート19444
3. マイニング報酬は現在のメインネットと同じ6.25 BSVですが、これはカスタム設定によるものです

## まとめ

Multi-Bsv-Networkは、JpyNetworkとLariNetworkの2つのチェーンを持つカスタムBitcoin SVネットワークです。現在の実装では、Regtestモードでもマイニング報酬が6.25 BSVに設定されていますが、これは標準的なRegtestモードの報酬（50 BSV）とは異なります。この設定は、開発・テスト目的でカスタマイズされたものと考えられます。
