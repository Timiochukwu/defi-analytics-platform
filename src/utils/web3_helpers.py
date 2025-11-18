"""
Web3 helper functions
"""
from typing import Optional
from web3 import Web3
from eth_utils import is_address, to_checksum_address
import os


def get_web3_provider(rpc_url: Optional[str] = None) -> Web3:
    """
    Get Web3 provider instance

    Args:
        rpc_url: RPC endpoint URL (defaults to env variable)

    Returns:
        Web3 instance
    """
    if rpc_url is None:
        rpc_url = os.getenv("ETHEREUM_RPC_URL", "http://localhost:8545")

    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_connected():
        raise ConnectionError(f"Failed to connect to Web3 provider: {rpc_url}")

    return w3


def validate_address(address: str) -> bool:
    """
    Validate Ethereum address

    Args:
        address: Ethereum address to validate

    Returns:
        True if valid, False otherwise
    """
    return is_address(address)


def to_checksum(address: str) -> str:
    """
    Convert address to checksum format

    Args:
        address: Ethereum address

    Returns:
        Checksummed address
    """
    if not validate_address(address):
        raise ValueError(f"Invalid Ethereum address: {address}")

    return to_checksum_address(address)


def wei_to_ether(wei: int) -> float:
    """
    Convert Wei to Ether

    Args:
        wei: Amount in Wei

    Returns:
        Amount in Ether
    """
    return Web3.from_wei(wei, 'ether')


def ether_to_wei(ether: float) -> int:
    """
    Convert Ether to Wei

    Args:
        ether: Amount in Ether

    Returns:
        Amount in Wei
    """
    return Web3.to_wei(ether, 'ether')
