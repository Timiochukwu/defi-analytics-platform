"""
Protocol data model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ProtocolType(Enum):
    """Protocol types"""
    LENDING = "lending"
    DEX = "dex"
    YIELD_AGGREGATOR = "yield_aggregator"
    DERIVATIVES = "derivatives"
    STAKING = "staking"
    BRIDGE = "bridge"


@dataclass
class Protocol:
    """
    Represents a DeFi protocol
    """
    protocol_id: str
    name: str
    protocol_type: ProtocolType
    chain: str
    tvl_usd: float
    contract_address: str

    # Risk metrics
    audit_score: Optional[float] = None
    days_deployed: Optional[int] = None
    has_bug_bounty: bool = False

    # Metadata
    website: Optional[str] = None
    documentation: Optional[str] = None
    auditors: List[str] = None

    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.auditors is None:
            self.auditors = []
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
