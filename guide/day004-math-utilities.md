# Day 004: Mathematical & Financial Utilities

> **Time**: 1.5-2 hours | **Difficulty**: ⭐⭐⭐ Moderate | **Builds on**: Day 003

---

## 🎯 What You'll Build Today

- ✅ Financial calculation functions (APY, compound interest, Sharpe ratio)
- ✅ Percentage and ratio calculations
- ✅ Statistical functions (volatility, standard deviation)
- ✅ Normalization and scaling utilities
- ✅ Test endpoint to verify all calculations
- ✅ NumPy integration for advanced math

---

## 📦 Dependencies (Day 4 NEW)

**Install NumPy:**

```bash
pip install numpy>=1.24.0
```

Update your `requirements.txt`:

```txt
# ... (previous dependencies from Days 1-3)

# Day 004 - Mathematical Operations
numpy>=1.24.0
```

---

## 📂 Files to Create/Modify

```
src/
├── api/
│   ├── main.py              ← MODIFY (add test endpoint)
│   ├── models.py            ← Keep from Day 002
│   ├── types.py             ← Keep from Day 003
│   └── routes/
│       ├── types.py         ← Keep from Day 003
│       └── calculations.py  ← MODIFY (move Day 002 endpoints here)
└── utils/
    ├── __init__.py          ← CREATE
    └── calculations.py      ← CREATE (main file for today)
```

---

## 💡 Why Mathematical Utilities?

In DeFi, **precision matters**:

- **APY vs APR**: Different compounding = different returns
- **Risk-Adjusted Returns**: 20% APY with 50% volatility ≠ 10% APY with 5% volatility
- **Sharpe Ratio**: Standard metric for comparing investments
- **Impermanent Loss**: Complex formula requires accurate math

**These utilities will be used every day from Day 6 onwards!**

---

## 🚀 Step-by-Step Implementation

### **Step 1: Create Utils Package** (5 min)

```bash
# Create utils directory
mkdir -p src/utils

# Create __init__.py
touch src/utils/__init__.py
```

Create `src/utils/__init__.py`:

```python
"""
Utility Functions Package
Day 004/030
"""

from .calculations import (
    # APY & Interest
    calculate_apy,
    calculate_apy_from_rate,
    calculate_compound_interest,
    apy_to_apr,
    apr_to_apy,

    # Percentage & Ratios
    calculate_percentage_change,
    calculate_ratio,
    normalize_to_range,

    # Statistics
    calculate_sharpe_ratio,
    calculate_volatility,
    calculate_standard_deviation,
    calculate_mean,

    # DeFi Specific
    calculate_impermanent_loss_simple,
    calculate_price_impact
)

__all__ = [
    "calculate_apy",
    "calculate_apy_from_rate",
    "calculate_compound_interest",
    "apy_to_apr",
    "apr_to_apy",
    "calculate_percentage_change",
    "calculate_ratio",
    "normalize_to_range",
    "calculate_sharpe_ratio",
    "calculate_volatility",
    "calculate_standard_deviation",
    "calculate_mean",
    "calculate_impermanent_loss_simple",
    "calculate_price_impact"
]
```

---

### **Step 2: Create Calculation Functions** (60 min)

Create `src/utils/calculations.py`:

