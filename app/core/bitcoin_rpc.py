from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from fastapi import HTTPException
import os
from typing import Optional

# Bitcoin RPC connection settings
RPC_USER = "bitcoin"
RPC_PASSWORD = "bitcoin"
RPC_HOST = "3.26.38.112"  # BSV Node IP
RPC_PORT = "18332"
RPC_URL = f"http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}"

def get_rpc_connection() -> AuthServiceProxy:
    """
    Create and return a Bitcoin RPC connection
    """
    try:
        return AuthServiceProxy(RPC_URL)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Bitcoin node: {str(e)}")

def execute_rpc(method: str, *params) -> any:
    """
    Execute an RPC method with the given parameters
    """
    try:
        rpc_connection = get_rpc_connection()
        result = getattr(rpc_connection, method)(*params)
        return result
    except JSONRPCException as e:
        raise HTTPException(status_code=400, detail=f"RPC error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing RPC method: {str(e)}")
