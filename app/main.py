from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import psycopg2
from app.core.bitcoin_utils import generate_keypair, get_balance, send_transaction, generate_blocks
from app.core.bitcoin_rpc import DEFAULT_NETWORK, DEFAULT_MODE, switch_network_mode, get_current_network_mode

app = FastAPI(
    title="BSV Node API",
    description="API for interacting with a Bitcoin SV node",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and response models
class TransactionRequest(BaseModel):
    fromAddress: str = Field(..., description="Source address")
    privateKey: str = Field(..., description="Private key of the source address")
    toAddress: str = Field(..., description="Destination address")
    amount: float = Field(..., description="Amount to send")
    network: str = Field(DEFAULT_NETWORK, description="Network to use (jpy or lari)")
    mode: str = Field(DEFAULT_MODE, description="Network mode to use (regtest, testnet, or mainnet)")

class KeyPairResponse(BaseModel):
    address: str
    privateKey: str
    network: str
    mode: str

class BalanceResponse(BaseModel):
    address: str
    balance: float
    unspentOutputs: List[Dict[str, Any]]
    network: str
    mode: str
    safeMode: Optional[bool] = None
    safeModeWarning: Optional[str] = None

class TransactionResponse(BaseModel):
    transactionId: str
    fromAddress: str
    toAddress: str
    amount: float
    network: str
    mode: str

class GenerateBlocksRequest(BaseModel):
    address: str = Field(..., description="Address to receive mining rewards")
    numBlocks: int = Field(1, description="Number of blocks to generate")
    network: str = Field(DEFAULT_NETWORK, description="Network to use (jpy or lari)")
    mode: str = Field(DEFAULT_MODE, description="Network mode to use (regtest, testnet, or mainnet)")

class GenerateBlocksResponse(BaseModel):
    address: str
    numBlocks: int
    blockHashes: List[str]
    network: str
    mode: str

class SwitchNetworkModeRequest(BaseModel):
    mode: str = Field(..., description="Network mode to switch to (regtest, testnet, or mainnet)")
    network: str = Field(DEFAULT_NETWORK, description="Network to use (jpy or lari)")

class SwitchNetworkModeResponse(BaseModel):
    network: str
    requestedMode: Optional[str] = None
    currentMode: Optional[str] = None
    mode: Optional[str] = None
    changed: bool
    info: Dict[str, Any]
    warning: Optional[str] = None
    manualStepsRequired: Optional[bool] = None
    documentation: Optional[str] = None

@app.get("/healthz")
async def healthz():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/api/keypair", response_model=KeyPairResponse)
async def create_keypair(
    network: str = Query(DEFAULT_NETWORK, description="Network to use (jpy or lari)"),
    mode: str = Query(DEFAULT_MODE, description="Network mode to use (regtest, testnet, or mainnet)")
):
    """
    Generate a new public-private key pair
    
    Args:
        network: The network to generate the key pair for (jpy or lari)
        mode: The network mode to use (regtest, testnet, or mainnet)
    
    Returns:
        KeyPairResponse: The generated address and private key
    """
    result = generate_keypair(network=network, mode=mode)
    result["mode"] = mode
    return result

@app.get("/api/balance/{address}", response_model=None)
async def check_balance(
    address: str,
    network: str = Query(DEFAULT_NETWORK, description="Network to use (jpy or lari)"),
    mode: str = Query(DEFAULT_MODE, description="Network mode to use (regtest, testnet, or mainnet)")
):
    """
    Get the balance for a specific address
    
    Args:
        address: The Bitcoin address to check
        network: The network to check the balance on (jpy or lari)
        mode: The network mode to use (regtest, testnet, or mainnet)
        
    Returns:
        BalanceResponse: The balance and unspent outputs for the address
    """
    result = get_balance(address, network=network, mode=mode)
    result["mode"] = mode
    return result

@app.post("/api/send", response_model=TransactionResponse)
async def send_transaction_endpoint(transaction: TransactionRequest):
    """
    Send a transaction from one address to another
    
    Args:
        transaction: The transaction details
        
    Returns:
        TransactionResponse: The transaction result
    """
    result = send_transaction(
        transaction.fromAddress,
        transaction.privateKey,
        transaction.toAddress,
        transaction.amount,
        network=transaction.network,
        mode=transaction.mode
    )
    result["mode"] = transaction.mode
    return result

@app.get("/api/node/info")
async def get_node_info(
    network: str = Query(DEFAULT_NETWORK, description="Network to use (jpy or lari)"),
    mode: str = Query(DEFAULT_MODE, description="Network mode to use (regtest, testnet, or mainnet)")
):
    """
    Get information about the BSV node
    
    Args:
        network: The network to get information for (jpy or lari)
        mode: The network mode to use (regtest, testnet, or mainnet)
    
    Returns:
        Dict: Node information
    """
    from app.core.bitcoin_rpc import execute_rpc
    
    network_info = execute_rpc("getnetworkinfo", network=network, mode=mode)
    blockchain_info = execute_rpc("getblockchaininfo", network=network, mode=mode)
    
    return {
        "version": network_info["version"],
        "subversion": network_info["subversion"],
        "connections": network_info["connections"],
        "chain": blockchain_info["chain"],
        "blocks": blockchain_info["blocks"],
        "difficulty": blockchain_info["difficulty"],
        "network": network,
        "mode": mode
    }

@app.post("/api/generate", response_model=GenerateBlocksResponse)
async def generate_blocks_endpoint(request: GenerateBlocksRequest):
    """
    Generate blocks with mining rewards going to the specified address
    
    Args:
        request: The generate blocks request details
        
    Returns:
        GenerateBlocksResponse: The generate blocks result
    """
    result = generate_blocks(request.address, request.numBlocks, network=request.network, mode=request.mode)
    result["mode"] = request.mode
    return result

@app.post("/api/network/mode", response_model=SwitchNetworkModeResponse)
async def switch_network_mode_endpoint(request: SwitchNetworkModeRequest):
    """
    Switch between Regtest, Testnet, and Mainnet modes
    
    Args:
        request: The switch network mode request details
        
    Returns:
        SwitchNetworkModeResponse: The switch network mode result
    """
    return switch_network_mode(request.mode, network=request.network)

@app.get("/api/network/mode")
async def get_network_mode(
    network: str = Query(DEFAULT_NETWORK, description="Network to get mode for (jpy or lari)")
):
    """
    Get the current network mode
    
    Args:
        network: The network to get the mode for (jpy or lari)
        
    Returns:
        Dict: The current network mode
    """
    current_mode = get_current_network_mode(network)
    
    return {
        "network": network,
        "currentMode": current_mode
    }
