#!/bin/bash

# Set colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}===== ネットワークモードAPIエンドポイントのテスト =====${NC}"

# Get current network mode for JpyNetwork
echo -e "${YELLOW}JpyNetworkの現在のネットワークモードを取得中...${NC}"
JPY_MODE=$(curl -s "http://localhost:5002/api/network/mode?network=jpy")
echo -e "${GREEN}JpyNetworkの現在のモード:${NC}"
echo "$JPY_MODE" | python3 -m json.tool 2>/dev/null || echo "$JPY_MODE"

# Get current network mode for LariNetwork
echo -e "${YELLOW}LariNetworkの現在のネットワークモードを取得中...${NC}"
LARI_MODE=$(curl -s "http://localhost:5002/api/network/mode?network=lari")
echo -e "${GREEN}LariNetworkの現在のモード:${NC}"
echo "$LARI_MODE" | python3 -m json.tool 2>/dev/null || echo "$LARI_MODE"

# Try to switch JpyNetwork to mainnet mode
echo -e "${YELLOW}JpyNetworkをmainnetモードに切り替え中...${NC}"
JPY_SWITCH=$(curl -s -X POST "http://localhost:5002/api/network/mode" \
  -H "Content-Type: application/json" \
  -d '{"mode":"mainnet","network":"jpy"}')

echo -e "${GREEN}JpyNetworkの切り替え結果:${NC}"
echo "$JPY_SWITCH" | python3 -m json.tool 2>/dev/null || echo "$JPY_SWITCH"

# Try to switch LariNetwork to mainnet mode
echo -e "${YELLOW}LariNetworkをmainnetモードに切り替え中...${NC}"
LARI_SWITCH=$(curl -s -X POST "http://localhost:5002/api/network/mode" \
  -H "Content-Type: application/json" \
  -d '{"mode":"mainnet","network":"lari"}')

echo -e "${GREEN}LariNetworkの切り替え結果:${NC}"
echo "$LARI_SWITCH" | python3 -m json.tool 2>/dev/null || echo "$LARI_SWITCH"

# Get current network mode for JpyNetwork after switch attempt
echo -e "${YELLOW}切り替え後のJpyNetworkのネットワークモードを取得中...${NC}"
JPY_MODE_AFTER=$(curl -s "http://localhost:5002/api/network/mode?network=jpy")
echo -e "${GREEN}JpyNetworkの現在のモード:${NC}"
echo "$JPY_MODE_AFTER" | python3 -m json.tool 2>/dev/null || echo "$JPY_MODE_AFTER"

# Get current network mode for LariNetwork after switch attempt
echo -e "${YELLOW}切り替え後のLariNetworkのネットワークモードを取得中...${NC}"
LARI_MODE_AFTER=$(curl -s "http://localhost:5002/api/network/mode?network=lari")
echo -e "${GREEN}LariNetworkの現在のモード:${NC}"
echo "$LARI_MODE_AFTER" | python3 -m json.tool 2>/dev/null || echo "$LARI_MODE_AFTER"

echo -e "${YELLOW}===== ネットワークモードAPIエンドポイントのテスト完了 =====${NC}"
