#!/bin/bash

# Test script for API-YUL network support
echo "Testing API-YUL network support..."

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

# Test keypair creation for LariNetwork
echo "Testing keypair creation for LariNetwork..."
LARI_KEYPAIR=$(curl -s -X POST "http://localhost:5003/api/keypair?network=lari")
echo "LariNetwork keypair: $LARI_KEYPAIR"

# Clean up
echo "Cleaning up..."
docker stop api-yul-test
docker rm api-yul-test

echo "Test completed."