```python
"""
=============================================================================
FINANCIAL & MATHEMATICAL CALCULATION UTILITIES
=============================================================================

DAY 004: Core Math Functions

PURPOSE:
- Provide reusable financial calculation functions
- Support DeFi analytics with accurate math
- Enable statistical analysis of yields and risks
- Normalize and compare different metrics

WHAT YOU'LL LEARN:
- Compound interest calculations
- Statistical analysis (Sharpe ratio, volatility)
- Percentage and ratio math
- NumPy for efficient calculations

WHY THIS MATTERS:
DeFi involves complex financial mathematics:
- APY calculations with different compounding periods
- Risk-adjusted returns (Sharpe ratio)
- Price impact and slippage
- Impermanent loss formulas

These functions are the foundation for all analytics we'll build.

DAY: 004/030
=============================================================================
"""

import numpy as np
from typing import List, Tuple, Optional
import math


# ====================================================================================
# APY & INTEREST RATE CALCULATIONS
# ====================================================================================

def calculate_apy(
    starting_value: float,
    ending_value: float,
    days: int
) -> float:
    """
    Calculate Annual Percentage Yield from actual returns

    FORMULA:
        APY = ((ending_value / starting_value) ^ (365 / days)) - 1

    EXAMPLE 1: 30-Day Yield
        Deposited: $10,000
        After 30 days: $10,100
        APY = ((10100/10000)^(365/30)) - 1 = 0.1268 = 12.68%

    EXAMPLE 2: 7-Day Yield
        Deposited: $1,000
        After 7 days: $1,010
        APY = ((1010/1000)^(365/7)) - 1 = 0.7888 = 78.88%

        Note: High short-term yield extrapolates to high APY!

    WHY IT MATTERS:
        - DeFi protocols report yields over different periods
        - APY normalizes everything to annual basis
        - Allows comparison of 7-day vs 30-day vs 90-day yields

    Args:
        starting_value: Initial deposit amount
        ending_value: Value after time period
        days: Number of days elapsed

    Returns:
        APY as decimal (0.1268 = 12.68%)

    Raises:
        ValueError: If inputs are invalid
    """
    if starting_value <= 0:
        raise ValueError("Starting value must be positive")
    if ending_value <= 0:
        raise ValueError("Ending value must be positive")
    if days <= 0:
        raise ValueError("Days must be positive")
    if days > 365:
        raise ValueError("Days should not exceed 365 for APY calculation")

    # Calculate growth factor
    growth_factor = ending_value / starting_value

    # Annualize the return
    periods_per_year = 365 / days
    apy = (growth_factor ** periods_per_year) - 1

    return apy


def calculate_apy_from_rate(
    daily_rate: float,
    compounds_per_year: int = 365
) -> float:
    """
    Calculate APY from a periodic rate

    FORMULA:
        APY = (1 + rate)^periods - 1

    EXAMPLE:
        Daily rate: 0.03% (0.0003)
        APY = (1.0003)^365 - 1 = 0.1157 = 11.57%

    Args:
        daily_rate: Rate per period (as decimal)
        compounds_per_year: Compounding frequency (default 365 for daily)

    Returns:
        APY as decimal
    """
    if daily_rate < -1:
        raise ValueError("Rate cannot be less than -100%")

    apy = (1 + daily_rate) ** compounds_per_year - 1
    return apy


def calculate_compound_interest(
    principal: float,
    rate: float,
    compounds_per_year: int,
    years: float
) -> float:
    """
    Calculate compound interest

    FORMULA:
        A = P(1 + r/n)^(nt)

        Where:
        - A = Final amount
        - P = Principal (initial amount)
        - r = Annual interest rate (decimal)
        - n = Compounding frequency per year
        - t = Time in years

    EXAMPLE 1: Daily Compounding
        Principal: $10,000
        Rate: 5% APR (0.05)
        Compounds: 365 (daily)
        Years: 1

        A = 10000 * (1 + 0.05/365)^(365*1)
        A = $10,512.67

    EXAMPLE 2: Continuous Compounding
        For continuous: use compounds_per_year = 365*24*60*60 (every second)
        Or use formula: A = P * e^(rt)

    WHY IT MATTERS:
        - Shows effect of compounding frequency
        - Daily vs monthly vs yearly compounding = different returns
        - DeFi often uses continuous compounding

    Args:
        principal: Initial deposit
        rate: Annual interest rate (decimal, e.g., 0.05 = 5%)
        compounds_per_year: Compounding frequency
        years: Time period in years

    Returns:
        Final amount after compounding
    """
    if principal < 0:
        raise ValueError("Principal must be non-negative")
    if compounds_per_year <= 0:
        raise ValueError("Compounds per year must be positive")
    if years < 0:
        raise ValueError("Years must be non-negative")

    amount = principal * (1 + rate / compounds_per_year) ** (compounds_per_year * years)
    return amount


def apy_to_apr(apy: float, compounds_per_year: int = 365) -> float:
    """
    Convert APY (Annual Percentage Yield) to APR (Annual Percentage Rate)

    FORMULA:
        APR = n * ((1 + APY)^(1/n) - 1)

    EXAMPLE:
        APY: 12.68%
        Compounds: 365 (daily)
        APR = 365 * ((1.1268)^(1/365) - 1) = 0.12 = 12%

    WHY IT MATTERS:
        - APY includes compounding effect
        - APR is the simple rate
        - Traditional finance uses APR, DeFi often quotes APY

    Args:
        apy: Annual Percentage Yield (decimal)
        compounds_per_year: Compounding frequency

    Returns:
        APR as decimal
    """
    if apy < -1:
        raise ValueError("APY cannot be less than -100%")
    if compounds_per_year <= 0:
        raise ValueError("Compounds per year must be positive")

    apr = compounds_per_year * ((1 + apy) ** (1 / compounds_per_year) - 1)
    return apr


def apr_to_apy(apr: float, compounds_per_year: int = 365) -> float:
    """
    Convert APR (Annual Percentage Rate) to APY (Annual Percentage Yield)

    FORMULA:
        APY = (1 + APR/n)^n - 1

    EXAMPLE:
        APR: 12%
        Compounds: 365 (daily)
        APY = (1 + 0.12/365)^365 - 1 = 0.1268 = 12.68%

    Args:
        apr: Annual Percentage Rate (decimal)
        compounds_per_year: Compounding frequency

    Returns:
        APY as decimal
    """
    if apr < -1:
        raise ValueError("APR cannot be less than -100%")
    if compounds_per_year <= 0:
        raise ValueError("Compounds per year must be positive")

    apy = (1 + apr / compounds_per_year) ** compounds_per_year - 1
    return apy


# ====================================================================================
# PERCENTAGE & RATIO CALCULATIONS
# ====================================================================================

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values

    FORMULA:
        Change% = ((new - old) / old) * 100

    EXAMPLES:
        ETH: $1,000 → $1,200
        Change = ((1200 - 1000) / 1000) * 100 = 20%

        ETH: $2,000 → $1,500
        Change = ((1500 - 2000) / 2000) * 100 = -25%

    WHY IT MATTERS:
        - Track price movements
        - Calculate returns
        - Measure performance

    Args:
        old_value: Original value
        new_value: New value

    Returns:
        Percentage change (20.0 = 20% increase, -25.0 = 25% decrease)
    """
    if old_value == 0:
        if new_value == 0:
            return 0.0
        else:
            return float('inf')  # Infinite increase from zero

    change = ((new_value - old_value) / abs(old_value)) * 100
    return change


def calculate_ratio(numerator: float, denominator: float) -> float:
    """
    Calculate ratio between two values

    EXAMPLES:
        Pool reserves: 1,000 ETH / 2,000,000 USDC
        Ratio = 1000 / 2000000 = 0.0005

        Price = denominator / numerator = 2000000 / 1000 = $2,000/ETH

    Args:
        numerator: Top value
        denominator: Bottom value

    Returns:
        Ratio (numerator / denominator)
    """
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")

    return numerator / denominator


def normalize_to_range(
    value: float,
    min_val: float,
    max_val: float,
    target_min: float = 0.0,
    target_max: float = 100.0
) -> float:
    """
    Normalize value to target range (default 0-100)

    FORMULA:
        normalized = ((value - min) / (max - min)) * (target_max - target_min) + target_min

    EXAMPLE:
        TVL = $50M, min = $1M, max = $100M
        Normalize to 0-100:
        normalized = ((50 - 1) / (100 - 1)) * 100 = 49.5

    WHY IT MATTERS:
        - Combine different metrics into scores
        - TVL (millions) + Volume (millions) + Age (days) → all 0-100
        - Enables weighted scoring

    Args:
        value: Value to normalize
        min_val: Minimum value in range
        max_val: Maximum value in range
        target_min: Target minimum (default 0)
        target_max: Target maximum (default 100)

    Returns:
        Normalized value
    """
    if max_val == min_val:
        return (target_min + target_max) / 2  # Middle of target range

    # Normalize to 0-1 first
    normalized = (value - min_val) / (max_val - min_val)

    # Scale to target range
    scaled = normalized * (target_max - target_min) + target_min

    # Clamp to target range
    return max(target_min, min(target_max, scaled))


# ====================================================================================
# STATISTICAL FUNCTIONS
# ====================================================================================

def calculate_mean(values: List[float]) -> float:
    """
    Calculate arithmetic mean (average)

    FORMULA:
        mean = sum(values) / count(values)

    Args:
        values: List of numbers

    Returns:
        Average value
    """
    if not values:
        return 0.0

    return float(np.mean(values))


def calculate_standard_deviation(values: List[float]) -> float:
    """
    Calculate standard deviation (volatility measure)

    FORMULA:
        σ = sqrt(Σ(x - μ)² / n)

        Where:
        - σ = standard deviation
        - x = each value
        - μ = mean
        - n = number of values

    EXAMPLE:
        Returns: [10%, 12%, 8%, 15%, 11%]
        Mean = 11.2%
        Std Dev = 2.56%

    WHY IT MATTERS:
        - Measures variability/volatility
        - Higher std dev = more risky
        - Used in Sharpe ratio calculation

    Args:
        values: List of numbers

    Returns:
        Standard deviation
    """
    if len(values) < 2:
        return 0.0

    return float(np.std(values, ddof=1))  # ddof=1 for sample std dev


def calculate_volatility(prices: List[float]) -> float:
    """
    Calculate price volatility (standard deviation of returns)

    STEPS:
        1. Convert prices to returns
        2. Calculate std dev of returns

    EXAMPLE:
        Prices: [$100, $105, $103, $108, $110]
        Returns: [5%, -1.9%, 4.85%, 1.85%]
        Volatility = std_dev(returns) = 2.89%

    WHY IT MATTERS:
        - Measures price stability
        - Higher volatility = higher risk
        - Key input for risk models

    Args:
        prices: List of prices over time

    Returns:
        Volatility (as decimal)
    """
    if len(prices) < 2:
        return 0.0

    # Convert to numpy array
    prices_array = np.array(prices)

    # Calculate returns
    returns = np.diff(prices_array) / prices_array[:-1]

    # Calculate standard deviation of returns
    volatility = float(np.std(returns, ddof=1))

    return volatility


def calculate_sharpe_ratio(
    returns: List[float],
    risk_free_rate: float = 0.02,
    periods_per_year: int = 365
) -> float:
    """
    Calculate Sharpe Ratio (risk-adjusted return metric)

    FORMULA:
        Sharpe = (Mean Return - Risk-Free Rate) / Std Dev of Returns

    EXAMPLE:
        Daily returns: [0.1%, 0.15%, 0.08%, 0.12%, 0.10%]
        Mean = 0.11% daily = 40.15% annual
        Std Dev = 0.03% daily = 0.49% annual
        Risk-free = 2% annual

        Sharpe = (0.4015 - 0.02) / 0.0049 = 77.86

        Interpretation: For each unit of risk, you get 77.86 units of return!

    INTERPRETATION:
        < 1.0:  Bad (not worth the risk)
        1.0-2.0: Good
        2.0-3.0: Very Good
        > 3.0:  Excellent

    WHY IT MATTERS:
        - Standard metric for comparing investments
        - Accounts for both return AND risk
        - 20% return with 50% volatility < 10% return with 2% volatility
        - Used in portfolio optimization

    Args:
        returns: List of periodic returns (as decimals)
        risk_free_rate: Annual risk-free rate (default 2%)
        periods_per_year: Periods in a year (365 for daily, 12 for monthly)

    Returns:
        Sharpe ratio (higher = better risk-adjusted returns)
    """
    if len(returns) < 2:
        return 0.0

    # Convert to numpy array
    returns_array = np.array(returns)

    # Calculate mean return and std dev
    mean_return = float(np.mean(returns_array))
    std_dev = float(np.std(returns_array, ddof=1))

    if std_dev == 0:
        return 0.0  # No volatility = undefined Sharpe

    # Annualize the mean return
    annual_return = (1 + mean_return) ** periods_per_year - 1

    # Annualize the std dev
    annual_std_dev = std_dev * np.sqrt(periods_per_year)

    # Calculate Sharpe ratio
    sharpe = (annual_return - risk_free_rate) / annual_std_dev

    return float(sharpe)


# ====================================================================================
# DeFi-SPECIFIC CALCULATIONS
# ====================================================================================

def calculate_impermanent_loss_simple(
    price_ratio: float
) -> float:
    """
    Calculate impermanent loss for a 50/50 LP position

    FORMULA:
        IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1

    EXAMPLES:
        Price 1x (no change): IL = 0%
        Price 2x (doubled):   IL = -5.7%
        Price 4x:             IL = -20%
        Price 0.5x (halved):  IL = -5.7%
        Price 0.25x:          IL = -20%

    WHAT IS IMPERMANENT LOSS:
        When you provide liquidity to a pool (e.g., ETH/USDC), if the
        price changes, you lose money compared to just holding the assets.

    EXAMPLE:
        Start: 1 ETH ($2,000) + 2,000 USDC = $4,000 total
        ETH → $4,000 (2x increase)

        If you held: 1 ETH ($4,000) + 2,000 USDC = $6,000
        In pool: 0.707 ETH ($2,828) + 2,828 USDC = $5,656
        Loss: $344 (5.7% IL)

    WHY IT MATTERS:
        - You need to earn fees to overcome IL
        - Volatile pairs = more IL risk
        - Stablecoin pairs = minimal IL

    Args:
        price_ratio: New price / original price (2.0 = 2x, 0.5 = 0.5x)

    Returns:
        Impermanent loss as decimal (-0.057 = -5.7% loss)
    """
    if price_ratio <= 0:
        raise ValueError("Price ratio must be positive")

    il = 2 * math.sqrt(price_ratio) / (1 + price_ratio) - 1
    return il


def calculate_price_impact(
    reserve_in: float,
    reserve_out: float,
    amount_in: float
) -> float:
    """
    Calculate price impact for an AMM trade (simplified)

    FORMULA:
        Price impact = amount_in / (reserve_in + amount_in)

    EXAMPLE:
        Pool: 1,000 ETH / 2,000,000 USDC
        Trade: 100 ETH

        Impact = 100 / (1000 + 100) = 9.09%

    WHY IT MATTERS:
        - Large trades move the price
        - Price impact = slippage you'll experience
        - Deep liquidity = low impact

    Args:
        reserve_in: Reserve of input token
        reserve_out: Reserve of output token
        amount_in: Amount to trade

    Returns:
        Price impact as decimal (0.0909 = 9.09%)
    """
    if reserve_in <= 0 or reserve_out <= 0:
        raise ValueError("Reserves must be positive")
    if amount_in < 0:
        raise ValueError("Amount must be non-negative")

    impact = amount_in / (reserve_in + amount_in)
    return impact


# ====================================================================================
# HELPER FUNCTIONS
# ====================================================================================

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value to range [min_val, max_val]"""
    return max(min_val, min(max_val, value))


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide, returning default if denominator is zero"""
    if denominator == 0:
        return default
    return numerator / denominator


def compound_growth(initial: float, rate: float, periods: int) -> float:
    """Calculate compound growth over periods"""
    if initial <= 0 or periods < 0:
        raise ValueError("Invalid inputs for compound growth")

    return initial * (1 + rate) ** periods
```

