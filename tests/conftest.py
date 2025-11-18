"""
Pytest configuration and fixtures
"""
import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_pool_data():
    """Sample liquidity pool data for testing"""
    return {
        "reserve_in": 2_000_000,
        "reserve_out": 1_000,
        "tvl": 100_000_000,
        "volume_24h": 80_000_000,
        "fee_tier": 0.003,
    }


@pytest.fixture
def sample_protocol_data():
    """Sample protocol data for testing"""
    return {
        "protocol_name": "Aave",
        "contract_address": "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",
        "auditors": ["Trail of Bits", "OpenZeppelin", "ConsenSys Diligence"],
        "code_lines": 15000,
        "days_deployed": 900,
        "tvl_usd": 5_000_000_000,
    }


@pytest.fixture
def sample_yield_opportunity():
    """Sample yield opportunity for testing"""
    return {
        "protocol": "Aave",
        "asset": "USDC",
        "apy": 8.5,
        "tvl": 1_200_000,
        "risk_score": 18.2,
    }
