from app.core.bitcoin_rpc import execute_rpc, DEFAULT_NETWORK
from fastapi import HTTPException
from typing import Dict, List, Any, Optional
from bitcoinrpc.authproxy import JSONRPCException

def generate_keypair(network: str = DEFAULT_NETWORK) -> Dict[str, str]:
    """
    Generate a new Bitcoin address and private key
    
    Args:
        network: The network to generate the key pair for (jpy or lari)
    """
    try:
        # Generate a new address
        address = execute_rpc("getnewaddress", network=network)
        
        # Get the private key for this address
        private_key = execute_rpc("dumpprivkey", address, network=network)
        
        return {
            "address": address,
            "privateKey": private_key,
            "network": network
        }
    except Exception as e:
        # Return a structured error response
        return {
            "address": "",
            "privateKey": "",
            "network": network,
            "error": str(e)
        }

def get_balance(address: str, network: str = DEFAULT_NETWORK) -> Dict[str, Any]:
    """
    Get the balance and unspent outputs for an address
    
    Args:
        address: The Bitcoin address to check
        network: The network to check the balance on (jpy or lari)
    """
    # Initialize the result with default values
    result = {
        "address": address,
        "balance": 0.0,
        "unspentOutputs": [],
        "network": network
    }
    
    try:
        # Import the address to the wallet if it's not already there
        try:
            execute_rpc("importaddress", address, "", False, network=network)
        except JSONRPCException as e:
            # Check if it's a safe mode error
            if "Safe mode" in str(e):
                result["safeMode"] = True
                result["safeModeWarning"] = str(e)
                return result
            # Re-raise other exceptions
            raise
        except Exception as e:
            # Add error information to the result
            result["error"] = str(e)
            return result
        
        # Get the unspent transaction outputs for this address
        try:
            unspent = execute_rpc("listunspent", 0, 9999999, [address], network=network)
            
            # Calculate the total balance
            total_balance = sum(float(utxo['amount']) for utxo in unspent)
            
            result["balance"] = total_balance
            result["unspentOutputs"] = unspent
            
            return result
        except JSONRPCException as e:
            # Check if it's a safe mode error
            if "Safe mode" in str(e):
                result["safeMode"] = True
                result["safeModeWarning"] = str(e)
                return result
            # Re-raise other exceptions
            raise
        except Exception as e:
            # Add error information to the result
            result["error"] = str(e)
            return result
    except Exception as e:
        # Add error information to the result
        result["error"] = str(e)
        return result

def send_transaction(from_address: str, private_key: str, to_address: str, amount: float, network: str = DEFAULT_NETWORK) -> Dict[str, Any]:
    """
    Send a transaction from one address to another
    
    Args:
        from_address: The source address
        private_key: The private key of the source address
        to_address: The destination address
        amount: The amount to send
        network: The network to send the transaction on (jpy or lari)
    """
    try:
        # Import the private key if it's not already in the wallet
        try:
            execute_rpc("importprivkey", private_key, "", False, network=network)
        except JSONRPCException as e:
            # Check if it's a safe mode error
            if "Safe mode" in str(e):
                return {
                    "fromAddress": from_address,
                    "toAddress": to_address,
                    "amount": amount,
                    "network": network,
                    "safeMode": True,
                    "safeModeWarning": str(e),
                    "error": "Transaction failed due to safe mode"
                }
            # Re-raise other exceptions
            raise
        except:
            pass  # Key might already be imported
        
        # Create and send the transaction
        txid = execute_rpc("sendtoaddress", to_address, amount, network=network)
        
        return {
            "transactionId": txid,
            "fromAddress": from_address,
            "toAddress": to_address,
            "amount": amount,
            "network": network
        }
    except JSONRPCException as e:
        # Check if it's a safe mode error
        if "Safe mode" in str(e):
            return {
                "fromAddress": from_address,
                "toAddress": to_address,
                "amount": amount,
                "network": network,
                "safeMode": True,
                "safeModeWarning": str(e),
                "error": "Transaction failed due to safe mode"
            }
        # Return a structured error response for other RPC errors
        return {
            "fromAddress": from_address,
            "toAddress": to_address,
            "amount": amount,
            "network": network,
            "error": str(e)
        }
    except Exception as e:
        # Return a structured error response for other errors
        return {
            "fromAddress": from_address,
            "toAddress": to_address,
            "amount": amount,
            "network": network,
            "error": str(e)
        }

def generate_blocks(address: str, num_blocks: int = 1, network: str = DEFAULT_NETWORK) -> Dict[str, Any]:
    """
    Generate blocks with mining rewards going to the specified address
    
    Args:
        address: The Bitcoin address to receive the mining rewards
        num_blocks: The number of blocks to generate (default: 1)
        network: The network to generate blocks on (jpy or lari)
    """
    try:
        # Generate blocks with rewards going to the specified address
        block_hashes = execute_rpc("generatetoaddress", num_blocks, address, network=network)
        
        return {
            "address": address,
            "numBlocks": num_blocks,
            "blockHashes": block_hashes,
            "network": network
        }
    except JSONRPCException as e:
        # Check if it's a safe mode error
        if "Safe mode" in str(e):
            return {
                "address": address,
                "numBlocks": num_blocks,
                "network": network,
                "safeMode": True,
                "safeModeWarning": str(e),
                "error": "Mining failed due to safe mode"
            }
        # Return a structured error response for other RPC errors
        return {
            "address": address,
            "numBlocks": num_blocks,
            "network": network,
            "error": str(e)
        }
    except Exception as e:
        # Return a structured error response for other errors
        return {
            "address": address,
            "numBlocks": num_blocks,
            "network": network,
            "error": str(e)
        }
