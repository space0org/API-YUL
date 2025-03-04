#!/bin/bash

# Test script for mining rewards generation and network mode switching

echo "===== Testing Mining Rewards Generation ====="

# Generate a new keypair
echo "Generating a new keypair..."
KEYPAIR=$(curl -s -X POST "http://localhost:5002/api/keypair?network=jpy")
echo "Keypair response:"
echo $KEYPAIR | jq

# Extract address from keypair
if [ -n "$KEYPAIR" ]; then
  ADDRESS=$(echo $KEYPAIR | jq -r '.address')
  echo "Generated address: $ADDRESS"
  
  # Check initial balance
  echo "Checking initial balance..."
  BALANCE=$(curl -s "http://localhost:5002/api/balance/$ADDRESS?network=jpy")
  echo "Initial balance:"
  echo $BALANCE | jq
  
  # Generate mining rewards
  echo "Generating mining rewards..."
  MINING=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"address\":\"$ADDRESS\",\"numBlocks\":1,\"network\":\"jpy\"}" "http://localhost:5002/api/generate")
  echo "Mining response:"
  echo $MINING | jq
  
  # Check updated balance
  echo "Checking updated balance..."
  BALANCE=$(curl -s "http://localhost:5002/api/balance/$ADDRESS?network=jpy")
  echo "Updated balance:"
  echo $BALANCE | jq
fi

echo "===== Testing Network Mode Switching ====="

# Check current network mode
echo "Checking current network mode..."
NODE_INFO=$(curl -s "http://localhost:5002/api/node/info?network=jpy")
echo "Current node info:"
echo $NODE_INFO | jq

# Switch to testnet mode
echo "Switching to testnet mode..."
MODE_SWITCH=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"mode\":\"testnet\",\"network\":\"jpy\"}" "http://localhost:5002/api/network/mode")
echo "Mode switch response:"
echo $MODE_SWITCH | jq

# Check updated network mode
echo "Checking updated network mode..."
NODE_INFO=$(curl -s "http://localhost:5002/api/node/info?network=jpy")
echo "Updated node info:"
echo $NODE_INFO | jq

# Switch back to regtest mode
echo "Switching back to regtest mode..."
MODE_SWITCH=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"mode\":\"regtest\",\"network\":\"jpy\"}" "http://localhost:5002/api/network/mode")
echo "Mode switch response:"
echo $MODE_SWITCH | jq

echo "Testing completed."
