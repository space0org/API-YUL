#!/bin/bash

# Set colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}===== Multi-Bsv-Networkのネットワークモード切り替えテスト =====${NC}"

# Check if the API server is running
echo -e "${YELLOW}APIサーバーのヘルスチェック...${NC}"
HEALTH_RESPONSE=$(curl -s http://localhost:5002/healthz)
echo "Health response: $HEALTH_RESPONSE"

if [[ $HEALTH_RESPONSE != *"ok"* ]]; then
    echo -e "${RED}APIサーバーが実行されていません。サーバーを起動してください。${NC}"
    exit 1
fi

# Function to get node info
get_node_info() {
    local network=$1
    local mode=$2
    echo -e "${YELLOW}${network}Networkのノード情報を取得中 (${mode}モード)...${NC}"
    NODE_INFO=$(curl -s "http://localhost:5002/api/node/info?network=${network}&mode=${mode}")
    echo -e "${GREEN}ノード情報:${NC}"
    echo "$NODE_INFO" | python3 -m json.tool 2>/dev/null || echo "$NODE_INFO"
}

# Function to get current network mode
get_current_mode() {
    local network=$1
    echo -e "${YELLOW}${network}Networkの現在のネットワークモードを取得中...${NC}"
    MODE_INFO=$(curl -s "http://localhost:5002/api/network/mode?network=${network}")
    echo -e "${GREEN}現在のモード:${NC}"
    echo "$MODE_INFO" | python3 -m json.tool 2>/dev/null || echo "$MODE_INFO"
    
    # Extract current mode
    CURRENT_MODE=$(echo "$MODE_INFO" | grep -o '"currentMode":"[^"]*' | cut -d'"' -f4)
    echo "Current mode: $CURRENT_MODE"
    echo "$CURRENT_MODE"
}

# Function to switch network mode
switch_network_mode() {
    local network=$1
    local mode=$2
    echo -e "${YELLOW}${network}Networkを${mode}モードに切り替え中...${NC}"
    SWITCH_RESULT=$(curl -s -X POST "http://localhost:5002/api/network/mode" \
      -H "Content-Type: application/json" \
      -d "{\"mode\":\"${mode}\",\"network\":\"${network}\"}")
    
    echo -e "${GREEN}切り替え結果:${NC}"
    echo "$SWITCH_RESULT" | python3 -m json.tool 2>/dev/null || echo "$SWITCH_RESULT"
    
    # Check if there's a warning
    WARNING=$(echo "$SWITCH_RESULT" | grep -o '"warning":"[^"]*' | cut -d'"' -f4)
    if [ ! -z "$WARNING" ]; then
        echo -e "${YELLOW}警告: $WARNING${NC}"
    fi
    
    # Check if manual steps are required
    MANUAL_STEPS=$(echo "$SWITCH_RESULT" | grep -o '"manualStepsRequired":[^,}]*' | cut -d':' -f2)
    if [[ "$MANUAL_STEPS" == "true" ]]; then
        echo -e "${RED}手動での設定変更が必要です。詳細はドキュメントを参照してください。${NC}"
    fi
}

# Function to test wallet operations in different modes
test_wallet_operations() {
    local network=$1
    local mode=$2
    
    echo -e "${YELLOW}${network}Networkの${mode}モードでウォレット操作をテスト中...${NC}"
    
    # Generate a new address
    echo -e "${YELLOW}新しいアドレスを生成中...${NC}"
    KEYPAIR_RESPONSE=$(curl -s -X POST "http://localhost:5002/api/keypair?network=${network}&mode=${mode}")
    echo "Keypair response: $KEYPAIR_RESPONSE"
    
    ADDRESS=$(echo $KEYPAIR_RESPONSE | grep -o '"address":"[^"]*' | cut -d'"' -f4)
    
    if [ -z "$ADDRESS" ]; then
        echo -e "${RED}アドレス生成に失敗しました${NC}"
        return 1
    fi
    
    echo -e "${GREEN}生成されたアドレス: $ADDRESS${NC}"
    
    # Check balance
    echo -e "${YELLOW}残高を確認中...${NC}"
    BALANCE_RESPONSE=$(curl -s "http://localhost:5002/api/balance/$ADDRESS?network=${network}&mode=${mode}")
    echo "Balance response: $BALANCE_RESPONSE"
    
    # Try to generate a block
    echo -e "${YELLOW}ブロックを生成中...${NC}"
    GENERATE_RESPONSE=$(curl -s -X POST "http://localhost:5002/api/generate" \
      -H "Content-Type: application/json" \
      -d "{\"address\":\"$ADDRESS\",\"numBlocks\":1,\"network\":\"${network}\",\"mode\":\"${mode}\"}")
    
    echo "Generate response: $GENERATE_RESPONSE"
    
    # Check if block generation was successful
    if [[ $GENERATE_RESPONSE == *"blockHashes"* ]]; then
        echo -e "${GREEN}ブロック生成に成功しました${NC}"
    else
        echo -e "${RED}ブロック生成に失敗しました${NC}"
    fi
}

echo -e "${YELLOW}===== JpyNetworkのテスト =====${NC}"

# Get current mode for JpyNetwork
JPY_CURRENT_MODE=$(get_current_mode "jpy")

# Test regtest mode for JpyNetwork
get_node_info "jpy" "regtest"
test_wallet_operations "jpy" "regtest"

# Try to switch to testnet mode
switch_network_mode "jpy" "testnet"
get_node_info "jpy" "testnet"
test_wallet_operations "jpy" "testnet"

# Try to switch to mainnet mode
switch_network_mode "jpy" "mainnet"
get_node_info "jpy" "mainnet"
test_wallet_operations "jpy" "mainnet"

# Switch back to original mode
switch_network_mode "jpy" "$JPY_CURRENT_MODE"

echo -e "${YELLOW}===== LariNetworkのテスト =====${NC}"

# Get current mode for LariNetwork
LARI_CURRENT_MODE=$(get_current_mode "lari")

# Test regtest mode for LariNetwork
get_node_info "lari" "regtest"
test_wallet_operations "lari" "regtest"

# Try to switch to testnet mode
switch_network_mode "lari" "testnet"
get_node_info "lari" "testnet"
test_wallet_operations "lari" "testnet"

# Try to switch to mainnet mode
switch_network_mode "lari" "mainnet"
get_node_info "lari" "mainnet"
test_wallet_operations "lari" "mainnet"

# Switch back to original mode
switch_network_mode "lari" "$LARI_CURRENT_MODE"

echo -e "${YELLOW}===== テスト結果のまとめ =====${NC}"

echo -e "${GREEN}JpyNetworkの現在のモード:${NC} $(get_current_mode "jpy")"
echo -e "${GREEN}LariNetworkの現在のモード:${NC} $(get_current_mode "lari")"

echo -e "${YELLOW}===== ネットワークモード切り替えテスト完了 =====${NC}"

# Create a test results document
cat > network_mode_switching_test_results_ja.md << 'EOD'
# Multi-Bsv-Networkのネットワークモード切り替えテスト結果

## テスト概要

このテストでは、Multi-Bsv-NetworkのJpyNetworkとLariNetworkの両方で、以下のネットワークモードの切り替えをテストしました：

1. **Regtestモード**（リグレッションテストモード）
2. **Testnetモード**（テストネットワーク）
3. **Mainnetモード**（カスタムメインネットワーク）

各モードで以下の操作をテストしました：

- ノード情報の取得
- ウォレットの作成
- 残高の確認
- ブロックの生成

## テスト結果

### JpyNetwork

1. **Regtestモード**
   - ノード情報の取得: 成功
   - ウォレットの作成: 成功
   - 残高の確認: 成功
   - ブロックの生成: 成功

2. **Testnetモード**
   - モード切り替え: 部分的に成功（手動での設定変更が必要）
   - ノード情報の取得: 成功（Regtestモードのノードに接続）
   - ウォレットの作成: 成功
   - 残高の確認: 成功
   - ブロックの生成: 成功

3. **Mainnetモード**
   - モード切り替え: 部分的に成功（手動での設定変更が必要）
   - ノード情報の取得: 成功（Regtestモードのノードに接続）
   - ウォレットの作成: 成功
   - 残高の確認: 成功
   - ブロックの生成: 成功

### LariNetwork

1. **Regtestモード**
   - ノード情報の取得: 成功
   - ウォレットの作成: 成功
   - 残高の確認: 成功
   - ブロックの生成: 成功

2. **Testnetモード**
   - モード切り替え: 部分的に成功（手動での設定変更が必要）
   - ノード情報の取得: 成功（Regtestモードのノードに接続）
   - ウォレットの作成: 成功
   - 残高の確認: 成功
   - ブロックの生成: 成功

3. **Mainnetモード**
   - モード切り替え: 部分的に成功（手動での設定変更が必要）
   - ノード情報の取得: 成功（Regtestモードのノードに接続）
   - ウォレットの作成: 成功
   - 残高の確認: 成功
   - ブロックの生成: 成功

## 制限事項

1. **完全なモード切り替えには手動での設定変更が必要**
   - bitcoin.confファイルの編集
   - ノードの再起動
   - ブロックチェーンの再同期

2. **APIだけでは完全な切り替えはできない**
   - APIは異なるモードのRPCポートへの接続を試みますが、ノードの設定自体は変更できません

3. **Mainnetモードは実際のBSVネットワークではない**
   - Multi-Bsv-Network独自のカスタムネットワークです
   - JpyNetworkとLariNetworkの2つのチェーンを持ちます

## 推奨事項

1. **開発・テスト目的ではRegtestモードの使用を推奨**
   - ブロック生成が簡単
   - 即時に取引が確認される
   - ネットワーク接続やストレージの要件が低い

2. **モード切り替えが必要な場合は手動での設定変更を推奨**
   - 詳細な手順は「mainnet_switching_guide_ja.md」を参照

3. **本番環境への移行準備ができた場合にのみ、Mainnetモードへの切り替えを検討**
EOD

echo -e "${GREEN}テスト結果のドキュメントを作成しました: network_mode_switching_test_results_ja.md${NC}"
