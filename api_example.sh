#!/bin/bash

API_URL="https://app-fhxknmbw.fly.dev"

echo "BSVノードAPI使用例"
echo "==================="

# 1. 公開鍵と秘密鍵のペア作成
echo "1. 公開鍵と秘密鍵のペア作成"
KEY_PAIR=$(curl -s -X POST $API_URL/api/keypair)
echo $KEY_PAIR | jq

# アドレスと秘密鍵を抽出
ADDRESS=$(echo $KEY_PAIR | jq -r '.address')
PRIVATE_KEY=$(echo $KEY_PAIR | jq -r '.privateKey')

echo "生成されたアドレス: $ADDRESS"
echo "生成された秘密鍵: $PRIVATE_KEY"

# 2. 残高確認
echo -e "\n2. 残高確認"
curl -s $API_URL/api/balance/$ADDRESS | jq

# 3. 別のアドレスを生成
echo -e "\n3. 別のアドレスを生成（送金先）"
SECOND_KEY_PAIR=$(curl -s -X POST $API_URL/api/keypair)
SECOND_ADDRESS=$(echo $SECOND_KEY_PAIR | jq -r '.address')
echo "送金先アドレス: $SECOND_ADDRESS"

# 4. 送金（注：実際の送金には十分な残高が必要です）
echo -e "\n4. 送金（デモ - 実際には十分な残高が必要）"
curl -s -X POST $API_URL/api/send \
  -H "Content-Type: application/json" \
  -d "{
    \"fromAddress\": \"$ADDRESS\",
    \"privateKey\": \"$PRIVATE_KEY\",
    \"toAddress\": \"$SECOND_ADDRESS\",
    \"amount\": 1.0
  }" | jq

# 5. ノード情報
echo -e "\n5. ノード情報"
curl -s $API_URL/api/node/info | jq