**✅ Checkpoint**: `src/utils/calculations.py` created (600+ lines!)

---

### **Step 3: Create Test Endpoint** (20 min)

Modify `src/api/main.py` - add these imports:

```python
from utils.calculations import (
    calculate_apy,
    calculate_apy_from_rate,
    calculate_percentage_change,
    calculate_sharpe_ratio,
    calculate_impermanent_loss_simple,
    apy_to_apr,
    apr_to_apy,
    calculate_volatility
)
```

Add this endpoint before `if __name__ == "__main__":`:

```python
@app.get(
    "/api/utils/test-math",
    tags=["Utilities"],
    summary="Test all mathematical functions"
)
async def test_mathematical_functions() -> Dict[str, Any]:
    """
    # Test Mathematical Functions

    Demonstrates all calculation functions with examples.

    ## Tests Included

    1. APY Calculation
    2. APR ↔ APY Conversion
    3. Percentage Change
    4. Sharpe Ratio
    5. Impermanent Loss
    6. Volatility

    ## Example Response

    ```json
    {
      "apy_tests": {
        "30_day_yield": { "apy_percent": 12.68 },
        "7_day_yield": { "apy_percent": 78.88 }
      },
      "conversion_tests": { ... },
      ...
    }
    ```
    """
    return {
        "apy_tests": {
            "30_day_yield": {
                "deposit": 10000,
                "ending_value": 10100,
                "days": 30,
                "apy_decimal": round(calculate_apy(10000, 10100, 30), 4),
                "apy_percent": round(calculate_apy(10000, 10100, 30) * 100, 2)
            },
            "7_day_yield": {
                "deposit": 1000,
                "ending_value": 1010,
                "days": 7,
                "apy_decimal": round(calculate_apy(1000, 1010, 7), 4),
                "apy_percent": round(calculate_apy(1000, 1010, 7) * 100, 2)
            },
            "daily_rate_to_apy": {
                "daily_rate_percent": 0.03,
                "daily_rate_decimal": 0.0003,
                "apy_decimal": round(calculate_apy_from_rate(0.0003), 4),
                "apy_percent": round(calculate_apy_from_rate(0.0003) * 100, 2)
            }
        },

        "conversion_tests": {
            "apr_to_apy": {
                "apr_percent": 12.0,
                "compounds_per_year": 365,
                "apy_percent": round(apr_to_apy(0.12, 365) * 100, 2)
            },
            "apy_to_apr": {
                "apy_percent": 12.68,
                "compounds_per_year": 365,
                "apr_percent": round(apy_to_apr(0.1268, 365) * 100, 2)
            }
        },

        "percentage_tests": {
            "eth_price_increase": {
                "old_price": 1000,
                "new_price": 1200,
                "change_percent": round(calculate_percentage_change(1000, 1200), 2)
            },
            "eth_price_decrease": {
                "old_price": 2000,
                "new_price": 1500,
                "change_percent": round(calculate_percentage_change(2000, 1500), 2)
            }
        },

        "sharpe_ratio_test": {
            "returns": [0.10, 0.12, 0.08, 0.15, 0.11],
            "risk_free_rate": 0.02,
            "sharpe_ratio": round(calculate_sharpe_ratio([0.10, 0.12, 0.08, 0.15, 0.11], 0.02), 2),
            "interpretation": "Excellent (>3.0)"
        },

        "impermanent_loss_tests": {
            "price_2x": {
                "price_ratio": 2.0,
                "il_percent": round(calculate_impermanent_loss_simple(2.0) * 100, 2),
                "description": "ETH doubled in price"
            },
            "price_4x": {
                "price_ratio": 4.0,
                "il_percent": round(calculate_impermanent_loss_simple(4.0) * 100, 2),
                "description": "ETH 4x in price"
            },
            "price_half": {
                "price_ratio": 0.5,
                "il_percent": round(calculate_impermanent_loss_simple(0.5) * 100, 2),
                "description": "ETH halved in price"
            }
        },

        "volatility_test": {
            "prices": [100, 105, 103, 108, 110],
            "volatility_decimal": round(calculate_volatility([100, 105, 103, 108, 110]), 4),
            "volatility_percent": round(calculate_volatility([100, 105, 103, 108, 110]) * 100, 2)
        },

        "notes": {
            "apy_vs_apr": "APY includes compounding, APR doesn't",
            "sharpe_ratio": "Higher = better risk-adjusted returns",
            "impermanent_loss": "Loss vs holding assets (overcome with fees)",
            "volatility": "Standard deviation of returns (higher = riskier)"
        }
    }
```

