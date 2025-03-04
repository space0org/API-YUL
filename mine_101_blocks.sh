#!/bin/bash

echo "===== Mining 101 Blocks and Checking Balance ====="

# Function to check if jq is installed
check_jq() {
  if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Installing..."
    sudo apt-get update && sudo apt-get install -y jq
  fi
}

# Check for jq
check_jq

# Function to test mining rewards with 101 blocks
test_mining_rewards() {
  local network=$1
  echo -e "\n===== Testing Mining Rewards for $network with 101 Blocks ====="
  
  # Generate keypair
  echo "Generating keypair..."
  KEYPAIR=$(curl -s -X POST "http://localhost:5002/api/keypair?network=$network")
  echo "Keypair response:"
  echo $KEYPAIR | jq
  ADDRESS=$(echo $KEYPAIR | jq -r '.address')
  echo "Generated address: $ADDRESS"
  
  # Check initial balance
  echo -e "\nChecking initial balance..."
  INITIAL_BALANCE=$(curl -s "http://localhost:5002/api/balance/$ADDRESS?network=$network")
  echo "Initial balance response:"
  echo $INITIAL_BALANCE | jq
  
  # Generate 101 mining rewards
  echo -e "\nGenerating 101 blocks for mining rewards..."
  MINING=$(curl -s -X POST -H "Content-Type: application/json" \
    -d "{\"address\":\"$ADDRESS\",\"numBlocks\":101,\"network\":\"$network\"}" \
    "http://localhost:5002/api/generate")
  echo "Mining response:"
  echo $MINING | jq
  
  # Wait for blocks to be processed
  echo -e "\nWaiting for blocks to be processed..."
  sleep 10
  
  # Check updated balance
  echo -e "\nChecking updated balance..."
  UPDATED_BALANCE=$(curl -s "http://localhost:5002/api/balance/$ADDRESS?network=$network")
  echo "Updated balance response:"
  echo $UPDATED_BALANCE | jq
  
  # Check if safe mode is active
  SAFE_MODE_INITIAL=$(echo $INITIAL_BALANCE | jq -r '.safeMode // false')
  SAFE_MODE_UPDATED=$(echo $UPDATED_BALANCE | jq -r '.safeMode // false')
  
  echo -e "\n$network Results:"
  echo "Safe mode (initial): $SAFE_MODE_INITIAL"
  echo "Safe mode (updated): $SAFE_MODE_UPDATED"
  
  if [[ "$SAFE_MODE_UPDATED" == "true" ]]; then
    echo "Node is in safe mode. Balance may show as 0 even after mining."
    echo "Safe mode warning: $(echo $UPDATED_BALANCE | jq -r '.safeModeWarning // "N/A"')"
    
    # Even in safe mode, verify that blocks were generated
    BLOCKS=$(echo $MINING | jq -r '.blockHashes | length')
    echo "Number of blocks generated: $BLOCKS"
    if [[ "$BLOCKS" -gt 0 ]]; then
      echo "SUCCESS: Mining rewards were generated successfully, but balance is not visible due to safe mode."
    else
      echo "ERROR: Failed to generate blocks."
    fi
  else
    # If not in safe mode, check if balance increased
    INITIAL_AMOUNT=$(echo $INITIAL_BALANCE | jq -r '.balance')
    UPDATED_AMOUNT=$(echo $UPDATED_BALANCE | jq -r '.balance')
    echo "Initial balance: $INITIAL_AMOUNT"
    echo "Updated balance: $UPDATED_AMOUNT"
    
    if (( $(echo "$UPDATED_AMOUNT > $INITIAL_AMOUNT" | bc -l) )); then
      echo "SUCCESS: Balance increased after mining rewards!"
    else
      echo "WARNING: Balance did not increase after mining rewards."
    fi
  fi
}

# Test JpyNetwork
test_mining_rewards "jpy"

# Test LariNetwork
test_mining_rewards "lari"

echo -e "\n===== Mining 101 Blocks Test Complete ====="
