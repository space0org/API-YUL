from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from fastapi import HTTPException
import os
from typing import Optional, Dict, Any

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

# Network mode configurations
NETWORK_MODE_CONFIGS = {
    "regtest": {
        "jpy": {
            "RPC_PORT": "18332"
        },
        "lari": {
            "RPC_PORT": "19332"
        }
    },
    "testnet": {
        "jpy": {
            "RPC_PORT": "18333"
        },
        "lari": {
            "RPC_PORT": "19333"
        }
    },
    "mainnet": {
        "jpy": {
            "RPC_PORT": "18444"  # Custom port for JpyNetwork mainnet
        },
        "lari": {
            "RPC_PORT": "19444"  # Custom port for LariNetwork mainnet
        }
    }
}

# Default network
DEFAULT_NETWORK = "jpy"

# Default network mode
DEFAULT_MODE = "regtest"

def get_rpc_connection(network: str = DEFAULT_NETWORK, mode: str = DEFAULT_MODE) -> AuthServiceProxy:
    """
    Create and return a Bitcoin RPC connection for the specified network and mode
    
    Args:
        network: The network to connect to (jpy or lari)
        mode: The network mode to use (regtest, testnet, or mainnet)
    """
    try:
        # Get network configuration
        if network not in NETWORK_CONFIGS:
            raise ValueError(f"Unknown network: {network}")
        
        if mode not in NETWORK_MODE_CONFIGS:
            raise ValueError(f"Unknown mode: {mode}. Must be 'regtest', 'testnet', or 'mainnet'")
        
        config = NETWORK_CONFIGS[network].copy()
        
        # Override with mode-specific configuration if available
        if network in NETWORK_MODE_CONFIGS.get(mode, {}):
            for key, value in NETWORK_MODE_CONFIGS[mode][network].items():
                config[key] = value
        
        # Override with environment variables if available
        rpc_user = os.environ.get(f"{network.upper()}_{mode.upper()}_RPC_USER", 
                                 os.environ.get(f"{network.upper()}_RPC_USER", 
                                              config["RPC_USER"]))
        
        rpc_password = os.environ.get(f"{network.upper()}_{mode.upper()}_RPC_PASSWORD", 
                                     os.environ.get(f"{network.upper()}_RPC_PASSWORD", 
                                                  config["RPC_PASSWORD"]))
        
        rpc_host = os.environ.get(f"{network.upper()}_{mode.upper()}_RPC_HOST", 
                                 os.environ.get(f"{network.upper()}_RPC_HOST", 
                                              config["RPC_HOST"]))
        
        rpc_port = os.environ.get(f"{network.upper()}_{mode.upper()}_RPC_PORT", 
                                 os.environ.get(f"{network.upper()}_RPC_PORT", 
                                              config["RPC_PORT"]))
        
        # Create RPC URL
        rpc_url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"
        
        return AuthServiceProxy(rpc_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Bitcoin node ({network}, {mode}): {str(e)}")

def execute_rpc(method: str, *params, network: str = DEFAULT_NETWORK, mode: str = DEFAULT_MODE, ignore_safe_mode: bool = False) -> Any:
    """
    Execute an RPC method with the given parameters on the specified network and mode
    
    Args:
        method: The RPC method to execute
        params: The parameters to pass to the RPC method
        network: The network to execute the RPC method on (jpy or lari)
        mode: The network mode to use (regtest, testnet, or mainnet)
        ignore_safe_mode: Whether to ignore safe mode errors (default: False)
    """
    try:
        rpc_connection = get_rpc_connection(network, mode)
        result = getattr(rpc_connection, method)(*params)
        return result
    except JSONRPCException as e:
        # Check if it's a safe mode error and we should ignore it
        if ignore_safe_mode and "Safe mode" in str(e):
            # Return None for safe mode errors when ignore_safe_mode is True
            return None
        else:
            raise HTTPException(status_code=400, detail=f"RPC error ({network}, {mode}): {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing RPC method ({network}, {mode}): {str(e)}")

def get_current_network_mode(network: str = DEFAULT_NETWORK) -> str:
    """
    Get the current network mode for the specified network
    
    Args:
        network: The network to get the mode for (jpy or lari)
    """
    try:
        # Get current network info
        rpc_connection = get_rpc_connection(network)
        blockchain_info = rpc_connection.getblockchaininfo()
        
        # Determine current mode based on chain
        chain = blockchain_info.get('chain', '')
        
        if chain == 'regtest':
            return 'regtest'
        elif chain == 'test':
            return 'testnet'
        elif chain == 'main':
            return 'mainnet'
        else:
            return 'unknown'
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get current network mode for {network}: {str(e)}")

def switch_network_mode(mode: str, network: str = DEFAULT_NETWORK) -> Dict[str, Any]:
    """
    Switch between Regtest, Testnet, and Mainnet modes
    
    Args:
        mode: The network mode to switch to ('regtest', 'testnet', or 'mainnet')
        network: The network to switch mode for (jpy or lari)
    """
    try:
        if mode not in ['regtest', 'testnet', 'mainnet']:
            raise ValueError(f"Invalid mode: {mode}. Must be 'regtest', 'testnet', or 'mainnet'")
        
        # Get current network mode
        current_mode = get_current_network_mode(network)
        
        # Get current network info using the current mode
        rpc_connection = get_rpc_connection(network, current_mode)
        current_info = rpc_connection.getnetworkinfo()
        
        # If already in the requested mode, return current info
        if current_mode == mode:
            return {
                "network": network,
                "requestedMode": mode,
                "currentMode": current_mode,
                "changed": False,
                "info": current_info,
                "warning": None
            }
        
        # Add warnings based on the requested mode
        warning = None
        if mode == 'mainnet':
            warning = "警告: Multi-Bsv-NetworkのMainnetモードに切り替えます。これは実際のBitcoin SVネットワークではなく、JpyNetworkとLariNetworkのカスタムチェーンです。完全な切り替えには、bitcoin.confファイルの編集とノードの再起動が必要です。"
        elif mode == 'testnet':
            warning = "警告: Testnetモードへの完全な切り替えには、bitcoin.confファイルの編集とノードの再起動が必要です。APIだけでは完全な切り替えはできません。"
        
        # Try to connect to the requested mode
        try:
            # Try to get network info using the requested mode
            new_rpc_connection = get_rpc_connection(network, mode)
            new_info = new_rpc_connection.getnetworkinfo()
            
            return {
                "network": network,
                "requestedMode": mode,
                "currentMode": current_mode,
                "changed": True,
                "info": new_info,
                "warning": warning
            }
        except Exception as e:
            # If we can't connect to the requested mode, add that to the warning
            if warning:
                warning += f" また、{mode}モードへの接続に失敗しました: {str(e)}"
            else:
                warning = f"{mode}モードへの接続に失敗しました: {str(e)}"
            
            # In a real implementation, we would need to:
            # 1. Modify bitcoin.conf
            # 2. Restart the node
            # 3. Wait for the node to sync with the new network
            
            return {
                "network": network,
                "requestedMode": mode,
                "currentMode": current_mode,
                "changed": False,
                "info": current_info,
                "warning": warning,
                "manualStepsRequired": True,
                "documentation": "multi_bsv_network_mode_switching_guide_ja.md"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to switch network mode on {network} network: {str(e)}")
