"""
Position data model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class PositionType(Enum):
    """Position types"""
    LENDING = "lending"
    LIQUIDITY_POOL = "liquidity_pool"
    STAKING = "staking"
    FARMING = "farming"


class PositionStatus(Enum):
    """Position status"""
    ACTIVE = "active"
    CLOSED = "closed"
    LIQUIDATED = "liquidated"


@dataclass
class Position:
    """
    Represents a DeFi position
    """
    position_id: str
    portfolio_id: str
    protocol_name: str
    position_type: PositionType
    status: PositionStatus

    # Position details
    asset_symbol: str
    amount: float
    value_usd: float
    entry_price: float
    current_price: float

    # Performance metrics
    current_apy: Optional[float] = None
    realized_profit_usd: Optional[float] = 0.0
    unrealized_profit_usd: Optional[float] = 0.0

    # Risk metrics
    health_factor: Optional[float] = None
    liquidation_price: Optional[float] = None

    # Timestamps
    opened_at: datetime = None
    closed_at: Optional[datetime] = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.opened_at is None:
            self.opened_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    @property
    def pnl_percent(self) -> float:
        """Calculate profit/loss percentage"""
        if self.entry_price == 0:
            return 0.0
        return ((self.current_price - self.entry_price) / self.entry_price) * 100

    @property
    def total_profit_usd(self) -> float:
        """Total profit (realized + unrealized)"""
        return (self.realized_profit_usd or 0.0) + (self.unrealized_profit_usd or 0.0)
