"""
Request schemas for API endpoints
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum


class StrategyType(str, Enum):
    """Portfolio strategy types"""
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"


class SlippageRequest(BaseModel):
    """Request schema for slippage calculation"""
    reserve_in: float = Field(..., gt=0, description="Input token reserve")
    reserve_out: float = Field(..., gt=0, description="Output token reserve")
    amount_in: float = Field(..., gt=0, description="Amount to swap")
    fee: float = Field(0.003, ge=0, le=1, description="Pool fee (0.003 = 0.3%)")


class PoolQualityRequest(BaseModel):
    """Request schema for pool quality scoring"""
    tvl: float = Field(..., gt=0, description="Total Value Locked")
    volume_24h: float = Field(..., ge=0, description="24-hour trading volume")
    fee_tier: float = Field(..., ge=0, le=1, description="Fee tier")
    reserve_ratio: float = Field(..., gt=0, le=1, description="Reserve balance ratio")


class SmartContractRiskRequest(BaseModel):
    """Request schema for smart contract risk assessment"""
    protocol_name: str = Field(..., min_length=1)
    contract_address: Optional[str] = None
    auditors: List[str] = Field(default_factory=list)
    code_lines: int = Field(..., gt=0)
    days_deployed: int = Field(..., ge=0)
    tvl_usd: float = Field(..., ge=0)
    upgrade_mechanism: str = Field(...)
    has_bug_bounty: bool = Field(default=False)
    admin_control_level: str = Field(...)


class LiquidationRiskRequest(BaseModel):
    """Request schema for liquidation risk assessment"""
    protocol_name: str = Field(..., min_length=1)
    asset: str = Field(..., min_length=1)
    collateral_value_usd: float = Field(..., gt=0)
    debt_value_usd: float = Field(..., ge=0)

    @validator('debt_value_usd')
    def debt_less_than_collateral(cls, v, values):
        if 'collateral_value_usd' in values and v > values['collateral_value_usd']:
            raise ValueError('Debt cannot exceed collateral value')
        return v


class PortfolioRequest(BaseModel):
    """Request schema for portfolio construction"""
    capital_usd: float = Field(..., gt=0, description="Capital to allocate")
    strategy: StrategyType = Field(..., description="Portfolio strategy")
    target_apy: Optional[float] = Field(None, ge=0, le=200, description="Target APY %")
    min_yield_percent: Optional[float] = Field(None, ge=0, description="Minimum yield %")
    max_risk_score: Optional[float] = Field(None, ge=0, le=100, description="Max risk score")
