from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import psycopg
from app.core.bitcoin_utils import generate_keypair, get_balance, send_transaction
from app.core.bitcoin_rpc import DEFAULT_NETWORK

app = FastAPI(
    title="BSV Node API",
    description="API for interacting with a Bitcoin SV node",
    version="1.0.0"
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Models for request and response
class TransactionRequest(BaseModel):
    fromAddress: str = Field(..., description="Source address")
    privateKey: str = Field(..., description="Private key of the source address")
    toAddress: str = Field(..., description="Destination address")
    amount: float = Field(..., description="Amount to send")
    network: str = Field(DEFAULT_NETWORK, description="Network to use (jpy or lari)")

class KeyPairResponse(BaseModel):
    address: str
    privateKey: str
    network: str

class BalanceResponse(BaseModel):
    address: str
    balance: float
    unspentOutputs: List[Dict[str, Any]]
    network: str

class TransactionResponse(BaseModel):
    transactionId: str
    fromAddress: str
    toAddress: str
    amount: float
    network: str

@app.get("/healthz")
async def healthz():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/api/keypair", response_model=KeyPairResponse)
async def create_keypair(network: str = Query(DEFAULT_NETWORK, description="Network to use (jpy or lari)")):
    """
    Generate a new public-private key pair
    
    Args:
        network: The network to generate the key pair for (jpy or lari)
    
    Returns:
        KeyPairResponse: The generated address and private key
    """
    return generate_keypair(network=network)

@app.get("/api/balance/{address}", response_model=BalanceResponse)
async def check_balance(
    address: str,
    network: str = Query(DEFAULT_NETWORK, description="Network to use (jpy or lari)")
):
    """
    Get the balance for a specific address
    
    Args:
        address: The Bitcoin address to check
        network: The network to check the balance on (jpy or lari)
        
    Returns:
        BalanceResponse: The balance and unspent outputs for the address
    """
    return get_balance(address, network=network)

@app.post("/api/send", response_model=TransactionResponse)
async def send_transaction_endpoint(transaction: TransactionRequest):
    """
    Send BSV from one address to another
    
    Args:
        transaction: The transaction details
        
    Returns:
        TransactionResponse: The transaction result
    """
    return send_transaction(
        transaction.fromAddress,
        transaction.privateKey,
        transaction.toAddress,
        transaction.amount,
        network=transaction.network
    )

@app.get("/api/node/info")
async def get_node_info(
    network: str = Query(DEFAULT_NETWORK, description="Network to use (jpy or lari)")
):
    """
    Get information about the BSV node
    
    Args:
        network: The network to get information for (jpy or lari)
    
    Returns:
        Dict: Node information
    """
    from app.core.bitcoin_rpc import execute_rpc
    
    network_info = execute_rpc("getnetworkinfo", network=network)
    blockchain_info = execute_rpc("getblockchaininfo", network=network)
    
    return {
        "version": network_info["version"],
        "subversion": network_info["subversion"],
        "connections": network_info["connections"],
        "chain": blockchain_info["chain"],
        "blocks": blockchain_info["blocks"],
        "difficulty": blockchain_info["difficulty"],
        "network": network
    }