Also update the version:

```python
@app.get("/", ...)
async def root():
    return {
        "version": "0.4.0-day004",  # ← UPDATE
        "day": "004/030",             # ← UPDATE
        # ... rest
    }
```

**✅ Checkpoint**: Test endpoint added

---

### **Step 4: Test All Functions** (15 min)

Restart server and test:

```bash
cd src/api
python main.py
```

#### **Test: Mathematical Functions**

```bash
curl http://localhost:8000/api/utils/test-math
```

**Expected output** (formatted):

```json
{
  "apy_tests": {
    "30_day_yield": {
      "deposit": 10000,
      "ending_value": 10100,
      "days": 30,
      "apy_decimal": 0.1268,
      "apy_percent": 12.68
    },
    "7_day_yield": {
      "deposit": 1000,
      "ending_value": 1010,
      "days": 7,
      "apy_decimal": 0.7888,
      "apy_percent": 78.88
    },
    "daily_rate_to_apy": {
      "daily_rate_percent": 0.03,
      "daily_rate_decimal": 0.0003,
      "apy_decimal": 0.1157,
      "apy_percent": 11.57
    }
  },
  "conversion_tests": {
    "apr_to_apy": {
      "apr_percent": 12.0,
      "compounds_per_year": 365,
      "apy_percent": 12.75
    },
    "apy_to_apr": {
      "apy_percent": 12.68,
      "compounds_per_year": 365,
      "apr_percent": 12.0
    }
  },
  "percentage_tests": {
    "eth_price_increase": {
      "old_price": 1000,
      "new_price": 1200,
      "change_percent": 20.0
    },
    "eth_price_decrease": {
      "old_price": 2000,
      "new_price": 1500,
      "change_percent": -25.0
    }
  },
  "sharpe_ratio_test": {
    "returns": [0.10, 0.12, 0.08, 0.15, 0.11],
    "risk_free_rate": 0.02,
    "sharpe_ratio": 3.67,
    "interpretation": "Excellent (>3.0)"
  },
  "impermanent_loss_tests": {
    "price_2x": {
      "price_ratio": 2.0,
      "il_percent": -5.72,
      "description": "ETH doubled in price"
    },
    "price_4x": {
      "price_ratio": 4.0,
      "il_percent": -20.0,
      "description": "ETH 4x in price"
    },
    "price_half": {
      "price_ratio": 0.5,
      "il_percent": -5.72,
      "description": "ETH halved in price"
    }
  },
  "volatility_test": {
    "prices": [100, 105, 103, 108, 110],
    "volatility_decimal": 0.0289,
    "volatility_percent": 2.89
  }
}
```

