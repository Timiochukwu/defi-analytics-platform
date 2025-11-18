"""
Response schemas for API endpoints
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SlippageResponse(BaseModel):
    """Response schema for slippage calculation"""
    amount_out: float
    slippage_percent: float
    price_impact: float
    effective_price: float
    minimum_received: float


class PoolQualityResponse(BaseModel):
    """Response schema for pool quality scoring"""
    overall_score: float
    rating: str
    tvl_score: float
    volume_score: float
    efficiency_score: float
    balance_score: float


class RiskAssessmentResponse(BaseModel):
    """Response schema for risk assessment"""
    overall_risk_score: float
    risk_level: str
    factors: Dict[str, float]
    recommendations: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class YieldOpportunityResponse(BaseModel):
    """Response schema for yield opportunity"""
    protocol: str
    asset: str
    apy: float
    tvl_usd: float
    risk_score: float
    risk_rating: str
    yield_type: str
    liquidity_score: Optional[float] = None


class PortfolioAllocation(BaseModel):
    """Portfolio allocation item"""
    protocol: str
    asset: str
    weight_percent: float
    allocated_usd: float
    expected_apy: float
    risk_score: float


class PortfolioResponse(BaseModel):
    """Response schema for portfolio construction"""
    strategy: str
    total_capital_usd: float
    expected_apy: float
    portfolio_risk_score: float
    sharpe_ratio: Optional[float]
    allocations: List[PortfolioAllocation]
    diversification_score: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    """API health check response"""
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
