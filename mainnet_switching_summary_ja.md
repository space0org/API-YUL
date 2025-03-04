# Multi-Bsv-Networkモード切り替え概要

## ネットワークモード

Multi-Bsv-Networkは3つのモードで動作します：

1. **Regtestモード**
   - 開発・テスト用
   - JpyNetwork: ポート18332
   - LariNetwork: ポート19332

2. **Testnetモード**
   - テスト用公開ネットワーク
   - JpyNetwork: ポート18333
   - LariNetwork: ポート19333

3. **Mainnetモード**
   - カスタムメインネットワーク（実際のBSVネットワークではない）
   - JpyNetwork: ポート18444
   - LariNetwork: ポート19444

## モード切り替え手順

### API経由（部分的な切り替え）

```bash
curl -X POST "http://localhost:5002/api/network/mode" \
  -H "Content-Type: application/json" \
  -d '{"mode":"mainnet","network":"jpy"}'
```

### 手動（完全な切り替え）

1. bitcoin.confファイルを編集
2. ノードを再起動
3. ブロックチェーンを同期

## 注意事項

- Mainnetモードは実際のBSVネットワークではなく、Multi-Bsv-Network独自のネットワークです
- 完全な切り替えには手動での設定変更が必要です
- 開発・テスト目的ではRegtestモードの使用を推奨します
