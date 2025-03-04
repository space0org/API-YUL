#!/bin/bash

echo "===== Balance Check Fix Test ====="

# Test the balance check for JpyNetwork
echo "JpyNetworkの残高確認:"
JPY_KEYPAIR=$(curl -s -X POST "http://localhost:5002/api/keypair?network=jpy")
JPY_ADDRESS=$(echo $JPY_KEYPAIR | jq -r .address 2>/dev/null || echo "Error getting address")
echo "新しいアドレス: $JPY_ADDRESS"
JPY_BALANCE=$(curl -s "http://localhost:5002/api/balance/$JPY_ADDRESS?network=jpy")
echo "$JPY_BALANCE" | jq . 2>/dev/null || echo "$JPY_BALANCE"

# Test the balance check for LariNetwork
echo "LariNetworkの残高確認:"
LARI_KEYPAIR=$(curl -s -X POST "http://localhost:5002/api/keypair?network=lari")
LARI_ADDRESS=$(echo $LARI_KEYPAIR | jq -r .address 2>/dev/null || echo "Error getting address")
echo "新しいアドレス: $LARI_ADDRESS"
LARI_BALANCE=$(curl -s "http://localhost:5002/api/balance/$LARI_ADDRESS?network=lari")
echo "$LARI_BALANCE" | jq . 2>/dev/null || echo "$LARI_BALANCE"

# Test the node info endpoint
echo "ノード情報:"
JPY_INFO=$(curl -s "http://localhost:5002/api/node/info?network=jpy")
echo "JpyNetwork情報:"
echo "$JPY_INFO" | jq . 2>/dev/null || echo "$JPY_INFO"

LARI_INFO=$(curl -s "http://localhost:5002/api/node/info?network=lari")
echo "LariNetwork情報:"
echo "$LARI_INFO" | jq . 2>/dev/null || echo "$LARI_INFO"

echo "===== テスト完了 ====="
