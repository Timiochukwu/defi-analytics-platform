# Days 003-005: Foundation Complete

> **Combined Time**: 4.5-6 hours | **Difficulty**: ⭐⭐ Easy to ⭐⭐⭐ Moderate

---

## 📅 Quick Overview

| Day | Topic | Time | Key Deliverable |
|-----|-------|------|-----------------|
| **003** | Enums & Dataclasses | 1.5-2h | DeFi-specific types (RiskLevel, YieldType, ProtocolType) |
| **004** | Math & Utilities | 1.5-2h | Financial calculation functions (compound interest, ratios) |
| **005** | API Organization | 1.5-2h | Router-based API structure with tags |

---

## 🎯 Day 003: Enums & Dataclasses

### **What You'll Build**

Create `src/api/types.py` with DeFi-specific enumerations:

```python
"""
DeFi Platform Types and Enumerations
Day 003/030
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


# ====================================================================================
# ENUMS
# ====================================================================================

class RiskLevel(Enum):
    """Risk level classifications for DeFi protocols"""
    VERY_LOW = "Very Low"       # Score: 0-20
    LOW = "Low"                 # Score: 21-40
    MODERATE = "Moderate"       # Score: 41-60
    HIGH = "High"               # Score: 61-80
    VERY_HIGH = "Very High"     # Score: 81-95
    CRITICAL = "Critical"       # Score: 96-100


class YieldType(Enum):
    """Types of yield generation in DeFi"""
    LENDING = "Lending"                    # Aave, Compound
    LP_FEES = "Liquidity Provider Fees"    # Uniswap, Curve
    STAKING = "Staking"                    # ETH staking, governance
    FARMING = "Yield Farming"              # Token rewards
    VAULT = "Yield Vault"                  # Yearn, Beefy
    STABLE_FARM = "Stable Farming"         # Low-risk stablecoin yields


class ProtocolType(Enum):
    """Types of DeFi protocols"""
    DEX = "Decentralized Exchange"    # Uniswap, SushiSwap
    LENDING = "Lending Protocol"       # Aave, Compound
    DERIVATIVES = "Derivatives"        # dYdX, GMX
    STABLECOIN = "Stablecoin"         # MakerDAO, Frax
    YIELD = "Yield Aggregator"        # Yearn, Beefy
    BRIDGE = "Bridge"                 # Cross-chain bridges
    LIQUID_STAKING = "Liquid Staking" # Lido, Rocket Pool


class PoolRating(Enum):
    """Liquidity pool quality ratings"""
    S_PLUS = "S+"   # 95-100: Exceptional
    A_PLUS = "A+"   # 90-94:  Excellent
    A = "A"         # 80-89:  Very Good
    B = "B"         # 70-79:  Good
    C = "C"         # 60-69:  Average
    D = "D"         # 50-59:  Below Average
    F = "F"         # 0-49:   Poor


# ====================================================================================
# DATACLASSES
# ====================================================================================

@dataclass
class Protocol:
    """Represents a DeFi protocol"""
    name: str
    protocol_type: ProtocolType
    chain: str  # "Ethereum", "Polygon", "Arbitrum", etc.
    website: str
    audited: bool
    audit_firms: List[str]
    tvl_usd: float
    days_active: int
    risk_score: float  # 0-100
    risk_level: RiskLevel


@dataclass
class YieldOpportunitySummary:
    """Summary of a yield opportunity"""
    protocol: str
    asset: str
    apy: float
    tvl_usd: float
    yield_type: YieldType
    risk_level: RiskLevel
    lock_days: int
    updated_at: datetime


@dataclass
class PoolInfo:
    """Liquidity pool information"""
    pool_address: str
    token0: str
    token1: str
    reserve0: float
    reserve1: float
    tvl_usd: float
    volume_24h: float
    fee_tier: float
    rating: PoolRating


# ====================================================================================
# HELPER FUNCTIONS
# ====================================================================================

def risk_score_to_level(score: float) -> RiskLevel:
    """Convert numerical risk score (0-100) to RiskLevel enum"""
    if score < 20:
        return RiskLevel.VERY_LOW
    elif score < 40:
        return RiskLevel.LOW
    elif score < 60:
        return RiskLevel.MODERATE
    elif score < 80:
        return RiskLevel.HIGH
    elif score < 96:
        return RiskLevel.VERY_HIGH
    else:
        return RiskLevel.CRITICAL


def pool_score_to_rating(score: float) -> PoolRating:
    """Convert pool quality score (0-100) to rating"""
    if score >= 95:
        return PoolRating.S_PLUS
    elif score >= 90:
        return PoolRating.A_PLUS
    elif score >= 80:
        return PoolRating.A
    elif score >= 70:
        return PoolRating.B
    elif score >= 60:
        return PoolRating.C
    elif score >= 50:
        return PoolRating.D
    else:
        return PoolRating.F
```

