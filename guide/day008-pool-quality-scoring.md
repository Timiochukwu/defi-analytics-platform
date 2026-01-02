# Day 008: Pool Quality Scoring System

**Focus**: Building a comprehensive pool quality scoring system with TVL analysis, volume metrics, reserve balance scoring, and overall 0-100 pool ratings.

**Time Estimate**: 2.5 hours
**Difficulty**: Intermediate
**Prerequisites**: Days 001-007 complete

---

## Table of Contents

1. [Learning Objectives](#learning-objectives)
2. [What We're Building Today](#what-were-building-today)
3. [Theory: Pool Quality Metrics](#theory-pool-quality-metrics)
4. [Implementation](#implementation)
5. [Testing with curl](#testing-with-curl)
6. [Common Issues](#common-issues)
7. [Key Takeaways](#key-takeaways)

---

## Learning Objectives

By the end of Day 008, you will:

- ✅ Understand how to calculate Total Value Locked (TVL)
- ✅ Implement Volume/TVL ratio analysis for liquidity efficiency
- ✅ Build a reserve balance scorer (pool symmetry analysis)
- ✅ Create a liquidity depth metric
- ✅ Develop a comprehensive 0-100 pool quality rating system
- ✅ Compare and rank multiple pools
- ✅ Understand what makes a "good" DeFi liquidity pool

---

## What We're Building Today

### Real-World Problem

Not all liquidity pools are created equal. A pool with $10M TVL might be worse than a pool with $1M TVL if:
- The reserves are severely imbalanced (e.g., 99% one token, 1% other)
- The trading volume is low relative to TVL (inefficient capital)
- The liquidity depth is shallow (high slippage)
- The fee tier doesn't match the volatility

**Today's Goal**: Build a scoring system to objectively rate pool quality from 0-100.

### Key Metrics We'll Implement

1. **TVL (Total Value Locked)**: Total dollar value in the pool
2. **Volume/TVL Ratio**: How efficiently is the liquidity being used?
3. **Reserve Balance Score**: How symmetric are the reserves?
4. **Liquidity Depth**: Can the pool handle large trades?
5. **Fee Efficiency**: Is the fee tier appropriate for volatility?
6. **Overall Quality Score**: Composite 0-100 rating

---

## Theory: Pool Quality Metrics

### 1. Total Value Locked (TVL)

**Formula**:
```
TVL = (Reserve_A × Price_A) + (Reserve_B × Price_B)
```

For a token/stablecoin pair (like ETH/USDC):
```
TVL = (ETH_Reserve × ETH_Price) + USDC_Reserve
```

**Example**:
- Pool: 1,000 ETH + 2,000,000 USDC
- ETH Price: $2,000
- TVL = (1,000 × $2,000) + $2,000,000 = $4,000,000

**Why It Matters**: Higher TVL generally means lower slippage, but only if other metrics are good.

---

### 2. Volume/TVL Ratio (Capital Efficiency)

**Formula**:
```
Volume/TVL Ratio = 24h_Trading_Volume / TVL
```

**Interpretation**:
- **< 0.1 (10%)**: Low efficiency, capital underutilized
- **0.1 - 0.3 (10-30%)**: Moderate efficiency
- **0.3 - 1.0 (30-100%)**: High efficiency, active trading
- **> 1.0 (100%+)**: Very high efficiency (volume exceeds TVL)

**Example**:
- Pool TVL: $4,000,000
- 24h Volume: $1,200,000
- Ratio: $1,200,000 / $4,000,000 = 0.30 (30% - High efficiency)

**Why It Matters**: A pool with 100% volume/TVL ratio generates more fees for LPs than a pool with 10% ratio.

---

### 3. Reserve Balance Score (Symmetry)

In a constant product AMM (x × y = k), the optimal state is 50/50 value split.

**Formula**:
```
Value_A = Reserve_A × Price_A
Value_B = Reserve_B × Price_B
Total_Value = Value_A + Value_B

Ratio_A = Value_A / Total_Value
Ratio_B = Value_B / Total_Value

Deviation = |Ratio_A - 0.5| × 2  # Convert to 0-1 scale
Balance_Score = (1 - Deviation) × 100  # Convert to 0-100
```

**Examples**:

| Reserve A Value | Reserve B Value | Ratio A | Deviation | Balance Score |
|----------------|-----------------|---------|-----------|---------------|
| $2,000,000 | $2,000,000 | 50% | 0.0 | **100** (Perfect) |
| $2,500,000 | $1,500,000 | 62.5% | 0.25 | **75** (Good) |
| $3,000,000 | $1,000,000 | 75% | 0.5 | **50** (Fair) |
| $3,600,000 | $400,000 | 90% | 0.8 | **20** (Poor) |

**Why It Matters**: Imbalanced pools have higher slippage and worse price execution.

---

### 4. Liquidity Depth Score

Measures how much liquidity is available for a standard trade size (e.g., $100k).

**Formula**:
```
# Test a $100k swap and measure slippage
Test_Amount = $100,000

Slippage = calculate_slippage(reserves, test_amount)

Depth_Score = {
    slippage < 0.1%:  100 (Excellent)
    slippage < 0.3%:  90  (Very Good)
    slippage < 0.5%:  80  (Good)
    slippage < 1.0%:  60  (Moderate)
    slippage < 2.0%:  40  (Fair)
    slippage < 5.0%:  20  (Poor)
    slippage >= 5.0%: 0   (Very Poor)
}
```

**Example**:
- Pool: 1,000 ETH + 2,000,000 USDC (ETH = $2,000)
- Test swap: $100,000 → 50 ETH
- Resulting slippage: 0.25%
- Depth Score: **90** (Very Good)

**Why It Matters**: Deep liquidity means institutional traders can execute large orders without massive slippage.

---

### 5. Fee Efficiency Score

Different pools should have different fee tiers based on volatility.

**Uniswap V3 Fee Tiers**:
- **0.01%**: Stablecoin pairs (USDC/USDT, DAI/USDC)
- **0.05%**: Correlated pairs (ETH/WBTC, stETH/ETH)
- **0.30%**: Standard pairs (ETH/USDC, most tokens)
- **1.00%**: Exotic pairs (high volatility tokens)

**Scoring Logic**:
```python
def score_fee_efficiency(pool_type: str, fee_tier: float) -> int:
    optimal_fees = {
        "stablecoin": 0.0001,      # 0.01%
        "correlated": 0.0005,      # 0.05%
        "standard": 0.003,         # 0.30%
        "exotic": 0.01             # 1.00%
    }

    optimal = optimal_fees[pool_type]
    deviation = abs(fee_tier - optimal) / optimal

    if deviation < 0.2:    # Within 20% of optimal
        return 100
    elif deviation < 0.5:  # Within 50% of optimal
        return 80
    elif deviation < 1.0:  # Within 100% of optimal
        return 60
    else:
        return 40
```

---

### 6. Overall Pool Quality Score (Composite)

Weighted average of all metrics:

**Formula**:
```
Quality_Score = (
    TVL_Score × 0.20 +              # 20% weight
    Volume_TVL_Score × 0.25 +       # 25% weight (most important)
    Balance_Score × 0.20 +          # 20% weight
    Depth_Score × 0.20 +            # 20% weight
    Fee_Efficiency_Score × 0.15     # 15% weight
)
```

**Rating Categories**:
- **90-100**: Excellent (Blue-chip pools)
- **80-89**: Very Good (Institutional grade)
- **70-79**: Good (Retail-friendly)
- **60-69**: Moderate (Acceptable for small trades)
- **50-59**: Fair (Use with caution)
- **0-49**: Poor (Avoid or arbitrage opportunity)

---

## Implementation

### Step 1: Update Enums (Day 003 Code)

Add pool quality rating enum to `src/models/defi_types.py`:

```python
from enum import Enum

class PoolQualityRating(Enum):
    """Pool quality rating categories"""
    EXCELLENT = "Excellent"        # 90-100: Blue-chip pools
    VERY_GOOD = "Very Good"        # 80-89: Institutional grade
    GOOD = "Good"                  # 70-79: Retail-friendly
    MODERATE = "Moderate"          # 60-69: Acceptable
    FAIR = "Fair"                  # 50-59: Use with caution
    POOR = "Poor"                  # 0-49: Avoid

    @classmethod
    def from_score(cls, score: float) -> "PoolQualityRating":
        """Convert numeric score to rating"""
        if score >= 90:
            return cls.EXCELLENT
        elif score >= 80:
            return cls.VERY_GOOD
        elif score >= 70:
            return cls.GOOD
        elif score >= 60:
            return cls.MODERATE
        elif score >= 50:
            return cls.FAIR
        else:
            return cls.POOR


class PoolType(Enum):
    """Pool type for fee efficiency scoring"""
    STABLECOIN = "stablecoin"      # USDC/USDT, DAI/USDC
    CORRELATED = "correlated"      # ETH/WBTC, stETH/ETH
    STANDARD = "standard"          # ETH/USDC, most pairs
    EXOTIC = "exotic"              # High volatility tokens
```

**File**: `/src/models/defi_types.py` (append to existing file)

---

### Step 2: Add Dataclasses for Pool Quality

Add to `src/models/defi_types.py`:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class PoolQualityMetrics:
    """Individual quality metrics for a liquidity pool"""
    tvl: float                          # Total Value Locked in USD
    tvl_score: int                      # 0-100 score based on TVL size
    volume_24h: float                   # 24-hour trading volume in USD
    volume_tvl_ratio: float             # Volume/TVL ratio
    volume_tvl_score: int               # 0-100 score based on capital efficiency
    reserve_balance_score: int          # 0-100 score based on reserve symmetry
    liquidity_depth_score: int          # 0-100 score based on slippage for $100k trade
    fee_efficiency_score: int           # 0-100 score based on fee tier appropriateness
    overall_score: float                # Weighted composite score (0-100)
    rating: str                         # Quality rating (Excellent, Good, etc.)

    # Additional context
    reserve_a_value: float              # Dollar value of token A reserves
    reserve_b_value: float              # Dollar value of token B reserves
    reserve_ratio: float                # Ratio of value_a / (value_a + value_b)
    slippage_100k: float                # Slippage % for $100k trade


@dataclass
class PoolComparisonResult:
    """Comparison of multiple pools"""
    pools: list[dict]                   # List of pool quality data
    best_pool: str                      # Name of highest-rated pool
    best_score: float                   # Score of best pool
    worst_pool: str                     # Name of lowest-rated pool
    worst_score: float                  # Score of worst pool
    ranking: list[str]                  # Pools ranked by quality (best to worst)
```

---

### Step 3: Implement Pool Quality Scoring Functions

Add to `src/analytics/liquidity_analyzer.py`:

```python
def calculate_tvl(
    self,
    reserve_a: float,
    reserve_b: float,
    price_a: float,
    price_b: float = 1.0
) -> float:
    """
    Calculate Total Value Locked (TVL) in USD.

    Args:
        reserve_a: Amount of token A in pool
        reserve_b: Amount of token B in pool
        price_a: USD price of token A
        price_b: USD price of token B (default 1.0 for stablecoins)

    Returns:
        Total value locked in USD

    Example:
        1,000 ETH + 2,000,000 USDC
        ETH price = $2,000
        TVL = (1,000 × $2,000) + (2,000,000 × $1) = $4,000,000
    """
    value_a = reserve_a * price_a
    value_b = reserve_b * price_b
    tvl = value_a + value_b

    return tvl


def score_tvl(self, tvl: float) -> int:
    """
    Score TVL on a 0-100 scale.

    Scoring Logic:
        >= $100M:  100 (Blue-chip)
        >= $50M:   90  (Institutional)
        >= $10M:   80  (Large pool)
        >= $5M:    70  (Medium-large)
        >= $1M:    60  (Medium)
        >= $500k:  50  (Small-medium)
        >= $100k:  40  (Small)
        < $100k:   20  (Very small)
    """
    if tvl >= 100_000_000:      # >= $100M
        return 100
    elif tvl >= 50_000_000:     # >= $50M
        return 90
    elif tvl >= 10_000_000:     # >= $10M
        return 80
    elif tvl >= 5_000_000:      # >= $5M
        return 70
    elif tvl >= 1_000_000:      # >= $1M
        return 60
    elif tvl >= 500_000:        # >= $500k
        return 50
    elif tvl >= 100_000:        # >= $100k
        return 40
    else:
        return 20


def calculate_volume_tvl_ratio(self, volume_24h: float, tvl: float) -> float:
    """
    Calculate Volume/TVL ratio for capital efficiency.

    Args:
        volume_24h: 24-hour trading volume in USD
        tvl: Total value locked in USD

    Returns:
        Volume/TVL ratio (e.g., 0.30 = 30%)

    Example:
        Volume = $1,200,000
        TVL = $4,000,000
        Ratio = 1,200,000 / 4,000,000 = 0.30 (30%)
    """
    if tvl == 0:
        return 0

    ratio = volume_24h / tvl
    return ratio


def score_volume_tvl_ratio(self, ratio: float) -> int:
    """
    Score Volume/TVL ratio on a 0-100 scale.

    Scoring Logic:
        >= 1.0 (100%+):  100 (Excellent efficiency)
        >= 0.5 (50%):    90  (Very good)
        >= 0.3 (30%):    80  (Good)
        >= 0.2 (20%):    70  (Moderate)
        >= 0.1 (10%):    60  (Fair)
        >= 0.05 (5%):    40  (Low)
        < 0.05 (5%):     20  (Very low)
    """
    if ratio >= 1.0:
        return 100
    elif ratio >= 0.5:
        return 90
    elif ratio >= 0.3:
        return 80
    elif ratio >= 0.2:
        return 70
    elif ratio >= 0.1:
        return 60
    elif ratio >= 0.05:
        return 40
    else:
        return 20


def calculate_reserve_balance_score(
    self,
    reserve_a: float,
    reserve_b: float,
    price_a: float,
    price_b: float = 1.0
) -> tuple[int, float, float, float]:
    """
    Calculate reserve balance score (pool symmetry).

    Optimal state: 50/50 value split

    Args:
        reserve_a: Amount of token A
        reserve_b: Amount of token B
        price_a: USD price of token A
        price_b: USD price of token B

    Returns:
        Tuple of (score, reserve_a_value, reserve_b_value, ratio)

    Example:
        1,000 ETH ($2,000) + 2,000,000 USDC
        Value A = $2,000,000, Value B = $2,000,000
        Ratio = 50%, Deviation = 0, Score = 100
    """
    value_a = reserve_a * price_a
    value_b = reserve_b * price_b
    total_value = value_a + value_b

    if total_value == 0:
        return 0, 0, 0, 0

    ratio_a = value_a / total_value
    ratio_b = value_b / total_value

    # Calculate deviation from 50/50 (0 = perfect, 1 = completely imbalanced)
    deviation = abs(ratio_a - 0.5) * 2

    # Convert to 0-100 score
    balance_score = int((1 - deviation) * 100)

    return balance_score, value_a, value_b, ratio_a


def calculate_liquidity_depth_score(
    self,
    reserve_a: float,
    reserve_b: float,
    price_a: float,
    test_amount_usd: float = 100_000,
    fee: float = 0.003
) -> tuple[int, float]:
    """
    Calculate liquidity depth score by testing a standard trade size.

    Tests a $100k swap and measures slippage.

    Args:
        reserve_a: Pool reserve of token A
        reserve_b: Pool reserve of token B (usually stablecoin)
        price_a: Current price of token A
        test_amount_usd: Test trade size in USD (default $100k)
        fee: Pool fee (default 0.3%)

    Returns:
        Tuple of (depth_score, slippage_percent)

    Scoring:
        < 0.1%:  100 (Excellent depth)
        < 0.3%:  90  (Very good)
        < 0.5%:  80  (Good)
        < 1.0%:  60  (Moderate)
        < 2.0%:  40  (Fair)
        < 5.0%:  20  (Poor)
        >= 5.0%: 0   (Very poor)
    """
    # Calculate test trade in token A units
    test_amount = test_amount_usd / price_a

    # Use our existing swap calculation
    swap_result = self.calculate_swap_output(
        reserve_in=reserve_a,
        reserve_out=reserve_b,
        amount_in=test_amount,
        fee=fee
    )

    # Calculate expected output at current price
    expected_output = test_amount * price_a

    # Calculate slippage
    slippage_percent = abs(
        (expected_output - swap_result.output_amount) / expected_output * 100
    )

    # Score based on slippage
    if slippage_percent < 0.1:
        depth_score = 100
    elif slippage_percent < 0.3:
        depth_score = 90
    elif slippage_percent < 0.5:
        depth_score = 80
    elif slippage_percent < 1.0:
        depth_score = 60
    elif slippage_percent < 2.0:
        depth_score = 40
    elif slippage_percent < 5.0:
        depth_score = 20
    else:
        depth_score = 0

    return depth_score, slippage_percent


def score_fee_efficiency(self, pool_type: str, fee_tier: float) -> int:
    """
    Score fee efficiency based on pool type and fee tier.

    Args:
        pool_type: Type of pool (stablecoin, correlated, standard, exotic)
        fee_tier: Current fee tier (e.g., 0.003 = 0.3%)

    Returns:
        Fee efficiency score (0-100)

    Optimal fees:
        stablecoin: 0.01% (0.0001)
        correlated: 0.05% (0.0005)
        standard: 0.30% (0.003)
        exotic: 1.00% (0.01)
    """
    optimal_fees = {
        "stablecoin": 0.0001,
        "correlated": 0.0005,
        "standard": 0.003,
        "exotic": 0.01
    }

    if pool_type not in optimal_fees:
        return 50  # Unknown type, neutral score

    optimal = optimal_fees[pool_type]
    deviation = abs(fee_tier - optimal) / optimal

    # Score based on deviation from optimal
    if deviation < 0.2:      # Within 20% of optimal
        return 100
    elif deviation < 0.5:    # Within 50% of optimal
        return 80
    elif deviation < 1.0:    # Within 100% of optimal
        return 60
    else:
        return 40


def calculate_pool_quality(
    self,
    reserve_a: float,
    reserve_b: float,
    price_a: float,
    price_b: float,
    volume_24h: float,
    pool_type: str = "standard",
    fee: float = 0.003
) -> PoolQualityMetrics:
    """
    Calculate comprehensive pool quality score.

    This is the master function that combines all quality metrics.

    Args:
        reserve_a: Pool reserve of token A
        reserve_b: Pool reserve of token B
        price_a: USD price of token A
        price_b: USD price of token B
        volume_24h: 24-hour trading volume in USD
        pool_type: Pool type for fee scoring (default "standard")
        fee: Pool fee tier (default 0.3%)

    Returns:
        PoolQualityMetrics with all scores and rating

    Example:
        Pool: 1,000 ETH + 2,000,000 USDC
        ETH = $2,000, Volume = $1,200,000
        Returns comprehensive quality metrics
    """
    # Calculate TVL and score
    tvl = self.calculate_tvl(reserve_a, reserve_b, price_a, price_b)
    tvl_score = self.score_tvl(tvl)

    # Calculate volume/TVL ratio and score
    volume_tvl_ratio = self.calculate_volume_tvl_ratio(volume_24h, tvl)
    volume_tvl_score = self.score_volume_tvl_ratio(volume_tvl_ratio)

    # Calculate reserve balance and score
    balance_score, value_a, value_b, ratio_a = self.calculate_reserve_balance_score(
        reserve_a, reserve_b, price_a, price_b
    )

    # Calculate liquidity depth and score
    depth_score, slippage_100k = self.calculate_liquidity_depth_score(
        reserve_a, reserve_b, price_a, fee=fee
    )

    # Calculate fee efficiency score
    fee_efficiency_score = self.score_fee_efficiency(pool_type, fee)

    # Calculate weighted composite score
    overall_score = (
        tvl_score * 0.20 +
        volume_tvl_score * 0.25 +
        balance_score * 0.20 +
        depth_score * 0.20 +
        fee_efficiency_score * 0.15
    )

    # Get rating from score
    rating = PoolQualityRating.from_score(overall_score)

    return PoolQualityMetrics(
        tvl=tvl,
        tvl_score=tvl_score,
        volume_24h=volume_24h,
        volume_tvl_ratio=volume_tvl_ratio,
        volume_tvl_score=volume_tvl_score,
        reserve_balance_score=balance_score,
        liquidity_depth_score=depth_score,
        fee_efficiency_score=fee_efficiency_score,
        overall_score=overall_score,
        rating=rating.value,
        reserve_a_value=value_a,
        reserve_b_value=value_b,
        reserve_ratio=ratio_a,
        slippage_100k=slippage_100k
    )


def compare_pools(self, pools_data: list[dict]) -> PoolComparisonResult:
    """
    Compare multiple pools and rank by quality.

    Args:
        pools_data: List of pool data dictionaries, each containing:
            - name: Pool identifier (e.g., "ETH/USDC Uniswap")
            - reserve_a, reserve_b, price_a, price_b
            - volume_24h, pool_type, fee

    Returns:
        PoolComparisonResult with rankings and comparisons

    Example:
        pools = [
            {"name": "ETH/USDC Uniswap", "reserve_a": 1000, ...},
            {"name": "ETH/USDC Sushiswap", "reserve_a": 500, ...}
        ]
        result = compare_pools(pools)
    """
    pool_scores = []

    for pool in pools_data:
        # Calculate quality for this pool
        quality = self.calculate_pool_quality(
            reserve_a=pool["reserve_a"],
            reserve_b=pool["reserve_b"],
            price_a=pool["price_a"],
            price_b=pool.get("price_b", 1.0),
            volume_24h=pool["volume_24h"],
            pool_type=pool.get("pool_type", "standard"),
            fee=pool.get("fee", 0.003)
        )

        pool_scores.append({
            "name": pool["name"],
            "overall_score": quality.overall_score,
            "rating": quality.rating,
            "tvl": quality.tvl,
            "volume_tvl_ratio": quality.volume_tvl_ratio,
            "balance_score": quality.reserve_balance_score,
            "depth_score": quality.liquidity_depth_score,
            "metrics": quality
        })

    # Sort by overall score (descending)
    pool_scores.sort(key=lambda x: x["overall_score"], reverse=True)

    # Extract rankings
    ranking = [pool["name"] for pool in pool_scores]
    best_pool = pool_scores[0]["name"]
    best_score = pool_scores[0]["overall_score"]
    worst_pool = pool_scores[-1]["name"]
    worst_score = pool_scores[-1]["overall_score"]

    return PoolComparisonResult(
        pools=pool_scores,
        best_pool=best_pool,
        best_score=best_score,
        worst_pool=worst_pool,
        worst_score=worst_score,
        ranking=ranking
    )
```

---

### Step 4: Add API Endpoints

Create new endpoints in `routes/liquidity.py`:

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from src.analytics.liquidity_analyzer import LiquidityAnalyzer
from src.models.defi_types import PoolQualityMetrics, PoolComparisonResult

router = APIRouter(prefix="/api/liquidity", tags=["Liquidity Analysis"])
analyzer = LiquidityAnalyzer()


# --- Request Models ---

class PoolQualityRequest(BaseModel):
    """Request model for pool quality calculation"""
    reserve_a: float = Field(..., gt=0, description="Reserve of token A")
    reserve_b: float = Field(..., gt=0, description="Reserve of token B")
    price_a: float = Field(..., gt=0, description="USD price of token A")
    price_b: float = Field(1.0, gt=0, description="USD price of token B")
    volume_24h: float = Field(..., ge=0, description="24-hour trading volume in USD")
    pool_type: str = Field("standard", description="Pool type: stablecoin, correlated, standard, exotic")
    fee: float = Field(0.003, gt=0, le=0.1, description="Pool fee tier (e.g., 0.003 = 0.3%)")


class PoolComparisonRequest(BaseModel):
    """Request model for comparing multiple pools"""
    pools: list[dict] = Field(..., min_items=2, description="List of pool data")


# --- Endpoints ---

@router.post("/pool-quality", response_model=dict)
async def calculate_pool_quality(request: PoolQualityRequest):
    """
    Calculate comprehensive quality score for a liquidity pool.

    Analyzes:
    - Total Value Locked (TVL)
    - Volume/TVL ratio (capital efficiency)
    - Reserve balance (pool symmetry)
    - Liquidity depth (slippage for $100k trade)
    - Fee efficiency

    Returns overall 0-100 score with rating.
    """
    try:
        quality = analyzer.calculate_pool_quality(
            reserve_a=request.reserve_a,
            reserve_b=request.reserve_b,
            price_a=request.price_a,
            price_b=request.price_b,
            volume_24h=request.volume_24h,
            pool_type=request.pool_type,
            fee=request.fee
        )

        return {
            "pool_quality": {
                "overall_score": round(quality.overall_score, 2),
                "rating": quality.rating,
                "metrics": {
                    "tvl": {
                        "value": quality.tvl,
                        "score": quality.tvl_score
                    },
                    "volume_efficiency": {
                        "volume_24h": quality.volume_24h,
                        "volume_tvl_ratio": round(quality.volume_tvl_ratio, 4),
                        "score": quality.volume_tvl_score
                    },
                    "reserve_balance": {
                        "score": quality.reserve_balance_score,
                        "reserve_a_value": quality.reserve_a_value,
                        "reserve_b_value": quality.reserve_b_value,
                        "ratio": round(quality.reserve_ratio, 4)
                    },
                    "liquidity_depth": {
                        "score": quality.liquidity_depth_score,
                        "slippage_100k": round(quality.slippage_100k, 4)
                    },
                    "fee_efficiency": {
                        "score": quality.fee_efficiency_score
                    }
                }
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compare-pools", response_model=dict)
async def compare_pools(request: PoolComparisonRequest):
    """
    Compare multiple pools and rank by quality.

    Each pool in the list should include:
    - name: Pool identifier
    - reserve_a, reserve_b: Pool reserves
    - price_a, price_b: Token prices
    - volume_24h: 24-hour volume
    - pool_type (optional): Pool type
    - fee (optional): Fee tier
    """
    try:
        comparison = analyzer.compare_pools(request.pools)

        return {
            "comparison": {
                "best_pool": {
                    "name": comparison.best_pool,
                    "score": round(comparison.best_score, 2)
                },
                "worst_pool": {
                    "name": comparison.worst_pool,
                    "score": round(comparison.worst_score, 2)
                },
                "ranking": comparison.ranking,
                "pools": [
                    {
                        "name": pool["name"],
                        "score": round(pool["overall_score"], 2),
                        "rating": pool["rating"],
                        "tvl": pool["tvl"],
                        "volume_tvl_ratio": round(pool["volume_tvl_ratio"], 4)
                    }
                    for pool in comparison.pools
                ]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/quality-metrics-info", response_model=dict)
async def get_quality_metrics_info():
    """
    Get information about pool quality scoring methodology.
    """
    return {
        "scoring_methodology": {
            "overall_score_weights": {
                "tvl_score": "20%",
                "volume_tvl_score": "25%",
                "reserve_balance_score": "20%",
                "liquidity_depth_score": "20%",
                "fee_efficiency_score": "15%"
            },
            "tvl_scoring": {
                "100M+": 100,
                "50M-100M": 90,
                "10M-50M": 80,
                "5M-10M": 70,
                "1M-5M": 60,
                "500k-1M": 50,
                "100k-500k": 40,
                "under_100k": 20
            },
            "volume_tvl_ratio_scoring": {
                "100%+": 100,
                "50-100%": 90,
                "30-50%": 80,
                "20-30%": 70,
                "10-20%": 60,
                "5-10%": 40,
                "under_5%": 20
            },
            "depth_scoring": {
                "slippage_under_0.1%": 100,
                "slippage_0.1-0.3%": 90,
                "slippage_0.3-0.5%": 80,
                "slippage_0.5-1.0%": 60,
                "slippage_1.0-2.0%": 40,
                "slippage_2.0-5.0%": 20,
                "slippage_over_5%": 0
            },
            "rating_categories": {
                "90-100": "Excellent (Blue-chip)",
                "80-89": "Very Good (Institutional)",
                "70-79": "Good (Retail-friendly)",
                "60-69": "Moderate (Acceptable)",
                "50-59": "Fair (Use with caution)",
                "0-49": "Poor (Avoid)"
            }
        }
    }
```

**File**: `/routes/liquidity.py` (add to existing file or create if not exists)

---

## Testing with curl

### Test 1: Calculate Pool Quality for ETH/USDC Uniswap

**Scenario**: Large, balanced pool with good volume

```bash
curl -X POST http://localhost:8000/api/liquidity/pool-quality \
  -H "Content-Type: application/json" \
  -d '{
    "reserve_a": 1000,
    "reserve_b": 2000000,
    "price_a": 2000,
    "price_b": 1.0,
    "volume_24h": 1200000,
    "pool_type": "standard",
    "fee": 0.003
  }'
```

**Expected Response**:
```json
{
  "pool_quality": {
    "overall_score": 81.0,
    "rating": "Very Good",
    "metrics": {
      "tvl": {
        "value": 4000000.0,
        "score": 70
      },
      "volume_efficiency": {
        "volume_24h": 1200000.0,
        "volume_tvl_ratio": 0.3,
        "score": 80
      },
      "reserve_balance": {
        "score": 100,
        "reserve_a_value": 2000000.0,
        "reserve_b_value": 2000000.0,
        "ratio": 0.5
      },
      "liquidity_depth": {
        "score": 90,
        "slippage_100k": 0.2512
      },
      "fee_efficiency": {
        "score": 100
      }
    }
  }
}
```

**Analysis**:
- **TVL Score: 70** ($4M pool - medium-large)
- **Volume/TVL Score: 80** (30% ratio - good efficiency)
- **Balance Score: 100** (Perfect 50/50 split)
- **Depth Score: 90** (0.25% slippage for $100k - very good)
- **Fee Efficiency: 100** (0.3% is optimal for standard pairs)
- **Overall: 81.0 - Very Good** (Institutional grade)

---

### Test 2: Calculate Pool Quality for Small, Imbalanced Pool

**Scenario**: Small pool with poor balance and low volume

```bash
curl -X POST http://localhost:8000/api/liquidity/pool-quality \
  -H "Content-Type: application/json" \
  -d '{
    "reserve_a": 50,
    "reserve_b": 500000,
    "price_a": 2000,
    "price_b": 1.0,
    "volume_24h": 20000,
    "pool_type": "standard",
    "fee": 0.003
  }'
```

**Expected Response**:
```json
{
  "pool_quality": {
    "overall_score": 42.5,
    "rating": "Poor",
    "metrics": {
      "tvl": {
        "value": 600000.0,
        "score": 50
      },
      "volume_efficiency": {
        "volume_24h": 20000.0,
        "volume_tvl_ratio": 0.0333,
        "score": 20
      },
      "reserve_balance": {
        "score": 66,
        "reserve_a_value": 100000.0,
        "reserve_b_value": 500000.0,
        "ratio": 0.1667
      },
      "liquidity_depth": {
        "score": 0,
        "slippage_100k": 14.2857
      },
      "fee_efficiency": {
        "score": 100
      }
    }
  }
}
```

**Analysis**:
- **TVL Score: 50** ($600k - small-medium pool)
- **Volume/TVL Score: 20** (3.3% ratio - very low efficiency)
- **Balance Score: 66** (17%/83% split - imbalanced)
- **Depth Score: 0** (14.3% slippage - very poor depth)
- **Overall: 42.5 - Poor** (Avoid for large trades)

---

### Test 3: Compare Multiple Pools

**Scenario**: Compare Uniswap, Sushiswap, and Curve pools

```bash
curl -X POST http://localhost:8000/api/liquidity/compare-pools \
  -H "Content-Type: application/json" \
  -d '{
    "pools": [
      {
        "name": "ETH/USDC Uniswap V3",
        "reserve_a": 1000,
        "reserve_b": 2000000,
        "price_a": 2000,
        "price_b": 1.0,
        "volume_24h": 1500000,
        "pool_type": "standard",
        "fee": 0.003
      },
      {
        "name": "ETH/USDC Sushiswap",
        "reserve_a": 500,
        "reserve_b": 1000000,
        "price_a": 2000,
        "price_b": 1.0,
        "volume_24h": 400000,
        "pool_type": "standard",
        "fee": 0.003
      },
      {
        "name": "USDC/USDT Curve",
        "reserve_a": 10000000,
        "reserve_b": 10000000,
        "price_a": 1.0,
        "price_b": 1.0,
        "volume_24h": 5000000,
        "pool_type": "stablecoin",
        "fee": 0.0001
      }
    ]
  }'
```

**Expected Response**:
```json
{
  "comparison": {
    "best_pool": {
      "name": "USDC/USDT Curve",
      "score": 93.5
    },
    "worst_pool": {
      "name": "ETH/USDC Sushiswap",
      "score": 74.0
    },
    "ranking": [
      "USDC/USDT Curve",
      "ETH/USDC Uniswap V3",
      "ETH/USDC Sushiswap"
    ],
    "pools": [
      {
        "name": "USDC/USDT Curve",
        "score": 93.5,
        "rating": "Excellent",
        "tvl": 20000000.0,
        "volume_tvl_ratio": 0.25
      },
      {
        "name": "ETH/USDC Uniswap V3",
        "score": 82.25,
        "rating": "Very Good",
        "tvl": 4000000.0,
        "volume_tvl_ratio": 0.375
      },
      {
        "name": "ETH/USDC Sushiswap",
        "score": 74.0,
        "rating": "Good",
        "tvl": 2000000.0,
        "volume_tvl_ratio": 0.2
      }
    ]
  }
}
```

**Analysis**:
- **Winner: USDC/USDT Curve** (93.5 - Excellent)
  - Massive TVL ($20M), perfect balance, optimal fee tier for stablecoins

- **Runner-up: ETH/USDC Uniswap V3** (82.25 - Very Good)
  - Good TVL, high volume efficiency (37.5%), balanced reserves

- **Third: ETH/USDC Sushiswap** (74.0 - Good)
  - Lower TVL, moderate volume efficiency (20%), still balanced

---

### Test 4: Get Quality Metrics Information

```bash
curl -X GET http://localhost:8000/api/liquidity/quality-metrics-info
```

**Expected Response**:
```json
{
  "scoring_methodology": {
    "overall_score_weights": {
      "tvl_score": "20%",
      "volume_tvl_score": "25%",
      "reserve_balance_score": "20%",
      "liquidity_depth_score": "20%",
      "fee_efficiency_score": "15%"
    },
    "tvl_scoring": {
      "100M+": 100,
      "50M-100M": 90,
      ...
    },
    ...
  }
}
```

---

## Common Issues

### Issue 1: Pool Quality Score Seems Too Low

**Symptom**: Pool has good TVL but overall score is low.

**Cause**: Other metrics are poor (balance, volume efficiency, depth).

**Fix**: Check individual metric scores to identify weak areas.

```bash
# Look at the detailed metrics breakdown
{
  "tvl": {"score": 70},           # Good
  "volume_efficiency": {"score": 20},  # Problem!
  "reserve_balance": {"score": 100},
  "liquidity_depth": {"score": 60}
}
```

**Solution**: In this case, low volume/TVL ratio (20 score) drags down overall score despite good TVL.

---

### Issue 2: Depth Score is 0

**Symptom**: `liquidity_depth_score: 0` with high slippage.

**Cause**: Pool is too small for $100k test trade, or severely imbalanced.

**Example**:
```json
{
  "liquidity_depth": {
    "score": 0,
    "slippage_100k": 15.3
  }
}
```

**Fix**: This pool is unsuitable for large trades. Use for small trades only or provide more liquidity.

---

### Issue 3: Fee Efficiency Score is Low

**Symptom**: Pool has 40-60 fee efficiency score.

**Cause**: Fee tier doesn't match pool type.

**Example**: Stablecoin pool with 0.3% fee (should be 0.01%):
```json
{
  "pool_type": "stablecoin",
  "fee": 0.003,           # 0.3% (too high!)
  "fee_efficiency_score": 40
}
```

**Fix**: Use appropriate fee tiers:
- Stablecoins: 0.01%
- Correlated: 0.05%
- Standard: 0.30%
- Exotic: 1.00%

---

### Issue 4: Comparison Returns Wrong Best Pool

**Symptom**: Pool with lower TVL wins comparison.

**Cause**: Volume efficiency and balance can outweigh TVL (which is only 20% weight).

**Example**:
```json
{
  "Pool A": {
    "tvl": 10000000,  # $10M
    "volume_tvl": 0.05,  # 5% (very low)
    "score": 68
  },
  "Pool B": {
    "tvl": 2000000,   # $2M
    "volume_tvl": 0.40,  # 40% (high)
    "score": 85       # Winner!
  }
}
```

**This is correct**: Pool B is more efficient despite lower TVL. Remember: **quality ≠ size**.

---

## Key Takeaways

### What We Learned Today

1. **TVL is Not Everything**: A $100M pool with 1% volume/TVL ratio is less efficient than a $10M pool with 50% ratio.

2. **Balance Matters**: Imbalanced pools (e.g., 90/10 split) have higher slippage and worse execution.

3. **Depth is Critical for Whales**: Institutions need pools with <0.5% slippage for $100k+ trades.

4. **Fee Tiers Should Match Volatility**: Stablecoins need 0.01%, volatile pairs need 0.3-1%.

5. **Composite Scoring**: Our weighted system (Volume 25%, TVL 20%, Balance 20%, Depth 20%, Fee 15%) balances multiple factors.

### Real-World Applications

- **Portfolio Construction**: Choose pools with scores 80+
- **Arbitrage**: Target pools with scores 40-60 (inefficiencies)
- **LP Strategy**: Provide liquidity to high-scoring pools (better returns)
- **Risk Management**: Avoid pools with depth score <40

### Tomorrow (Day 009)

We'll build an **Impermanent Loss Calculator** that shows LPs how much they're losing (or gaining) vs. just holding tokens.

**Preview**:
- What is impermanent loss?
- Mathematical formula: `IL = 2√(price_ratio) / (1 + price_ratio) - 1`
- When does IL become permanent (pool abandonment)?
- Fee income vs IL analysis

---

## Summary

**Files Modified**:
1. `/src/models/defi_types.py` - Added `PoolQualityRating`, `PoolType`, `PoolQualityMetrics`, `PoolComparisonResult`
2. `/src/analytics/liquidity_analyzer.py` - Added 10+ pool quality functions
3. `/routes/liquidity.py` - Added 3 new endpoints

**New API Endpoints**:
- `POST /api/liquidity/pool-quality` - Calculate comprehensive pool quality
- `POST /api/liquidity/compare-pools` - Compare and rank multiple pools
- `GET /api/liquidity/quality-metrics-info` - Get scoring methodology

**Key Functions**:
- `calculate_tvl()` - Total value locked calculation
- `calculate_volume_tvl_ratio()` - Capital efficiency metric
- `calculate_reserve_balance_score()` - Pool symmetry analysis
- `calculate_liquidity_depth_score()` - Slippage testing for $100k trades
- `calculate_pool_quality()` - Master function combining all metrics
- `compare_pools()` - Multi-pool ranking system

**Testing**: 4 curl examples covering quality calculation, poor pools, pool comparison, and methodology info.

**Day 008 Complete!** ✅

Tomorrow we tackle impermanent loss - the LP's worst enemy! 🎯