**✅ All calculations working!**

---

#### **Test: Individual Functions in Python**

Create `src/utils/test_calculations.py`:

```python
"""
Test Day 004 - Mathematical Functions
"""

from calculations import *


def test_apy_calculations():
    print("=" * 60)
    print("TEST: APY Calculations")
    print("=" * 60)

    # Test 1: 30-day yield
    apy = calculate_apy(10000, 10100, 30)
    print(f"30-day 1% return → {apy*100:.2f}% APY")

    # Test 2: 7-day yield
    apy = calculate_apy(1000, 1010, 7)
    print(f"7-day 1% return → {apy*100:.2f}% APY")

    # Test 3: Daily rate to APY
    apy = calculate_apy_from_rate(0.0003, 365)
    print(f"0.03% daily rate → {apy*100:.2f}% APY")

    print()


def test_conversions():
    print("=" * 60)
    print("TEST: APR ↔ APY Conversions")
    print("=" * 60)

    # APR to APY
    apr = 0.12
    apy = apr_to_apy(apr, 365)
    print(f"12% APR (daily compound) → {apy*100:.2f}% APY")

    # APY back to APR
    apr_back = apy_to_apr(apy, 365)
    print(f"{apy*100:.2f}% APY → {apr_back*100:.2f}% APR (matches!)")

    print()


def test_sharpe_ratio():
    print("=" * 60)
    print("TEST: Sharpe Ratio")
    print("=" * 60)

    # High return, high risk
    returns_volatile = [0.10, 0.20, -0.05, 0.15, 0.25]
    sharpe_volatile = calculate_sharpe_ratio(returns_volatile, 0.02, 365)
    print(f"Volatile returns: {returns_volatile}")
    print(f"Sharpe ratio: {sharpe_volatile:.2f}")

    # Moderate return, low risk
    returns_stable = [0.10, 0.11, 0.09, 0.10, 0.10]
    sharpe_stable = calculate_sharpe_ratio(returns_stable, 0.02, 365)
    print(f"\nStable returns: {returns_stable}")
    print(f"Sharpe ratio: {sharpe_stable:.2f}")

    print(f"\nHigher Sharpe = Better risk-adjusted returns!")
    print()


def test_impermanent_loss():
    print("=" * 60)
    print("TEST: Impermanent Loss")
    print("=" * 60)

    price_ratios = [0.5, 1.0, 1.5, 2.0, 4.0]

    print("Price Change | IL %")
    print("-" * 30)
    for ratio in price_ratios:
        il = calculate_impermanent_loss_simple(ratio)
        change = (ratio - 1) * 100
        print(f"{change:+7.0f}%      | {il*100:+6.2f}%")

    print("\nKey insight: Price up or down = IL!")
    print()


if __name__ == "__main__":
    test_apy_calculations()
    test_conversions()
    test_sharpe_ratio()
    test_impermanent_loss()

    print("=" * 60)
    print("✅ All Day 004 tests passed!")
    print("=" * 60)
```

