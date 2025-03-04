from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from fastapi import HTTPException
import os
from typing import Optional, Dict

# Network configurations
NETWORK_CONFIGS = {
    "jpy": {
        "RPC_USER": "jpyuser",
        "RPC_PASSWORD": "jpypassword",
        "RPC_HOST": "localhost",  # Default to localhost for local development
        "RPC_PORT": "18332"
    },
    "lari": {
        "RPC_USER": "lariuser",
        "RPC_PASSWORD": "laripassword",
        "RPC_HOST": "localhost",  # Default to localhost for local development
        "RPC_PORT": "19332"  # Different port for LariNetwork
    }
}

# Default network
DEFAULT_NETWORK = "jpy"

def get_rpc_connection(network: str = DEFAULT_NETWORK) -> AuthServiceProxy:
    """
    Create and return a Bitcoin RPC connection for the specified network
    
    Args:
        network: The network to connect to (jpy or lari)
    """
    try:
        # Get network configuration
        if network not in NETWORK_CONFIGS:
            raise ValueError(f"Unknown network: {network}")
        
        config = NETWORK_CONFIGS[network]
        
        # Override with environment variables if available
        rpc_user = os.environ.get(f"{network.upper()}_RPC_USER", config["RPC_USER"])
        rpc_password = os.environ.get(f"{network.upper()}_RPC_PASSWORD", config["RPC_PASSWORD"])
        rpc_host = os.environ.get(f"{network.upper()}_RPC_HOST", config["RPC_HOST"])
        rpc_port = os.environ.get(f"{network.upper()}_RPC_PORT", config["RPC_PORT"])
        
        # Create RPC URL
        rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"
        
        return AuthServiceProxy(rpc_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Bitcoin node ({network}): {str(e)}")

def execute_rpc(method: str, *params, network: str = DEFAULT_NETWORK) -> any:
    """
    Execute an RPC method with the given parameters on the specified network
    
    Args:
        method: The RPC method to execute
        params: The parameters to pass to the RPC method
        network: The network to execute the RPC method on (jpy or lari)
    """
    try:
        rpc_connection = get_rpc_connection(network)
        result = getattr(rpc_connection, method)(*params)
        return result
    except JSONRPCException as e:
        raise HTTPException(status_code=400, detail=f"RPC error ({network}): {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing RPC method ({network}): {str(e)}")
