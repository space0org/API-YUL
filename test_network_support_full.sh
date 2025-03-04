#!/bin/bash

# Full Test Script for Network Parameter Support in API-YUL
# This script tests the API endpoints with network parameters for both JpyNetwork and LariNetwork

# Stop and remove existing test container if it exists
echo "Cleaning up existing containers..."
docker stop api-yul-test || true
docker rm api-yul-test || true

# Build the Docker image
echo "Building Docker image..."
docker build -t api-yul-test .

# Run the Docker container
echo "Running Docker container..."
docker run -d --name api-yul-test -p 5003:5002 api-yul-test

# Wait for the container to start
echo "Waiting for container to start..."
sleep 5

# Test the health check endpoint
echo "Testing health check endpoint..."
HEALTH=$(curl -s http://localhost:5003/healthz)
echo "Health check response: $HEALTH"

# Test keypair creation for JpyNetwork
echo "Testing keypair creation for JpyNetwork..."
JPY_KEYPAIR=$(curl -s -X POST "http://localhost:5003/api/keypair?network=jpy")
echo "JpyNetwork keypair: $JPY_KEYPAIR"

# Extract address and private key from JpyNetwork keypair
JPY_ADDRESS=$(echo $JPY_KEYPAIR | grep -o '"address":"[^"]*"' | cut -d'"' -f4)
JPY_PRIVATE_KEY=$(echo $JPY_KEYPAIR | grep -o '"privateKey":"[^"]*"' | cut -d'"' -f4)
echo "JpyNetwork address: $JPY_ADDRESS"
echo "JpyNetwork private key: $JPY_PRIVATE_KEY"

# Test keypair creation for LariNetwork
echo "Testing keypair creation for LariNetwork..."
LARI_KEYPAIR=$(curl -s -X POST "http://localhost:5003/api/keypair?network=lari")
echo "LariNetwork keypair: $LARI_KEYPAIR"

# Extract address and private key from LariNetwork keypair
LARI_ADDRESS=$(echo $LARI_KEYPAIR | grep -o '"address":"[^"]*"' | cut -d'"' -f4)
LARI_PRIVATE_KEY=$(echo $LARI_KEYPAIR | grep -o '"privateKey":"[^"]*"' | cut -d'"' -f4)
echo "LariNetwork address: $LARI_ADDRESS"
echo "LariNetwork private key: $LARI_PRIVATE_KEY"

# Test balance check for JpyNetwork
echo "Testing balance check for JpyNetwork..."
JPY_BALANCE=$(curl -s "http://localhost:5003/api/balance/$JPY_ADDRESS?network=jpy")
echo "JpyNetwork balance: $JPY_BALANCE"

# Test balance check for LariNetwork
echo "Testing balance check for LariNetwork..."
LARI_BALANCE=$(curl -s "http://localhost:5003/api/balance/$LARI_ADDRESS?network=lari")
echo "LariNetwork balance: $LARI_BALANCE"

# Test node info for JpyNetwork
echo "Testing node info for JpyNetwork..."
JPY_NODE_INFO=$(curl -s "http://localhost:5003/api/node/info?network=jpy")
echo "JpyNetwork node info: $JPY_NODE_INFO"

# Test node info for LariNetwork
echo "Testing node info for LariNetwork..."
LARI_NODE_INFO=$(curl -s "http://localhost:5003/api/node/info?network=lari")
echo "LariNetwork node info: $LARI_NODE_INFO"

# Clean up
echo "Cleaning up..."
docker stop api-yul-test
docker rm api-yul-test

echo "Test completed."
