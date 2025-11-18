"""
=============================================================================
DeFi ANALYTICS PLATFORM - FastAPI BACKEND
=============================================================================

PURPOSE:
REST API for DeFi analytics platform providing:
- Portfolio management endpoints
- Yield optimization
- Risk assessment
- Liquidity analysis
- Real-time data feeds

FOR MSc RESEARCH:
- Access DeFi data programmatically
- Build custom analytics on top
- Integrate with other systems
- Automated trading/rebalancing bots

AUTHOR: Built for Economics & Finance MSc students
DATE: 2024
=============================================================================
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Note: In production, uncomment these imports after modules are available
# from analytics.liquidity_analyzer import LiquidityAnalyzer
# from risk.defi_risk_models import (
#     SmartContractRiskAnalyzer,
#     LiquidationRiskAnalyzer,
#     SystemicRiskAnalyzer
# )
# from optimization.yield_optimizer import (
#     YieldOpportunityAnalyzer,
#     PortfolioOptimizer
# )
# from optimization.defi_portfolio import (
#     PortfolioConstructor,
#     PortfolioMonitor,
#     PortfolioRebalancer
# )


# ====================================================================================
# PYDANTIC MODELS (Request/Response Schemas)
# ====================================================================================

class SlippageRequest(BaseModel):
    """Request for slippage calculation"""
    reserve_in: float = Field(..., description="Reserve of input token")
    reserve_out: float = Field(..., description="Reserve of output token")
    amount_in: float = Field(..., description="Amount to trade")
    fee: float = Field(0.003, description="Pool fee (default 0.3%)")

    class Config:
        json_schema_extra = {
            "example": {
                "reserve_in": 2000000,
                "reserve_out": 1000,
                "amount_in": 10000,
                "fee": 0.003
            }
        }


class PoolQualityRequest(BaseModel):
    """Request for pool quality scoring"""
    tvl: float = Field(..., description="Total Value Locked in USD")
    volume_24h: float = Field(..., description="24h trading volume in USD")
    fee_tier: float = Field(..., description="Pool fee tier")
    reserve_ratio: float = Field(1.0, description="Reserve balance ratio")

    class Config:
        json_schema_extra = {
            "example": {
                "tvl": 100000000,
                "volume_24h": 80000000,
                "fee_tier": 0.0005,
                "reserve_ratio": 0.98
            }
        }


class SmartContractRiskRequest(BaseModel):
    """Request for smart contract risk assessment"""
    protocol_name: str
    contract_address: str
    auditors: List[str]
    code_lines: int
    days_deployed: int
    tvl_usd: float
    upgrade_mechanism: str = "Unknown"
    has_bug_bounty: bool = False
    admin_control_level: str = "Unknown"

    class Config:
        json_schema_extra = {
            "example": {
                "protocol_name": "Example Protocol",
                "contract_address": "0x1234567890abcdef",
                "auditors": ["Trail of Bits", "OpenZeppelin"],
                "code_lines": 5000,
                "days_deployed": 180,
                "tvl_usd": 50000000,
                "upgrade_mechanism": "Timelock + Multisig",
                "has_bug_bounty": True,
                "admin_control_level": "Low"
            }
        }


class LiquidationRiskRequest(BaseModel):
    """Request for liquidation risk assessment"""
    protocol_name: str
    asset: str
    collateral_value_usd: float
    debt_value_usd: float
    liquidation_threshold: Optional[float] = None
    liquidation_penalty: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "protocol_name": "Aave",
                "asset": "ETH",
                "collateral_value_usd": 100000,
                "debt_value_usd": 60000
            }
        }


class PortfolioRequest(BaseModel):
    """Request for portfolio construction"""
    capital_usd: float = Field(..., description="Capital to invest")
    strategy: str = Field(..., description="Strategy: conservative, balanced, or aggressive")
    target_apy: Optional[float] = Field(None, description="Target APY (optional)")

    class Config:
        json_schema_extra = {
            "example": {
                "capital_usd": 100000,
                "strategy": "balanced",
                "target_apy": 15.0
            }
        }


# ====================================================================================
# INITIALIZE FastAPI APP
# ====================================================================================

app = FastAPI(
    title="DeFi Analytics Platform API",
    description="""
    Comprehensive DeFi Analytics Platform for portfolio management, risk assessment,
    yield optimization, and liquidity analysis.

    ## Features

    * **Liquidity Analysis**: Calculate slippage, analyze depth, score pools
    * **Risk Assessment**: Smart contract risk, liquidation risk, systemic risk
    * **Yield Optimization**: Find best yields, optimize portfolios
    * **Portfolio Management**: Build, monitor, and rebalance DeFi portfolios

    ## For MSc Research

    This API provides programmatic access to DeFi analytics suitable for:
    - Academic research
    - Quantitative analysis
    - Trading strategy development
    - Risk management systems

    Built for Economics & Finance MSc students.
    """,
    version="1.0.0",
    contact={
        "name": "DeFi Analytics Team",
        "email": "contact@defi-analytics.com"
    },
    license_info={
        "name": "MIT License"
    }
)

# CORS middleware (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ====================================================================================
# ROOT & HEALTH CHECK ENDPOINTS
# ====================================================================================

@app.get("/", tags=["General"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "DeFi Analytics Platform API",
        "version": "1.0.0",
        "documentation": "/docs",
        "status": "operational",
        "endpoints": {
            "liquidity": "/api/liquidity/*",
            "risk": "/api/risk/*",
            "yield": "/api/yield/*",
            "portfolio": "/api/portfolio/*"
        }
    }


@app.get("/health", tags=["General"])
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "operational",
            "database": "operational",  # In production, check DB connection
            "web3": "operational"        # In production, check Web3 connection
        }
    }


# ====================================================================================
# LIQUIDITY ANALYSIS ENDPOINTS
# ====================================================================================

@app.post("/api/liquidity/slippage", tags=["Liquidity Analysis"])
async def calculate_slippage(request: SlippageRequest):
    """
    Calculate slippage for a trade using Constant Product Market Maker formula

    **Use Case**: Before executing a large trade, check expected slippage

    **Example**:
    - Pool: 1,000 ETH / 2,000,000 USDC (price = $2,000/ETH)
    - Trade: Buy 10 ETH with USDC
    - Expected slippage: ~0.5%
    """
    try:
        # In production, use actual LiquidityAnalyzer
        # analyzer = LiquidityAnalyzer()
        # result = analyzer.calculate_slippage_constant_product(...)

        # Demo calculation
        price_before = request.reserve_in / request.reserve_out
        amount_in_with_fee = request.amount_in * (1 - request.fee)
        amount_out = (request.reserve_out * amount_in_with_fee) / (request.reserve_in + amount_in_with_fee)
        execution_price = request.amount_in / amount_out if amount_out > 0 else 0
        slippage_percent = ((execution_price - price_before) / price_before * 100) if price_before > 0 else 0

        return {
            "trade_size_usd": request.amount_in,
            "expected_price": round(price_before, 4),
            "execution_price": round(execution_price, 4),
            "slippage_percent": round(slippage_percent, 3),
            "output_amount": round(amount_out, 4),
            "rating": "Excellent" if slippage_percent < 0.1 else ("Good" if slippage_percent < 0.5 else "Moderate")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/liquidity/pool-quality", tags=["Liquidity Analysis"])
async def assess_pool_quality(request: PoolQualityRequest):
    """
    Score liquidity pool quality from 0-100

    **Scoring Factors**:
    - TVL (40%): Higher is better
    - Volume/TVL ratio (30%): Higher means more activity
    - Reserve balance (20%): Closer to 50/50 is better
    - Fee appropriateness (10%): Matches pair type

    **Example**: ETH/USDC pool with $100M TVL, $80M daily volume → Score: 93/100 (A+)
    """
    try:
        # Demo scoring logic (simplified)
        import math

        # TVL score
        tvl_score = min(100, 50 + (math.log10(request.tvl) - 6) * 20) if request.tvl > 0 else 0

        # Volume ratio score
        volume_ratio = request.volume_24h / request.tvl if request.tvl > 0 else 0
        volume_score = min(100, 100 if volume_ratio > 0.5 else volume_ratio * 200)

        # Balance score
        balance_score = max(0, 100 - abs(1.0 - request.reserve_ratio) * 200)

        # Fee score
        fee_score = 100 if request.fee_tier == 0.0005 else 90

        # Overall score
        overall = (tvl_score * 0.4 + volume_score * 0.3 + balance_score * 0.2 + fee_score * 0.1)

        rating = "A+" if overall >= 90 else ("A" if overall >= 80 else ("B" if overall >= 70 else "C"))

        return {
            "overall_score": round(overall, 2),
            "rating": rating,
            "tvl_score": round(tvl_score, 2),
            "volume_score": round(volume_score, 2),
            "balance_score": round(balance_score, 2),
            "fee_score": round(fee_score, 2),
            "volume_to_tvl_ratio": round(volume_ratio, 4)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ====================================================================================
# RISK ASSESSMENT ENDPOINTS
# ====================================================================================

@app.post("/api/risk/smart-contract", tags=["Risk Assessment"])
async def assess_smart_contract_risk(request: SmartContractRiskRequest):
    """
    Assess smart contract security risk

    **Risk Factors**:
    1. Audit quality (30%)
    2. Code complexity (20%)
    3. Time deployed (20%)
    4. TVL at risk (15%)
    5. Admin keys (15%)

    **Example**: Aave (3 audits, 900 days deployed, $5B TVL) → Risk: 18/100 (Very Low)
    """
    try:
        # Demo risk calculation (simplified)
        audit_score = min(100, 30 + len(request.auditors) * 25)
        if request.has_bug_bounty:
            audit_score += 10

        complexity_score = min(100, request.code_lines / 100)
        time_score = min(100, 10 + request.days_deployed / 10)

        # Overall risk (higher = riskier)
        overall_risk = (
            (100 - audit_score) * 0.30 +
            complexity_score * 0.20 +
            (100 - time_score) * 0.20 +
            40 * 0.15 +  # TVL risk (simplified)
            30 * 0.15    # Admin risk (simplified)
        )

        risk_level = "Very Low" if overall_risk < 20 else ("Low" if overall_risk < 40 else "Moderate")

        return {
            "protocol_name": request.protocol_name,
            "overall_risk_score": round(overall_risk, 2),
            "risk_level": risk_level,
            "audit_score": round(audit_score, 2),
            "code_complexity": round(complexity_score, 2),
            "time_score": round(time_score, 2),
            "number_of_audits": len(request.auditors),
            "days_deployed": request.days_deployed,
            "recommendation": "Safe to use" if overall_risk < 40 else "Use with caution"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/risk/liquidation", tags=["Risk Assessment"])
async def assess_liquidation_risk(request: LiquidationRiskRequest):
    """
    Assess liquidation risk for lending position

    **Health Factor**:
    - HF > 1.5: Safe
    - HF = 1.2-1.5: Moderate risk
    - HF < 1.2: High risk
    - HF < 1.0: Liquidatable!

    **Example**: $100k ETH collateral, $60k debt, 86% threshold → HF = 1.43 (Moderate)
    """
    try:
        # Use protocol defaults if not provided
        liq_threshold = request.liquidation_threshold or 0.86
        liq_penalty = request.liquidation_penalty or 0.05

        # Calculate health factor
        health_factor = (
            (request.collateral_value_usd * liq_threshold) / request.debt_value_usd
            if request.debt_value_usd > 0 else float('inf')
        )

        # Current LTV
        current_ltv = request.debt_value_usd / request.collateral_value_usd if request.collateral_value_usd > 0 else 0

        # Distance to liquidation
        if health_factor != float('inf'):
            distance = ((health_factor - 1.0) / health_factor) * 100
        else:
            distance = 100.0

        # Risk level
        if health_factor >= 1.5:
            risk_level = "Low"
        elif health_factor >= 1.2:
            risk_level = "Moderate"
        elif health_factor >= 1.0:
            risk_level = "High"
        else:
            risk_level = "Critical"

        return {
            "protocol": request.protocol_name,
            "asset": request.asset,
            "health_factor": round(health_factor, 3),
            "current_ltv": round(current_ltv * 100, 2),
            "liquidation_threshold": liq_threshold,
            "distance_to_liquidation_percent": round(distance, 2),
            "liquidation_penalty_percent": liq_penalty * 100,
            "risk_level": risk_level,
            "recommendation": "Add collateral" if health_factor < 1.5 else "Position is safe"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ====================================================================================
# YIELD OPTIMIZATION ENDPOINTS
# ====================================================================================

@app.get("/api/yield/opportunities", tags=["Yield Optimization"])
async def get_yield_opportunities(
    min_apy: float = Query(0, description="Minimum APY %"),
    max_risk: int = Query(5, description="Maximum risk level (1-5)"),
    min_tvl: float = Query(1000000, description="Minimum TVL in USD")
):
    """
    Get current yield opportunities across DeFi protocols

    **Filters**:
    - min_apy: Minimum acceptable APY
    - max_risk: Maximum risk tolerance (1=Very Low, 5=Very High)
    - min_tvl: Minimum Total Value Locked

    **Returns**: List of opportunities ranked by risk-adjusted returns
    """
    try:
        # Demo opportunities (in production, fetch from protocols)
        opportunities = [
            {
                "protocol": "Aave",
                "pool": "USDC Lending",
                "asset": "USDC",
                "apy": 3.5,
                "tvl_millions": 2000,
                "risk_level": 1,
                "risk_rating": "Very Low",
                "yield_type": "Lending",
                "lock_days": 0
            },
            {
                "protocol": "Curve",
                "pool": "3pool",
                "asset": "USDC/USDT/DAI",
                "apy": 8.0,
                "tvl_millions": 1500,
                "risk_level": 2,
                "risk_rating": "Low",
                "yield_type": "LP",
                "lock_days": 0
            },
            {
                "protocol": "Uniswap V3",
                "pool": "ETH/USDC 0.05%",
                "asset": "ETH/USDC",
                "apy": 25.0,
                "tvl_millions": 800,
                "risk_level": 3,
                "risk_rating": "Moderate",
                "yield_type": "LP",
                "lock_days": 0,
                "il_risk": "Moderate"
            }
        ]

        # Filter
        filtered = [
            opp for opp in opportunities
            if opp['apy'] >= min_apy
            and opp['risk_level'] <= max_risk
            and opp['tvl_millions'] * 1_000_000 >= min_tvl
        ]

        return {
            "count": len(filtered),
            "opportunities": filtered,
            "filters_applied": {
                "min_apy": min_apy,
                "max_risk": max_risk,
                "min_tvl": min_tvl
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ====================================================================================
# PORTFOLIO MANAGEMENT ENDPOINTS
# ====================================================================================

@app.post("/api/portfolio/build", tags=["Portfolio Management"])
async def build_portfolio(request: PortfolioRequest):
    """
    Build optimal DeFi portfolio based on strategy

    **Strategies**:
    - **Conservative**: Stablecoins, blue-chip protocols, 2-8% APY
    - **Balanced**: Mix of stable and volatile, 10-20% APY
    - **Aggressive**: High yield focus, 30-50% APY, higher risk

    **Example**: $100k balanced → 30% Aave, 25% Curve, 25% Uniswap LP, 15% ETH staking, 5% Yearn
    """
    try:
        capital = request.capital_usd
        strategy = request.strategy.lower()

        if strategy == "conservative":
            allocations = [
                {"protocol": "Aave", "pool": "USDC", "percent": 40, "apy": 3.5, "amount": capital * 0.40},
                {"protocol": "Compound", "pool": "USDC", "percent": 25, "apy": 3.2, "amount": capital * 0.25},
                {"protocol": "Curve", "pool": "3pool", "percent": 25, "apy": 5.0, "amount": capital * 0.25},
                {"protocol": "Yearn", "pool": "USDC Vault", "percent": 10, "apy": 6.0, "amount": capital * 0.10}
            ]
            expected_apy = 4.1
            risk_score = 18.5

        elif strategy == "balanced":
            allocations = [
                {"protocol": "Aave", "pool": "USDC", "percent": 30, "apy": 3.5, "amount": capital * 0.30},
                {"protocol": "Curve", "pool": "3pool", "percent": 25, "apy": 8.0, "amount": capital * 0.25},
                {"protocol": "Uniswap V3", "pool": "ETH/USDC", "percent": 25, "apy": 18.0, "amount": capital * 0.25},
                {"protocol": "Lido", "pool": "ETH Staking", "percent": 15, "apy": 4.5, "amount": capital * 0.15},
                {"protocol": "Yearn", "pool": "USDC Vault", "percent": 5, "apy": 12.0, "amount": capital * 0.05}
            ]
            expected_apy = 9.5
            risk_score = 28.5

        elif strategy == "aggressive":
            allocations = [
                {"protocol": "Curve", "pool": "3pool", "percent": 15, "apy": 8.0, "amount": capital * 0.15},
                {"protocol": "Uniswap V3", "pool": "ETH/USDC", "percent": 30, "apy": 35.0, "amount": capital * 0.30},
                {"protocol": "GMX", "pool": "GLP", "percent": 25, "apy": 42.0, "amount": capital * 0.25},
                {"protocol": "Convex", "pool": "cvxCRV", "percent": 20, "apy": 50.0, "amount": capital * 0.20},
                {"protocol": "Stargate", "pool": "USDC", "percent": 10, "apy": 25.0, "amount": capital * 0.10}
            ]
            expected_apy = 35.7
            risk_score = 48.5
        else:
            raise HTTPException(status_code=400, detail="Strategy must be: conservative, balanced, or aggressive")

        return {
            "strategy": strategy.capitalize(),
            "total_capital": capital,
            "expected_apy": expected_apy,
            "risk_score": risk_score,
            "allocations": allocations,
            "diversification": len(allocations)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/portfolio/performance", tags=["Portfolio Management"])
async def get_portfolio_performance(
    portfolio_id: str = Query(..., description="Portfolio ID")
):
    """
    Get portfolio performance metrics

    **Metrics**:
    - Total value
    - P&L (absolute and %)
    - Current APY
    - Sharpe ratio
    - Max drawdown
    - Risk score
    """
    try:
        # Demo performance data
        return {
            "portfolio_id": portfolio_id,
            "total_value_usd": 105750,
            "initial_value_usd": 100000,
            "total_pnl_usd": 5750,
            "total_pnl_percent": 5.75,
            "current_apy": 12.5,
            "sharpe_ratio": 1.8,
            "max_drawdown_percent": 7.5,
            "risk_score": 28.5,
            "num_positions": 5,
            "health_status": "Healthy",
            "last_updated": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ====================================================================================
# RUN APPLICATION
# ====================================================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 80)
    print("DeFi ANALYTICS PLATFORM API")
    print("=" * 80)
    print("\nStarting server...")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative docs: http://localhost:8000/redoc")
    print("\nPress CTRL+C to stop\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
