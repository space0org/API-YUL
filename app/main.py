from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import psycopg
import json
from app.core.bitcoin_utils import generate_keypair, get_balance, send_transaction, generate_blocks
from app.core.bitcoin_rpc import DEFAULT_NETWORK, switch_network_mode

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

# Exception handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Check if the detail is a dictionary
    if isinstance(exc.detail, dict):
        # Return the detail as JSON
        return JSONResponse(
            status_code=200,  # Always return 200 to avoid API errors
            content=exc.detail
        )
    # Check if the detail is a string that might be JSON
    elif isinstance(exc.detail, str):
        try:
            # Try to parse the detail as JSON
            detail_json = json.loads(exc.detail)
            # Return the parsed JSON
            return JSONResponse(
                status_code=200,  # Always return 200 to avoid API errors
                content=detail_json
            )
        except json.JSONDecodeError:
            # If it's not valid JSON, return it as a string
            pass
    
    # Default handling for other cases
    return JSONResponse(
        status_code=200,  # Always return 200 to avoid API errors
        content={"error": str(exc.detail)}
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
    safeMode: Optional[bool] = None
    safeModeWarning: Optional[str] = None
    error: Optional[str] = None

class TransactionResponse(BaseModel):
    transactionId: Optional[str] = None
    fromAddress: str
    toAddress: str
    amount: float
    network: str
    error: Optional[str] = None
    safeMode: Optional[bool] = None
    safeModeWarning: Optional[str] = None

class GenerateBlocksRequest(BaseModel):
    address: str = Field(..., description="Address to receive mining rewards")
    numBlocks: int = Field(1, description="Number of blocks to generate")
    network: str = Field(DEFAULT_NETWORK, description="Network to use (jpy or lari)")

class GenerateBlocksResponse(BaseModel):
    address: str
    numBlocks: int
    blockHashes: Optional[List[str]] = None
    network: str
    error: Optional[str] = None
    safeMode: Optional[bool] = None
    safeModeWarning: Optional[str] = None

class SwitchNetworkModeRequest(BaseModel):
    mode: str = Field(..., description="Network mode to switch to (regtest or testnet)")
    network: str = Field(DEFAULT_NETWORK, description="Network to use (jpy or lari)")

class SwitchNetworkModeResponse(BaseModel):
    network: str
    mode: str
    changed: bool
    info: Dict[str, Any]
    error: Optional[str] = None

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
    try:
        return generate_keypair(network=network)
    except Exception as e:
        # Return a structured error response
        return {
            "address": "",
            "privateKey": "",
            "network": network,
            "error": str(e)
        }

@app.get("/api/balance/{address}")
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
    try:
        # Try to get the balance using the existing function
        return get_balance(address, network=network)
    except Exception as e:
        # Return a structured error response
        error_message = str(e)
        
        # Check if it's a safe mode error
        is_safe_mode = "Safe mode" in error_message
        
        response = {
            "address": address,
            "balance": 0.0,
            "unspentOutputs": [],
            "network": network,
            "error": error_message
        }
        
        # Add safe mode information if applicable
        if is_safe_mode:
            response["safeMode"] = True
            response["safeModeWarning"] = error_message
        
        return response

@app.post("/api/send")
async def send_transaction_endpoint(transaction: TransactionRequest):
    """
    Send BSV from one address to another
    
    Args:
        transaction: The transaction details
        
    Returns:
        TransactionResponse: The transaction result
    """
    try:
        # Try to send the transaction using the existing function
        return send_transaction(
            transaction.fromAddress,
            transaction.privateKey,
            transaction.toAddress,
            transaction.amount,
            network=transaction.network
        )
    except Exception as e:
        # Return a structured error response
        error_message = str(e)
        
        # Check if it's a safe mode error
        is_safe_mode = "Safe mode" in error_message
        
        response = {
            "fromAddress": transaction.fromAddress,
            "toAddress": transaction.toAddress,
            "amount": transaction.amount,
            "network": transaction.network,
            "error": error_message
        }
        
        # Add safe mode information if applicable
        if is_safe_mode:
            response["safeMode"] = True
            response["safeModeWarning"] = error_message
        
        return response

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
    
    try:
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
    except Exception as e:
        # Return a structured error response
        error_message = str(e)
        
        # Check if it's a safe mode error
        is_safe_mode = "Safe mode" in error_message
        
        response = {
            "network": network,
            "error": error_message
        }
        
        # Add safe mode information if applicable
        if is_safe_mode:
            response["safeMode"] = True
            response["safeModeWarning"] = error_message
        
        return response

@app.post("/api/generate")
async def generate_blocks_endpoint(request: GenerateBlocksRequest):
    """
    Generate blocks with mining rewards going to the specified address
    
    Args:
        request: The generate blocks request details
        
    Returns:
        GenerateBlocksResponse: The generate blocks result
    """
    try:
        # Try to generate blocks using the existing function
        return generate_blocks(request.address, request.numBlocks, network=request.network)
    except Exception as e:
        # Return a structured error response
        error_message = str(e)
        
        # Check if it's a safe mode error
        is_safe_mode = "Safe mode" in error_message
        
        response = {
            "address": request.address,
            "numBlocks": request.numBlocks,
            "network": request.network,
            "error": error_message
        }
        
        # Add safe mode information if applicable
        if is_safe_mode:
            response["safeMode"] = True
            response["safeModeWarning"] = error_message
        
        return response

@app.post("/api/network/mode")
async def switch_network_mode_endpoint(request: SwitchNetworkModeRequest):
    """
    Switch between Regtest mode and Test mode
    
    Args:
        request: The switch network mode request details
        
    Returns:
        SwitchNetworkModeResponse: The switch network mode result
    """
    try:
        # Try to switch network mode using the existing function
        return switch_network_mode(request.mode, network=request.network)
    except Exception as e:
        # Return a structured error response
        error_message = str(e)
        
        response = {
            "network": request.network,
            "mode": request.mode,
            "changed": False,
            "info": {},
            "error": error_message
        }
        
        return response