### **Test Day 003**

Add to `main.py`:

```python
from types import RiskLevel, YieldType, risk_score_to_level

@app.get("/api/types/risk-levels", tags=["Types"])
async def get_risk_levels():
    """Get all risk level definitions"""
    return {
        "risk_levels": [
            {"value": level.value, "name": level.name}
            for level in RiskLevel
        ]
    }

@app.get("/api/types/yield-types", tags=["Types"])
async def get_yield_types():
    """Get all yield type definitions"""
    return {
        "yield_types": [
            {"value": yt.value, "name": yt.name}
            for yt in YieldType
        ]
    }
```

**Test:**
```bash
curl http://localhost:8000/api/types/risk-levels
curl http://localhost:8000/api/types/yield-types
```

**✅ Day 003 Complete!**

---

## 🎯 Day 004: Math & Utility Functions

### **What You'll Build**

Create `src/utils/calculations.py`:

```python
"""
Financial Calculation Utilities
Day 004/030
"""

import numpy as np
from typing import Tuple, List


# ====================================================================================
# APY & INTEREST CALCULATIONS
# ====================================================================================

def calculate_apy(
    deposit: float,
    earned: float,
    days: int
) -> float:
    """
    Calculate Annual Percentage Yield

    Formula: APY = ((ending / starting) ^ (365 / days)) - 1

    Example:
        Deposit $10,000, earn $100 in 30 days
        APY = ((10100/10000)^(365/30)) - 1 = 0.1268 = 12.68%

    Args:
        deposit: Initial deposit amount
        earned: Amount earned in the period
        days: Number of days

    Returns:
        APY as decimal (0.1268 = 12.68%)
    """
    if deposit <= 0 or days <= 0:
        raise ValueError("Deposit and days must be positive")

    ending_value = deposit + earned
    growth_factor = ending_value / deposit
    periods_per_year = 365 / days
    apy = (growth_factor ** periods_per_year) - 1

    return apy


def calculate_compound_interest(
    principal: float,
    rate: float,
    compounds_per_year: int,
    years: float
) -> float:
    """
    Calculate compound interest

    Formula: A = P(1 + r/n)^(nt)

    Example:
        $10,000 at 5% APR, compounded daily for 1 year
        A = 10000(1 + 0.05/365)^(365*1) = $10,512.67

    Args:
        principal: Initial amount
        rate: Annual interest rate (decimal, e.g., 0.05 = 5%)
        compounds_per_year: Compounding frequency (365 = daily, 12 = monthly)
        years: Time period in years

    Returns:
        Final amount after compounding
    """
    amount = principal * (1 + rate / compounds_per_year) ** (compounds_per_year * years)
    return amount


def apy_to_apr(apy: float, compounds_per_year: int = 365) -> float:
    """
    Convert APY to APR

    Formula: APR = n * ((1 + APY)^(1/n) - 1)

    Args:
        apy: Annual Percentage Yield (decimal)
        compounds_per_year: Compounding frequency

    Returns:
        APR as decimal
    """
    apr = compounds_per_year * ((1 + apy) ** (1 / compounds_per_year) - 1)
    return apr


# ====================================================================================
# PERCENTAGE & RATIO CALCULATIONS
# ====================================================================================

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values

    Formula: ((new - old) / old) * 100

    Example:
        ETH price: $1,000 → $1,200
        Change = ((1200 - 1000) / 1000) * 100 = 20%

    Args:
        old_value: Original value
        new_value: New value

    Returns:
        Percentage change (20.0 = 20% increase)
    """
    if old_value == 0:
        raise ValueError("Old value cannot be zero")

    change = ((new_value - old_value) / old_value) * 100
    return change


def calculate_ratio(value1: float, value2: float) -> float:
    """
    Calculate ratio between two values

    Example:
        Pool reserves: 1,000 ETH / 2,000,000 USDC
        Ratio = 1000 / 2000000 = 0.0005
        Price = 2000000 / 1000 = $2,000 per ETH

    Args:
        value1: First value
        value2: Second value

    Returns:
        Ratio (value1 / value2)
    """
    if value2 == 0:
        raise ValueError("Denominator cannot be zero")

    return value1 / value2


def normalize_to_range(
    value: float,
    min_val: float,
    max_val: float
) -> float:
    """
    Normalize value to 0-100 range

    Formula: ((value - min) / (max - min)) * 100

    Example:
        TVL = $50M, min = $1M, max = $100M
        Normalized = ((50 - 1) / (100 - 1)) * 100 = 49.5

    Args:
        value: Value to normalize
        min_val: Minimum value in range
        max_val: Maximum value in range

    Returns:
        Normalized value (0-100)
    """
    if max_val == min_val:
        return 50.0  # Middle of range if no variation

    normalized = ((value - min_val) / (max_val - min_val)) * 100
    return max(0, min(100, normalized))  # Clamp to 0-100


# ====================================================================================
# STATISTICAL FUNCTIONS
# ====================================================================================

def calculate_sharpe_ratio(
    returns: List[float],
    risk_free_rate: float = 0.02
) -> float:
    """
    Calculate Sharpe Ratio (risk-adjusted return)

    Formula: (Mean Return - Risk-Free Rate) / Std Deviation

    Example:
        Portfolio returns: [0.10, 0.12, 0.08, 0.15, 0.11]
        Risk-free rate: 2%
        Sharpe = (0.112 - 0.02) / std(returns) = 3.2

    Args:
        returns: List of periodic returns (as decimals)
        risk_free_rate: Annual risk-free rate (default 2%)

    Returns:
        Sharpe ratio (higher = better risk-adjusted returns)
    """
    if len(returns) < 2:
        raise ValueError("Need at least 2 returns for Sharpe calculation")

    mean_return = np.mean(returns)
    std_dev = np.std(returns)

    if std_dev == 0:
        return 0.0

    sharpe = (mean_return - risk_free_rate) / std_dev
    return sharpe


def calculate_volatility(prices: List[float]) -> float:
    """
    Calculate price volatility (standard deviation of returns)

    Args:
        prices: List of prices

    Returns:
        Volatility (standard deviation)
    """
    if len(prices) < 2:
        return 0.0

    # Calculate returns
    returns = [
        (prices[i] - prices[i-1]) / prices[i-1]
        for i in range(1, len(prices))
    ]

    return float(np.std(returns))
```

