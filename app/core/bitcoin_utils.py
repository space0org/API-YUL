from app.core.bitcoin_rpc import execute_rpc
from fastapi import HTTPException
from typing import Dict, List, Any, Optional

def generate_keypair() -> Dict[str, str]:
    """
    Generate a new Bitcoin address and private key
    """
    try:
        # Generate a new address
        address = execute_rpc("getnewaddress")
        
        # Get the private key for this address
        private_key = execute_rpc("dumpprivkey", address)
        
        return {
            "address": address,
            "privateKey": private_key
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate key pair: {str(e)}")

def get_balance(address: str) -> Dict[str, Any]:
    """
    Get the balance and unspent outputs for an address
    """
    try:
        # Import the address to the wallet if it's not already there
        try:
            execute_rpc("importaddress", address, "", False)
        except:
            pass  # Address might already be imported
        
        # Get the unspent transaction outputs for this address
        unspent = execute_rpc("listunspent", 0, 9999999, [address])
        
        # Calculate the total balance
        total_balance = sum(float(utxo['amount']) for utxo in unspent)
        
        return {
            "address": address,
            "balance": total_balance,
            "unspentOutputs": unspent
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get balance: {str(e)}")

def send_transaction(from_address: str, private_key: str, to_address: str, amount: float) -> Dict[str, Any]:
    """
    Send a transaction from one address to another
    """
    try:
        # Import the private key if it's not already in the wallet
        try:
            execute_rpc("importprivkey", private_key, "", False)
        except:
            pass  # Key might already be imported
        
        # Create and send the transaction
        txid = execute_rpc("sendtoaddress", to_address, amount)
        
        return {
            "transactionId": txid,
            "fromAddress": from_address,
            "toAddress": to_address,
            "amount": amount
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send transaction: {str(e)}")
