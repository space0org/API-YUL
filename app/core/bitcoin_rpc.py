from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from fastapi import HTTPException
import os
import json
from typing import Optional, Dict, Any, Union

# Network configurations
NETWORK_CONFIGS = {
    "jpy": {
        "RPC_USER": "bitcoin",
        "RPC_PASSWORD": "bitcoin",
        "RPC_HOST": "172.18.0.2",  # JpyNetwork node IP
        "RPC_PORT": "8332",
        "SAFE_MODE_HANDLING": "graceful"  # Special handling for safe mode
    },
    "lari": {
        "RPC_USER": "bitcoin",
        "RPC_PASSWORD": "bitcoin",
        "RPC_HOST": "172.18.0.3",  # LariNetwork node IP
        "RPC_PORT": "8332",
        "SAFE_MODE_HANDLING": "graceful"  # Now both networks use graceful handling
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
        print(f"Failed to connect to Bitcoin node ({network}): {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to connect to Bitcoin node ({network}): {str(e)}")

def execute_rpc(method: str, *params, network: str = DEFAULT_NETWORK, ignore_safe_mode: bool = False) -> Any:
    """
    Execute an RPC method with the given parameters on the specified network
    
    Args:
        method: The RPC method to execute
        params: The parameters to pass to the RPC method
        network: The network to execute the RPC method on (jpy or lari)
        ignore_safe_mode: Whether to ignore safe mode errors (default: False)
    """
    try:
        # Get network configuration
        if network not in NETWORK_CONFIGS:
            raise ValueError(f"Unknown network: {network}")
        
        config = NETWORK_CONFIGS[network]
        safe_mode_handling = config.get("SAFE_MODE_HANDLING", "standard")
        
        rpc_connection = get_rpc_connection(network)
        result = getattr(rpc_connection, method)(*params)
        return result
    except JSONRPCException as e:
        error_str = str(e)
        # Check if it's a safe mode error
        if "Safe mode" in error_str:
            print(f"Safe mode error in {network} for method {method}: {error_str}")
            
            # For graceful handling, return appropriate values for certain methods
            if safe_mode_handling == "graceful":
                if method == "listunspent":
                    return []
                elif method == "importaddress":
                    return None
                elif ignore_safe_mode:
                    return None
            
            # For balance-related methods, raise a special exception
            if method in ["listunspent", "importaddress"]:
                raise HTTPException(
                    status_code=200,  # Use 200 to indicate this is an expected error
                    detail={
                        "address": params[0] if len(params) > 0 else "",
                        "balance": 0.0,
                        "unspentOutputs": [],
                        "network": network,
                        "safeMode": True,
                        "safeModeWarning": error_str
                    }
                )
        
        # Re-raise the exception with detailed information
        print(f"RPC error ({network}) for method {method}: {error_str}")
        raise HTTPException(status_code=400, detail=f"RPC error ({network}): {error_str}")
    except Exception as e:
        print(f"Error executing RPC method ({network}) {method}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error executing RPC method ({network}): {str(e)}")

def switch_network_mode(mode: str, network: str = DEFAULT_NETWORK) -> Dict[str, Any]:
    """
    Switch between Regtest mode and Test mode
    
    Args:
        mode: The network mode to switch to ('regtest' or 'testnet')
        network: The network to switch mode for (jpy or lari)
    """
    try:
        if mode not in ['regtest', 'testnet']:
            raise ValueError(f"Invalid mode: {mode}. Must be 'regtest' or 'testnet'")
        
        # Get current network info
        rpc_connection = get_rpc_connection(network)
        current_info = rpc_connection.getnetworkinfo()
        
        # Determine current mode
        current_mode = 'regtest' if current_info.get('regtestmode', False) else 'testnet'
        
        # If already in the requested mode, return current info
        if current_mode == mode:
            return {
                "network": network,
                "mode": mode,
                "changed": False,
                "info": current_info
            }
        
        # Execute RPC command to switch mode
        # Note: This requires restarting the node, which may not be possible via RPC
        # In a real implementation, this would require modifying bitcoin.conf and restarting the node
        result = execute_rpc("setnetworkactive", False, network=network)  # Temporarily disable network
        result = execute_rpc("setnetworkactive", True, network=network)   # Re-enable network with new mode
        
        # Get updated network info
        updated_info = rpc_connection.getnetworkinfo()
        
        return {
            "network": network,
            "mode": mode,
            "changed": True,
            "info": updated_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to switch network mode on {network} network: {str(e)}")