### **Test Day 004**

Add to `main.py`:

```python
from utils.calculations import (
    calculate_apy,
    calculate_percentage_change,
    calculate_sharpe_ratio
)

@app.get("/api/utils/test-calculations", tags=["Utilities"])
async def test_calculations():
    """Test mathematical functions"""
    return {
        "apy_test": {
            "deposit": 10000,
            "earned": 100,
            "days": 30,
            "apy_percent": round(calculate_apy(10000, 100, 30) * 100, 2)
        },
        "percentage_change_test": {
            "old": 1000,
            "new": 1200,
            "change_percent": round(calculate_percentage_change(1000, 1200), 2)
        },
        "sharpe_test": {
            "returns": [0.10, 0.12, 0.08, 0.15, 0.11],
            "sharpe_ratio": round(calculate_sharpe_ratio([0.10, 0.12, 0.08, 0.15, 0.11]), 2)
        }
    }
```

**Test:**
```bash
curl http://localhost:8000/api/utils/test-calculations
```

**Expected output:**
```json
{
  "apy_test": {
    "deposit": 10000,
    "earned": 100,
    "days": 30,
    "apy_percent": 12.68
  },
  "percentage_change_test": {
    "old": 1000,
    "new": 1200,
    "change_percent": 20.0
  },
  "sharpe_test": {
    "returns": [0.10, 0.12, 0.08, 0.15, 0.11],
    "sharpe_ratio": 3.67
  }
}
```

