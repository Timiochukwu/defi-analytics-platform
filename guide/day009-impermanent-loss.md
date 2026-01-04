# Day 009: Impermanent Loss Calculator

**Focus**: Understanding and calculating impermanent loss (IL) for liquidity providers in AMM pools, comparing IL to fee income, and determining when providing liquidity is profitable.

**Time Estimate**: 2.5 hours
**Difficulty**: Intermediate-Advanced
**Prerequisites**: Days 001-008 complete

---

## Table of Contents

1. [Learning Objectives](#learning-objectives)
2. [What We're Building Today](#what-were-building-today)
3. [Theory: Impermanent Loss Explained](#theory-impermanent-loss-explained)
4. [Implementation](#implementation)
5. [Testing with curl](#testing-with-curl)
6. [Common Issues](#common-issues)
7. [Key Takeaways](#key-takeaways)

---

## Learning Objectives

By the end of Day 009, you will:

- ✅ Understand what impermanent loss is and why it occurs
- ✅ Calculate IL percentage for any price change
- ✅ Compare IL to fee income to determine profitability
- ✅ Understand when IL becomes "permanent" (realized loss)
- ✅ Calculate LP position value vs holding (HODL) strategy
- ✅ Build an IL simulator for various price scenarios
- ✅ Make informed decisions about providing liquidity

---

## What We're Building Today

### Real-World Problem

**Scenario**: You provide 1 ETH + $2,000 USDC to a Uniswap pool when ETH = $2,000.

After 1 month:
- ETH price increases to $3,000
- You earned $50 in trading fees

**Questions**:
1. How much is your LP position worth now?
2. How much would you have if you just held (HODL)?
3. Did you profit or lose by providing liquidity?

**Answer**: You might have **lost money** despite earning fees, due to impermanent loss.

### What is Impermanent Loss?

**Impermanent Loss (IL)** is the opportunity cost of providing liquidity to an AMM pool instead of just holding the tokens.

**Key Points**:
- Occurs when token prices diverge from deposit price
- "Impermanent" because it can revert if prices return
- Becomes "permanent" when you withdraw at a different price
- Amplified by higher price volatility

**Why Does IL Occur?**

AMM pools rebalance automatically via arbitrage. When ETH price increases:
1. Arbitrageurs buy ETH from the pool (cheaper than market)
2. Pool loses ETH, gains USDC
3. You end up with less ETH than you started with
4. Missing out on ETH price gains

---

## Theory: Impermanent Loss Explained

### The Mathematical Formula

For a 50/50 AMM pool (like Uniswap V2):

**Impermanent Loss Formula**:
```
IL = (2 × √price_ratio) / (1 + price_ratio) - 1

Where:
    price_ratio = current_price / initial_price
```

**Alternative Formula (percentage)**:
```
IL% = ((2 × √price_ratio) / (1 + price_ratio) - 1) × 100
```

---

### IL by Price Change

| Price Change | Price Ratio | IL Percentage |
|--------------|-------------|---------------|
| 0% (no change) | 1.0 | **0.00%** |
| +25% | 1.25 | **-0.62%** |
| +50% | 1.5 | **-2.02%** |
| +75% | 1.75 | **-3.53%** |
| +100% (2x) | 2.0 | **-5.72%** |
| +200% (3x) | 3.0 | **-13.40%** |
| +300% (4x) | 4.0 | **-20.00%** |
| +400% (5x) | 5.0 | **-25.46%** |
| -25% | 0.75 | **-0.62%** |
| -50% | 0.5 | **-5.72%** |
| -75% | 0.25 | **-20.00%** |

**Key Insight**: IL is **symmetric** - same loss whether price goes up or down by same ratio.

---

### Example 1: ETH 2x Price Increase

**Initial State**:
- Deposit: 1 ETH + $2,000 USDC
- ETH Price: $2,000
- Total Value: $4,000

**After ETH → $4,000 (2x increase)**:

**Step 1**: Calculate new reserves using constant product formula
```
Initial: x × y = k
1 ETH × 2,000 USDC = 2,000

New: x' × y' = k
x' × y' = 2,000

At new price: y' = x' × $4,000
x' × (x' × 4,000) = 2,000
x'^2 = 0.5
x' = 0.707 ETH
y' = 2,828 USDC
```

**Step 2**: Calculate LP position value
```
LP Value = (0.707 ETH × $4,000) + $2,828 USDC
         = $2,828 + $2,828
         = $5,656
```

**Step 3**: Calculate HODL value
```
HODL Value = (1 ETH × $4,000) + $2,000 USDC
           = $4,000 + $2,000
           = $6,000
```

**Step 4**: Calculate IL
```
IL = $5,656 / $6,000 - 1
   = -5.72%
```

**Result**: You lost $344 compared to just holding!

---

### Example 2: ETH Price Drops 50%

**Initial State**:
- Deposit: 1 ETH + $2,000 USDC
- ETH Price: $2,000

**After ETH → $1,000 (50% decrease)**:

**New Reserves**:
```
x' × y' = 2,000
y' = x' × $1,000
x'^2 = 2
x' = 1.414 ETH
y' = 1,414 USDC
```

**LP Value**:
```
LP Value = (1.414 ETH × $1,000) + $1,414 USDC
         = $1,414 + $1,414
         = $2,828
```

**HODL Value**:
```
HODL Value = (1 ETH × $1,000) + $2,000 USDC
           = $1,000 + $2,000
           = $3,000
```

**IL**:
```
IL = $2,828 / $3,000 - 1
   = -5.72%
```

**Result**: Same IL (-5.72%) whether price goes up or down by 2x!

---

### IL vs Fee Income

**Critical Question**: When do fees outweigh IL?

**Formula**:
```
Net Profit = Fee Income - Impermanent Loss

Profitable if: Fee Income > |IL|
```

**Example**:
- IL: -$344 (-5.72%)
- Fees earned: $400
- **Net Profit**: $400 - $344 = **$56 profit**

**Break-Even Analysis**:

For ETH 2x price increase (IL = -5.72%):
- Need fees > 5.72% to break even
- If pool has 0.3% fee and 100% volume/TVL ratio
- Time to break even: 5.72% / 0.3% = **19 days**

---

### When Does IL Become Permanent?

IL is "impermanent" only while you stay in the pool. It becomes **permanent** when:

1. **You withdraw from the pool** (realize the loss)
2. **Price never returns** to deposit price
3. **Pool is abandoned** (no volume, no fees)

**IL Recovery**:
- If price returns to deposit price: IL → 0%
- If you earn enough fees: Net profit despite IL
- If you exit: IL is realized as permanent loss

---

## Implementation

### Step 1: Add Impermanent Loss Dataclasses

Add to `src/models/defi_types.py`:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ImpermanentLossResult:
    """Result of impermanent loss calculation"""
    initial_price: float                # Starting price of token
    current_price: float                # Current price of token
    price_ratio: float                  # current_price / initial_price
    price_change_percent: float         # Percentage price change

    # Pool state
    initial_token_a: float              # Initial deposit of token A
    initial_token_b: float              # Initial deposit of token B
    current_token_a: float              # Current holdings of token A
    current_token_b: float              # Current holdings of token B

    # Values
    initial_value_usd: float            # Initial position value
    lp_value_usd: float                 # Current LP position value
    hodl_value_usd: float               # Value if just held tokens

    # IL metrics
    il_percent: float                   # Impermanent loss percentage
    il_usd: float                       # Impermanent loss in USD

    # Fee comparison
    fee_income_usd: Optional[float] = None     # Total fees earned
    net_profit_usd: Optional[float] = None     # Fees - IL
    net_profit_percent: Optional[float] = None # Net profit %


@dataclass
class ILSimulationResult:
    """Result of IL simulation across price range"""
    price_scenarios: list[float]        # List of simulated prices
    il_percentages: list[float]         # IL % for each price
    lp_values: list[float]              # LP value for each price
    hodl_values: list[float]            # HODL value for each price
    break_even_price: Optional[float]   # Price where IL = 0 (original price)


@dataclass
class ILBreakEvenAnalysis:
    """Analysis of fees needed to offset IL"""
    il_percent: float                   # Impermanent loss %
    il_usd: float                       # IL in dollars
    fee_apr: float                      # Annual fee rate (e.g., 0.30)
    volume_tvl_ratio: float             # Daily volume/TVL ratio
    days_to_break_even: float           # Days needed to earn IL back in fees
    fees_needed_usd: float              # USD fees needed to offset IL
```

---

### Step 2: Implement IL Calculation Functions

Add to `src/analytics/liquidity_analyzer.py`:

```python
import math
from typing import Optional

def calculate_impermanent_loss(
    self,
    initial_price: float,
    current_price: float,
    initial_token_a: float,
    initial_token_b: float,
    fee_income_usd: Optional[float] = None
) -> ImpermanentLossResult:
    """
    Calculate impermanent loss for a liquidity position.

    Args:
        initial_price: Price of token A when LP position was opened
        current_price: Current price of token A
        initial_token_a: Initial amount of token A deposited
        initial_token_b: Initial amount of token B deposited (usually stablecoin)
        fee_income_usd: Optional total fees earned (for net profit calculation)

    Returns:
        ImpermanentLossResult with full analysis

    Formula:
        IL% = (2 × √(price_ratio)) / (1 + price_ratio) - 1

    Example:
        Initial: 1 ETH + $2,000 USDC at ETH = $2,000
        Current: ETH = $4,000
        Returns IL = -5.72%, LP value = $5,656, HODL = $6,000
    """
    # Calculate price ratio and change
    price_ratio = current_price / initial_price
    price_change_percent = (price_ratio - 1) * 100

    # Calculate initial value
    initial_value_usd = (initial_token_a * initial_price) + initial_token_b

    # Calculate HODL value (just hold both tokens)
    hodl_value_usd = (initial_token_a * current_price) + initial_token_b

    # Calculate constant product k
    k = initial_token_a * initial_token_b

    # Calculate new reserves after price change
    # At equilibrium: current_token_b = current_token_a × current_price
    # current_token_a × (current_token_a × current_price) = k
    # current_token_a^2 = k / current_price
    current_token_a = math.sqrt(k / current_price)
    current_token_b = k / current_token_a

    # Calculate LP position value
    lp_value_usd = (current_token_a * current_price) + current_token_b

    # Calculate impermanent loss
    # Method 1: Using formula
    il_percent_formula = ((2 * math.sqrt(price_ratio)) / (1 + price_ratio) - 1) * 100

    # Method 2: Using actual values (should match)
    il_percent = (lp_value_usd / hodl_value_usd - 1) * 100
    il_usd = lp_value_usd - hodl_value_usd

    # Calculate net profit if fee income provided
    net_profit_usd = None
    net_profit_percent = None
    if fee_income_usd is not None:
        net_profit_usd = fee_income_usd + il_usd  # il_usd is negative
        net_profit_percent = (net_profit_usd / initial_value_usd) * 100

    return ImpermanentLossResult(
        initial_price=initial_price,
        current_price=current_price,
        price_ratio=price_ratio,
        price_change_percent=price_change_percent,
        initial_token_a=initial_token_a,
        initial_token_b=initial_token_b,
        current_token_a=current_token_a,
        current_token_b=current_token_b,
        initial_value_usd=initial_value_usd,
        lp_value_usd=lp_value_usd,
        hodl_value_usd=hodl_value_usd,
        il_percent=il_percent,
        il_usd=il_usd,
        fee_income_usd=fee_income_usd,
        net_profit_usd=net_profit_usd,
        net_profit_percent=net_profit_percent
    )


def simulate_il_price_range(
    self,
    initial_price: float,
    initial_token_a: float,
    initial_token_b: float,
    price_range_min: float,
    price_range_max: float,
    num_points: int = 50
) -> ILSimulationResult:
    """
    Simulate IL across a range of prices.

    Args:
        initial_price: Starting price
        initial_token_a: Initial token A amount
        initial_token_b: Initial token B amount
        price_range_min: Minimum price to simulate
        price_range_max: Maximum price to simulate
        num_points: Number of price points to calculate

    Returns:
        ILSimulationResult with IL data for each price point

    Example:
        Simulate IL for ETH price from $1,000 to $5,000
        Shows how IL changes across price range
    """
    price_step = (price_range_max - price_range_min) / (num_points - 1)
    price_scenarios = []
    il_percentages = []
    lp_values = []
    hodl_values = []

    for i in range(num_points):
        price = price_range_min + (i * price_step)
        price_scenarios.append(price)

        # Calculate IL at this price
        il_result = self.calculate_impermanent_loss(
            initial_price=initial_price,
            current_price=price,
            initial_token_a=initial_token_a,
            initial_token_b=initial_token_b
        )

        il_percentages.append(il_result.il_percent)
        lp_values.append(il_result.lp_value_usd)
        hodl_values.append(il_result.hodl_value_usd)

    return ILSimulationResult(
        price_scenarios=price_scenarios,
        il_percentages=il_percentages,
        lp_values=lp_values,
        hodl_values=hodl_values,
        break_even_price=initial_price
    )


def calculate_il_break_even(
    self,
    initial_price: float,
    current_price: float,
    initial_token_a: float,
    initial_token_b: float,
    fee_apr: float,
    volume_tvl_ratio: float
) -> ILBreakEvenAnalysis:
    """
    Calculate how long it takes for fees to offset impermanent loss.

    Args:
        initial_price: Starting price
        current_price: Current price
        initial_token_a: Initial token A amount
        initial_token_b: Initial token B amount
        fee_apr: Annual fee percentage (e.g., 0.003 = 0.3%)
        volume_tvl_ratio: Daily volume/TVL ratio (e.g., 0.5 = 50%)

    Returns:
        ILBreakEvenAnalysis with days to break even

    Example:
        ETH 2x (IL = -5.72%)
        Fee: 0.3%, Volume/TVL: 50%
        Daily fees: 0.3% × 50% = 0.15%
        Days to break even: 5.72% / 0.15% = 38 days
    """
    # Calculate IL
    il_result = self.calculate_impermanent_loss(
        initial_price=initial_price,
        current_price=current_price,
        initial_token_a=initial_token_a,
        initial_token_b=initial_token_b
    )

    il_percent = abs(il_result.il_percent)
    il_usd = abs(il_result.il_usd)

    # Calculate daily fee rate
    # Daily fees = fee_tier × daily_volume
    # Daily volume = TVL × volume_tvl_ratio
    # So: daily_fee_rate = fee_apr × volume_tvl_ratio
    daily_fee_rate = fee_apr * volume_tvl_ratio

    # Calculate days to break even
    if daily_fee_rate > 0:
        days_to_break_even = (il_percent / 100) / daily_fee_rate
    else:
        days_to_break_even = float('inf')

    fees_needed_usd = il_usd

    return ILBreakEvenAnalysis(
        il_percent=il_percent,
        il_usd=il_usd,
        fee_apr=fee_apr,
        volume_tvl_ratio=volume_tvl_ratio,
        days_to_break_even=days_to_break_even,
        fees_needed_usd=fees_needed_usd
    )


def calculate_il_by_price_change(self, price_change_percent: float) -> float:
    """
    Quick IL calculation given a price change percentage.

    Args:
        price_change_percent: Price change % (e.g., 100 for 2x, -50 for 0.5x)

    Returns:
        Impermanent loss percentage

    Formula:
        price_ratio = 1 + (price_change_percent / 100)
        IL% = (2 × √price_ratio) / (1 + price_ratio) - 1

    Examples:
        +100% (2x):   -5.72%
        +200% (3x):   -13.40%
        -50% (0.5x):  -5.72%
    """
    price_ratio = 1 + (price_change_percent / 100)

    if price_ratio <= 0:
        raise ValueError("Price ratio must be positive")

    il_percent = ((2 * math.sqrt(price_ratio)) / (1 + price_ratio) - 1) * 100

    return il_percent
```

---

### Step 3: Add API Endpoints

Add to `routes/liquidity.py`:

```python
from pydantic import BaseModel, Field
from src.models.defi_types import (
    ImpermanentLossResult,
    ILSimulationResult,
    ILBreakEvenAnalysis
)

# --- Request Models ---

class ImpermanentLossRequest(BaseModel):
    """Request for IL calculation"""
    initial_price: float = Field(..., gt=0, description="Initial token price")
    current_price: float = Field(..., gt=0, description="Current token price")
    initial_token_a: float = Field(..., gt=0, description="Initial amount of token A")
    initial_token_b: float = Field(..., gt=0, description="Initial amount of token B")
    fee_income_usd: Optional[float] = Field(None, ge=0, description="Total fees earned (optional)")


class ILSimulationRequest(BaseModel):
    """Request for IL simulation"""
    initial_price: float = Field(..., gt=0, description="Starting price")
    initial_token_a: float = Field(..., gt=0, description="Initial token A")
    initial_token_b: float = Field(..., gt=0, description="Initial token B")
    price_range_min: float = Field(..., gt=0, description="Minimum price")
    price_range_max: float = Field(..., gt=0, description="Maximum price")
    num_points: int = Field(50, ge=10, le=200, description="Number of price points")


class ILBreakEvenRequest(BaseModel):
    """Request for IL break-even analysis"""
    initial_price: float = Field(..., gt=0)
    current_price: float = Field(..., gt=0)
    initial_token_a: float = Field(..., gt=0)
    initial_token_b: float = Field(..., gt=0)
    fee_apr: float = Field(..., gt=0, le=0.1, description="Fee tier (e.g., 0.003 = 0.3%)")
    volume_tvl_ratio: float = Field(..., gt=0, le=10, description="Daily volume/TVL ratio")


# --- Endpoints ---

@router.post("/impermanent-loss", response_model=dict)
async def calculate_impermanent_loss(request: ImpermanentLossRequest):
    """
    Calculate impermanent loss for a liquidity position.

    Compares LP position value to HODL value and calculates:
    - Current token holdings in the pool
    - LP position value vs HODL value
    - Impermanent loss percentage and USD amount
    - Net profit if fee income provided

    Example:
        Initial: 1 ETH + $2,000 USDC at ETH = $2,000
        Current: ETH = $4,000
        Returns: IL = -5.72%, LP = $5,656, HODL = $6,000
    """
    try:
        result = analyzer.calculate_impermanent_loss(
            initial_price=request.initial_price,
            current_price=request.current_price,
            initial_token_a=request.initial_token_a,
            initial_token_b=request.initial_token_b,
            fee_income_usd=request.fee_income_usd
        )

        return {
            "impermanent_loss": {
                "price_info": {
                    "initial_price": result.initial_price,
                    "current_price": result.current_price,
                    "price_ratio": round(result.price_ratio, 4),
                    "price_change_percent": round(result.price_change_percent, 2)
                },
                "holdings": {
                    "initial": {
                        "token_a": result.initial_token_a,
                        "token_b": result.initial_token_b,
                        "value_usd": result.initial_value_usd
                    },
                    "current_lp": {
                        "token_a": round(result.current_token_a, 6),
                        "token_b": round(result.current_token_b, 2),
                        "value_usd": round(result.lp_value_usd, 2)
                    },
                    "if_hodl": {
                        "token_a": result.initial_token_a,
                        "token_b": result.initial_token_b,
                        "value_usd": round(result.hodl_value_usd, 2)
                    }
                },
                "impermanent_loss": {
                    "percent": round(result.il_percent, 2),
                    "usd": round(result.il_usd, 2)
                },
                "fee_analysis": {
                    "fee_income_usd": result.fee_income_usd,
                    "net_profit_usd": round(result.net_profit_usd, 2) if result.net_profit_usd else None,
                    "net_profit_percent": round(result.net_profit_percent, 2) if result.net_profit_percent else None
                } if request.fee_income_usd else None
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/il-simulation", response_model=dict)
async def simulate_il(request: ILSimulationRequest):
    """
    Simulate impermanent loss across a price range.

    Returns IL percentages, LP values, and HODL values
    for multiple price points.

    Useful for visualizing IL risk across different scenarios.
    """
    try:
        result = analyzer.simulate_il_price_range(
            initial_price=request.initial_price,
            initial_token_a=request.initial_token_a,
            initial_token_b=request.initial_token_b,
            price_range_min=request.price_range_min,
            price_range_max=request.price_range_max,
            num_points=request.num_points
        )

        # Format for response (round values)
        scenarios = []
        for i in range(len(result.price_scenarios)):
            scenarios.append({
                "price": round(result.price_scenarios[i], 2),
                "il_percent": round(result.il_percentages[i], 2),
                "lp_value": round(result.lp_values[i], 2),
                "hodl_value": round(result.hodl_values[i], 2)
            })

        return {
            "simulation": {
                "break_even_price": result.break_even_price,
                "num_scenarios": len(scenarios),
                "scenarios": scenarios
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/il-break-even", response_model=dict)
async def calculate_break_even(request: ILBreakEvenRequest):
    """
    Calculate how long it takes for fees to offset IL.

    Analyzes:
    - Current impermanent loss
    - Expected daily fee income
    - Days needed to break even

    Example:
        IL = -5.72%, Fee = 0.3%, Volume/TVL = 50%
        Daily fees = 0.15%, Days to break even = 38 days
    """
    try:
        result = analyzer.calculate_il_break_even(
            initial_price=request.initial_price,
            current_price=request.current_price,
            initial_token_a=request.initial_token_a,
            initial_token_b=request.initial_token_b,
            fee_apr=request.fee_apr,
            volume_tvl_ratio=request.volume_tvl_ratio
        )

        daily_fee_rate = request.fee_apr * request.volume_tvl_ratio

        return {
            "break_even_analysis": {
                "impermanent_loss": {
                    "percent": round(result.il_percent, 2),
                    "usd": round(result.il_usd, 2)
                },
                "fee_parameters": {
                    "fee_tier": request.fee_apr,
                    "volume_tvl_ratio": request.volume_tvl_ratio,
                    "daily_fee_rate": round(daily_fee_rate * 100, 4)
                },
                "break_even": {
                    "days_to_break_even": round(result.days_to_break_even, 2),
                    "fees_needed_usd": round(result.fees_needed_usd, 2)
                }
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/il-reference", response_model=dict)
async def get_il_reference():
    """
    Get reference table of IL by price change.

    Returns common IL scenarios for quick reference.
    """
    reference_data = [
        {"price_change": "0%", "price_ratio": 1.0, "il_percent": 0.0},
        {"price_change": "+25%", "price_ratio": 1.25, "il_percent": -0.62},
        {"price_change": "+50%", "price_ratio": 1.5, "il_percent": -2.02},
        {"price_change": "+100% (2x)", "price_ratio": 2.0, "il_percent": -5.72},
        {"price_change": "+200% (3x)", "price_ratio": 3.0, "il_percent": -13.40},
        {"price_change": "+300% (4x)", "price_ratio": 4.0, "il_percent": -20.00},
        {"price_change": "+400% (5x)", "price_ratio": 5.0, "il_percent": -25.46},
        {"price_change": "-25%", "price_ratio": 0.75, "il_percent": -0.62},
        {"price_change": "-50%", "price_ratio": 0.5, "il_percent": -5.72},
        {"price_change": "-75%", "price_ratio": 0.25, "il_percent": -20.00}
    ]

    return {
        "il_reference_table": reference_data,
        "formula": "IL% = (2 × √price_ratio) / (1 + price_ratio) - 1",
        "note": "IL is symmetric - same loss for equal ratio changes up or down"
    }
```

---

## Testing with curl

### Test 1: Calculate IL for ETH 2x Price Increase

**Scenario**: Deposited 1 ETH + $2,000 USDC at $2,000, ETH now $4,000

```bash
curl -X POST http://localhost:8000/api/liquidity/impermanent-loss \
  -H "Content-Type: application/json" \
  -d '{
    "initial_price": 2000,
    "current_price": 4000,
    "initial_token_a": 1.0,
    "initial_token_b": 2000
  }'
```

**Expected Response**:
```json
{
  "impermanent_loss": {
    "price_info": {
      "initial_price": 2000.0,
      "current_price": 4000.0,
      "price_ratio": 2.0,
      "price_change_percent": 100.0
    },
    "holdings": {
      "initial": {
        "token_a": 1.0,
        "token_b": 2000.0,
        "value_usd": 4000.0
      },
      "current_lp": {
        "token_a": 0.707107,
        "token_b": 2828.43,
        "value_usd": 5656.85
      },
      "if_hodl": {
        "token_a": 1.0,
        "token_b": 2000.0,
        "value_usd": 6000.0
      }
    },
    "impermanent_loss": {
      "percent": -5.72,
      "usd": -343.15
    },
    "fee_analysis": null
  }
}
```

**Analysis**:
- Started with: 1 ETH + $2,000 USDC = $4,000
- LP now has: 0.707 ETH + $2,828 USDC = $5,656
- If held: 1 ETH ($4,000) + $2,000 = $6,000
- **IL: -$343 (-5.72%)**
- Lost out on ETH gains due to pool rebalancing

---

### Test 2: IL with Fee Income (Profitable)

**Scenario**: Same as above, but earned $400 in fees

```bash
curl -X POST http://localhost:8000/api/liquidity/impermanent-loss \
  -H "Content-Type: application/json" \
  -d '{
    "initial_price": 2000,
    "current_price": 4000,
    "initial_token_a": 1.0,
    "initial_token_b": 2000,
    "fee_income_usd": 400
  }'
```

**Expected Response**:
```json
{
  "impermanent_loss": {
    "price_info": {
      "initial_price": 2000.0,
      "current_price": 4000.0,
      "price_ratio": 2.0,
      "price_change_percent": 100.0
    },
    "holdings": {
      "initial": {
        "token_a": 1.0,
        "token_b": 2000.0,
        "value_usd": 4000.0
      },
      "current_lp": {
        "token_a": 0.707107,
        "token_b": 2828.43,
        "value_usd": 5656.85
      },
      "if_hodl": {
        "token_a": 1.0,
        "token_b": 2000.0,
        "value_usd": 6000.0
      }
    },
    "impermanent_loss": {
      "percent": -5.72,
      "usd": -343.15
    },
    "fee_analysis": {
      "fee_income_usd": 400.0,
      "net_profit_usd": 56.85,
      "net_profit_percent": 1.42
    }
  }
}
```

**Analysis**:
- IL: -$343
- Fees: +$400
- **Net Profit: +$57 (+1.42%)**
- Fees outweighed IL - providing liquidity was profitable!

---

### Test 3: IL Simulation Across Price Range

**Scenario**: Simulate IL for ETH from $1,000 to $5,000

```bash
curl -X POST http://localhost:8000/api/liquidity/il-simulation \
  -H "Content-Type: application/json" \
  -d '{
    "initial_price": 2000,
    "initial_token_a": 1.0,
    "initial_token_b": 2000,
    "price_range_min": 1000,
    "price_range_max": 5000,
    "num_points": 10
  }'
```

**Expected Response** (abbreviated):
```json
{
  "simulation": {
    "break_even_price": 2000.0,
    "num_scenarios": 10,
    "scenarios": [
      {
        "price": 1000.0,
        "il_percent": -5.72,
        "lp_value": 2828.43,
        "hodl_value": 3000.0
      },
      {
        "price": 1444.44,
        "il_percent": -2.63,
        "lp_value": 3394.11,
        "hodl_value": 3488.89
      },
      {
        "price": 2000.0,
        "il_percent": 0.0,
        "lp_value": 4000.0,
        "hodl_value": 4000.0
      },
      {
        "price": 2555.56,
        "il_percent": -1.56,
        "lp_value": 4538.05,
        "hodl_value": 4611.11
      },
      {
        "price": 3000.0,
        "il_percent": -2.78,
        "lp_value": 4898.98,
        "hodl_value": 5040.0
      },
      {
        "price": 4000.0,
        "il_percent": -5.72,
        "lp_value": 5656.85,
        "hodl_value": 6000.0
      },
      {
        "price": 5000.0,
        "il_percent": -8.53,
        "lp_value": 6324.56,
        "hodl_value": 7000.0
      }
    ]
  }
}
```

**Analysis**:
- At $2,000 (initial price): IL = 0%
- At $1,000 (-50%): IL = -5.72%
- At $4,000 (+100%): IL = -5.72%
- At $5,000 (+150%): IL = -8.53%
- IL increases as price deviates from initial price

---

### Test 4: Break-Even Analysis

**Scenario**: How long to recover -5.72% IL with 0.3% fees?

```bash
curl -X POST http://localhost:8000/api/liquidity/il-break-even \
  -H "Content-Type: application/json" \
  -d '{
    "initial_price": 2000,
    "current_price": 4000,
    "initial_token_a": 1.0,
    "initial_token_b": 2000,
    "fee_apr": 0.003,
    "volume_tvl_ratio": 0.5
  }'
```

**Expected Response**:
```json
{
  "break_even_analysis": {
    "impermanent_loss": {
      "percent": 5.72,
      "usd": 343.15
    },
    "fee_parameters": {
      "fee_tier": 0.003,
      "volume_tvl_ratio": 0.5,
      "daily_fee_rate": 0.15
    },
    "break_even": {
      "days_to_break_even": 38.13,
      "fees_needed_usd": 343.15
    }
  }
}
```

**Analysis**:
- IL: -5.72% (-$343)
- Fee tier: 0.3%
- Daily volume: 50% of TVL
- Daily fee rate: 0.3% × 50% = **0.15%/day**
- **Break-even: 38 days**
- After 38 days, fees will offset IL completely

---

### Test 5: Get IL Reference Table

```bash
curl -X GET http://localhost:8000/api/liquidity/il-reference
```

**Expected Response**:
```json
{
  "il_reference_table": [
    {"price_change": "0%", "price_ratio": 1.0, "il_percent": 0.0},
    {"price_change": "+25%", "price_ratio": 1.25, "il_percent": -0.62},
    {"price_change": "+50%", "price_ratio": 1.5, "il_percent": -2.02},
    {"price_change": "+100% (2x)", "price_ratio": 2.0, "il_percent": -5.72},
    {"price_change": "+200% (3x)", "price_ratio": 3.0, "il_percent": -13.40},
    {"price_change": "+300% (4x)", "price_ratio": 4.0, "il_percent": -20.00},
    {"price_change": "+400% (5x)", "price_ratio": 5.0, "il_percent": -25.46},
    {"price_change": "-25%", "price_ratio": 0.75, "il_percent": -0.62},
    {"price_change": "-50%", "price_ratio": 0.5, "il_percent": -5.72},
    {"price_change": "-75%", "price_ratio": 0.25, "il_percent": -20.00}
  ],
  "formula": "IL% = (2 × √price_ratio) / (1 + price_ratio) - 1",
  "note": "IL is symmetric - same loss for equal ratio changes up or down"
}
```

---

## Common Issues

### Issue 1: IL is Negative Even Though Position Value Increased

**Symptom**:
```json
{
  "lp_value_usd": 5656.85,     # Increased from $4,000
  "il_percent": -5.72           # Negative IL
}
```

**Cause**: IL measures **relative** loss vs HODL, not absolute gain.

**Explanation**:
- Your LP position DID increase ($4,000 → $5,656)
- But HODL would have been better ($6,000)
- IL = -5.72% means you lost 5.72% relative to HODL

**This is expected behavior**, not a bug.

---

### Issue 2: IL Same for Price Up and Down

**Symptom**: IL is -5.72% whether ETH goes 2x or 0.5x.

**Cause**: IL formula is symmetric.

**Explanation**:
```
Price 2x (ratio = 2):   IL = -5.72%
Price 0.5x (ratio = 0.5): IL = -5.72%
```

This is mathematically correct. IL depends on price **divergence**, not direction.

---

### Issue 3: Break-Even Time is Infinity

**Symptom**:
```json
{
  "days_to_break_even": "Infinity"
}
```

**Cause**: `volume_tvl_ratio` is 0 (no trading volume).

**Fix**: Pool must have trading volume to earn fees.

```bash
# Bad: No volume
"volume_tvl_ratio": 0.0  # No fees earned

# Good: 50% daily volume
"volume_tvl_ratio": 0.5  # Fees earned
```

---

### Issue 4: Net Profit is Null

**Symptom**:
```json
{
  "net_profit_usd": null,
  "net_profit_percent": null
}
```

**Cause**: `fee_income_usd` not provided in request.

**Fix**: Include fee income to calculate net profit:

```bash
curl -X POST http://localhost:8000/api/liquidity/impermanent-loss \
  -H "Content-Type: application/json" \
  -d '{
    ...
    "fee_income_usd": 400  # Add this
  }'
```

---

## Key Takeaways

### What We Learned Today

1. **IL is Opportunity Cost**: It's the difference between LP value and HODL value.

2. **IL Formula**: `IL% = (2 × √price_ratio) / (1 + price_ratio) - 1`
   - 2x price change: -5.72% IL
   - 3x price change: -13.40% IL
   - 5x price change: -25.46% IL

3. **IL is Symmetric**: Same loss whether price goes up or down by same ratio.

4. **Fees Can Offset IL**: If fees > |IL|, providing liquidity is profitable.

5. **Break-Even Analysis**: Calculate `days = IL% / (fee_tier × volume_tvl_ratio)`

6. **IL is "Impermanent"**: Only if price returns to initial price, or you stay in pool long enough for fees to compensate.

### When to Provide Liquidity

**Favorable Conditions**:
- High volume/TVL ratio (>30%)
- Stable price pairs (stablecoins, correlated assets)
- High fee tiers (1% for exotic pairs)
- Long-term commitment (more time to earn fees)

**Unfavorable Conditions**:
- Volatile price pairs (ETH/meme tokens)
- Low volume pools (<10% volume/TVL)
- Short time horizon
- Expecting major price movements

### Real-World Strategy

**Conservative LP**: Stick to stablecoin pools (USDC/USDT, DAI/USDC)
- IL ≈ 0% (prices don't diverge)
- Earn fees risk-free

**Moderate LP**: Use correlated pairs (ETH/stETH, WBTC/renBTC)
- IL < 2% (prices move together)
- Higher fees than stablecoins

**Aggressive LP**: High volatility pairs (ETH/USDC, ETH/alts)
- IL can be 10-20%+
- Must earn high fees to compensate

---

### Tomorrow (Day 010)

We'll tackle **Uniswap V3 Concentrated Liquidity**, where LPs can:
- Provide liquidity in specific price ranges
- Earn 100-1000x more fees per dollar
- Face amplified IL if price moves out of range

**Preview**:
- Price range positions (e.g., ETH $2,000-$3,000)
- Capital efficiency calculation
- Out-of-range risk analysis
- Position rebalancing strategies

---

## Summary

**Files Modified**:
1. `/src/models/defi_types.py` - Added `ImpermanentLossResult`, `ILSimulationResult`, `ILBreakEvenAnalysis`
2. `/src/analytics/liquidity_analyzer.py` - Added 5 IL calculation functions
3. `/routes/liquidity.py` - Added 4 new endpoints

**New API Endpoints**:
- `POST /api/liquidity/impermanent-loss` - Calculate IL with optional fee analysis
- `POST /api/liquidity/il-simulation` - Simulate IL across price range
- `POST /api/liquidity/il-break-even` - Calculate days to recover IL with fees
- `GET /api/liquidity/il-reference` - Get IL reference table

**Key Functions**:
- `calculate_impermanent_loss()` - Full IL analysis with fee comparison
- `simulate_il_price_range()` - IL simulation for multiple price points
- `calculate_il_break_even()` - Break-even time analysis
- `calculate_il_by_price_change()` - Quick IL lookup by price change %

**Testing**: 5 curl examples covering IL calculation, fee analysis, simulation, break-even, and reference data.

**Day 009 Complete!** ✅

Tomorrow: Uniswap V3 concentrated liquidity! 🎯
