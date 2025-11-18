"""
Portfolio data model
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class PortfolioStrategy(Enum):
    """Portfolio strategy types"""
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"
    CUSTOM = "custom"


@dataclass
class Portfolio:
    """
    Represents a DeFi portfolio
    """
    portfolio_id: str
    user_id: str
    name: str
    strategy: PortfolioStrategy

    # Capital
    initial_capital_usd: float
    current_value_usd: float

    # Performance metrics
    total_deposited_usd: float = 0.0
    total_withdrawn_usd: float = 0.0
    realized_profit_usd: float = 0.0
    unrealized_profit_usd: float = 0.0

    # Risk metrics
    risk_score: Optional[float] = None
    max_drawdown_percent: Optional[float] = None
    sharpe_ratio: Optional[float] = None

    # Positions
    position_ids: List[str] = field(default_factory=list)

    # Timestamps
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    @property
    def total_profit_usd(self) -> float:
        """Total profit (realized + unrealized)"""
        return self.realized_profit_usd + self.unrealized_profit_usd

    @property
    def roi_percent(self) -> float:
        """Return on investment percentage"""
        if self.initial_capital_usd == 0:
            return 0.0
        return (self.total_profit_usd / self.initial_capital_usd) * 100

    @property
    def net_deposits_usd(self) -> float:
        """Net deposits (deposits - withdrawals)"""
        return self.total_deposited_usd - self.total_withdrawn_usd