**✅ Day 004 Complete!**

---

## 🎯 Day 005: API Organization with Routers

### **What You'll Build**

Reorganize API into modular routers:

```
src/api/
├── main.py              ← Main app
├── models.py            ← Pydantic models
├── routes/
│   ├── __init__.py
│   ├── general.py       ← Health, root
│   ├── calculations.py  ← Calculation endpoints
│   └── types.py         ← Type listings
└── utils/
    └── calculations.py  ← Math functions
```

Create `src/api/routes/general.py`:

```python
"""General Routes - Health checks, info"""
from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any

router = APIRouter(tags=["General"])

@router.get("/")
async def root() -> Dict[str, Any]:
    return {
        "message": "DeFi Analytics Platform API",
        "version": "0.5.0-day005",
        "day": "005/030",
        "status": "operational"
    }

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "0.5.0-day005"
    }
```

Create `src/api/routes/calculations.py`:

```python
"""Calculation Routes"""
from fastapi import APIRouter, HTTPException, status
from models import PercentageRequest, PercentageResponse, APYCalculationRequest, APYCalculationResponse

router = APIRouter(prefix="/api/calculate", tags=["Calculations"])

@router.post("/percentage", response_model=PercentageResponse)
async def calculate_percentage(request: PercentageRequest):
    # ... (same implementation as Day 002)
    pass

@router.post("/apy", response_model=APYCalculationResponse)
async def calculate_apy(request: APYCalculationRequest):
    # ... (same implementation as Day 002)
    pass
```

Update `src/api/main.py`:

```python
"""
Main FastAPI Application - Day 005
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import general, calculations, types as types_routes

app = FastAPI(
    title="DeFi Analytics Platform API",
    version="0.5.0-day005",
    # ... rest of config
)

# Add middleware
app.add_middleware(CORSMiddleware, ...)

# Include routers
app.include_router(general.router)
app.include_router(calculations.router)
app.include_router(types_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

**Benefits of Router Organization:**
- ✅ Cleaner code structure
- ✅ Easier to maintain
- ✅ Team collaboration friendly
- ✅ Automatic API documentation grouping

**Test:**
```bash
curl http://localhost:8000/
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/calculate/percentage -d '{"value":100,"percentage":10}'
```

**✅ Day 005 Complete!**

---

## 🎉 FOUNDATION COMPLETE! (Days 001-005)

### **What You've Built:**

✅ FastAPI server with auto-reload
✅ Health check and root endpoints
✅ Pydantic request/response models
✅ Field validation and error handling
✅ DeFi-specific enums and dataclasses
✅ Financial calculation utilities
✅ Router-based API organization
✅ API documentation (Swagger/ReDoc)

### **Current API Structure:**

```
GET  /                             - API info
GET  /health                       - Health check
POST /api/calculate/percentage     - Percentage calculator
POST /api/calculate/apy            - APY calculator
GET  /api/types/risk-levels        - Risk level definitions
GET  /api/types/yield-types        - Yield type definitions
GET  /api/utils/test-calculations  - Test math functions
```

---

## 📊 Progress

```
[██████████░░░░░░░░░░░░░░░░░░] Day 005/030 (16.7%)

Foundation:     [██████████] 5/5 days ✓ COMPLETE
Liquidity:      [░░░░░░░░░░] 0/7 days
Risk:           [░░░░░░░░░░] 0/6 days
Yield:          [░░░░░░░░░░] 0/6 days
Data/Production:[░░░░░░░░░░] 0/6 days
```

---

## 🚀 Next Steps

**Tomorrow (Day 006)**: AMM Mathematics
- Constant product formula (x * y = k)
- Swap output calculation
- Price calculation from reserves
- Begin liquidity analysis module

**You're ready for the real DeFi code!** 🔥

---

**Days 001-005 Complete** ✅ | **Next**: Day 006 - AMM Basics