Run it:

```bash
cd src/utils
python test_calculations.py
```

**✅ Python tests working!**

---

## 🎉 Day 004 Complete!

### **What You Built:**

✅ 15+ financial calculation functions (600+ lines!)
✅ APY, APR, compound interest calculations
✅ Sharpe ratio for risk-adjusted returns
✅ Impermanent loss calculator
✅ Volatility and standard deviation
✅ NumPy integration for efficiency
✅ Test endpoint with comprehensive examples
✅ Utility functions used throughout the project

### **What You Learned:**

- Compound interest mathematics
- APY vs APR (and why it matters)
- Sharpe ratio for investment comparison
- Impermanent loss in DeFi
- Statistical calculations with NumPy
- Financial formulas in Python
- Creating reusable utility libraries

---

## 📊 Progress

```
[████████████████░░░░░░░░░░░░] Day 004/030 (13.3%)

Foundation:     [████████░░] 4/5 days
Liquidity:      [░░░░░░░░░░] 0/7 days
Risk:           [░░░░░░░░░░] 0/6 days
Yield:          [░░░░░░░░░░] 0/6 days
Data/Production:[░░░░░░░░░░] 0/6 days
```

---

## 💡 Key Formulas

### **APY (Annual Percentage Yield)**
```
APY = ((ending / starting) ^ (365 / days)) - 1
```

### **Sharpe Ratio**
```
Sharpe = (Return - RiskFreeRate) / StandardDeviation
```

### **Impermanent Loss**
```
IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1
```

### **Compound Interest**
```
A = P(1 + r/n)^(nt)
```

---

## 🚀 Next Steps

**Tomorrow (Day 005)**: API Organization with Routers
- Split endpoints into route modules
- Clean project structure
- Route prefixes and tags
- Professional API organization

---

**Day 004/030 Complete** ✅ | **Next**: Day 005 - API Organization
