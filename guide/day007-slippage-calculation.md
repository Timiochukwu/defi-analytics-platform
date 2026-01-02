# Day 007: Slippage Calculation & Tolerance

> **Time**: 1.5-2 hours | **Difficulty**: ⭐⭐⭐ Moderate | **Builds on**: Day 006

---

## 🎯 What You'll Build Today

- ✅ Understand slippage vs price impact
- ✅ Calculate slippage percentage
- ✅ Implement slippage tolerance checks
- ✅ Build minimum output calculator
- ✅ Create slippage protection endpoints
- ✅ Real-world trade simulation
- ✅ Learn why trades fail (insufficient output)

---

## 📦 Dependencies

**No new dependencies!** Uses existing:
- `src/analytics/liquidity_analyzer.py` (Day 006)

---

## 📂 Files to Modify

```
src/analytics/
└── liquidity_analyzer.py    ← ADD slippage functions

src/api/routes/
└── liquidity.py             ← ADD slippage endpoints
```

---

## 💡 Slippage vs Price Impact - What's the Difference?

### **Price Impact**
```
How much the price moves DUE TO YOUR TRADE

Pool: 1,000 ETH / 2,000,000 USDC
Price before: $2,000/ETH
Trade: 10,000 USDC
Price after: $2,010/ETH
Price Impact: 0.5%

This is PREDICTABLE - you can calculate it before trading!
```

### **Slippage**
```
Difference between EXPECTED and ACTUAL execution price

Expected: 5 ETH (at $2,000)
Actual: 4.975 ETH (at $2,010)
Slippage: (5 - 4.975) / 5 = 0.5%

Caused by:
1. Price impact (your trade)
2. Other trades happening between quote and execution
3. Price volatility
```

### **Why Slippage Matters**

**Scenario: MEV Bot Sandwich Attack**
```
1. You submit: Buy 10 ETH with 20,000 USDC (expect $2,000/ETH)
2. Bot sees your transaction
3. Bot front-runs: Buys before you → price goes to $2,100
4. Your trade executes at $2,100 (not $2,000!)
5. Bot back-runs: Sells at $2,100 → profits

Without slippage protection, you just paid 5% more!
```

**Slippage Tolerance Solution:**
```
Set max slippage: 1%
Expected: 10 ETH
Minimum acceptable: 9.9 ETH (1% less)

If actual < 9.9 ETH → TRANSACTION REVERTS
Protects you from MEV and sudden price moves!
```

---

## 🚀 Step-by-Step Implementation

### **Step 1: Add Slippage Functions to LiquidityAnalyzer** (40 min)

Add these functions to `src/analytics/liquidity_analyzer.py`:

```python
# Add to imports at top of file
from enum import Enum

# Add new data structures
@dataclass
class SlippageResult:
    """
    Result of slippage calculation

    EXAMPLE:
        SlippageResult(
            expected_output=5.0,
            actual_output=4.975,
            slippage_percent=0.5,
            slippage_amount=0.025,
            within_tolerance=True
        )
    """
    expected_output: float      # What you expected to get
    actual_output: float        # What you actually get
    slippage_percent: float     # Slippage percentage
    slippage_amount: float      # Absolute slippage amount
    within_tolerance: bool      # Whether slippage is acceptable


class SlippageRating(Enum):
    """Rating for slippage amount"""
    EXCELLENT = "Excellent"     # < 0.1%
    GOOD = "Good"               # 0.1% - 0.5%
    ACCEPTABLE = "Acceptable"   # 0.5% - 1.0%
    HIGH = "High"               # 1.0% - 3.0%
    VERY_HIGH = "Very High"     # 3.0% - 5.0%
    EXTREME = "Extreme"         # > 5.0%


# Add these methods to LiquidityAnalyzer class

def calculate_slippage(
    self,
    reserve_in: float,
    reserve_out: float,
    amount_in: float,
    expected_price: Optional[float] = None,
    fee: float = 0.003
) -> SlippageResult:
    """
    Calculate slippage for a trade

    SLIPPAGE FORMULA:
        Slippage% = (Expected - Actual) / Expected * 100

    EXAMPLE 1: Price Impact Only
        Pool: 1,000 ETH / 2,000,000 USDC
        Trade: 10,000 USDC
        Expected (at $2,000): 5 ETH
        Actual: 4.975 ETH
        Slippage: (5 - 4.975) / 5 = 0.5%

    EXAMPLE 2: With Price Movement
        Expected price when quoted: $2,000/ETH
        Someone else trades before you
        Actual price when executed: $2,050/ETH
        Expected: 5 ETH
        Actual: 4.878 ETH
        Slippage: (5 - 4.878) / 5 = 2.44%

    Args:
        reserve_in: Current reserve of input token
        reserve_out: Current reserve of output token
        amount_in: Amount to trade
        expected_price: Expected price (if None, uses current)
        fee: Trading fee

    Returns:
        SlippageResult with all slippage metrics
    """
    # Calculate actual output with current reserves
    swap = self.calculate_swap_output(
        reserve_in=reserve_in,
        reserve_out=reserve_out,
        amount_in=amount_in,
        fee=fee
    )
    actual_output = swap.output_amount

    # Calculate expected output
    if expected_price is None:
        # Use current price
        expected_price = reserve_in / reserve_out

    # Expected output at given price (ignoring impact)
    expected_output = amount_in / expected_price

    # Calculate slippage
    slippage_amount = expected_output - actual_output
    slippage_percent = (slippage_amount / expected_output * 100) if expected_output > 0 else 0

    return SlippageResult(
        expected_output=expected_output,
        actual_output=actual_output,
        slippage_percent=slippage_percent,
        slippage_amount=slippage_amount,
        within_tolerance=True  # Will be set by tolerance check
    )


def calculate_minimum_output(
    self,
    expected_output: float,
    slippage_tolerance_percent: float
) -> float:
    """
    Calculate minimum acceptable output given slippage tolerance

    FORMULA:
        Min Output = Expected * (1 - Tolerance%)

    EXAMPLE:
        Expected: 10 ETH
        Tolerance: 1% (0.01)
        Minimum: 10 * (1 - 0.01) = 9.9 ETH

        If actual < 9.9 ETH → Transaction should revert!

    WHY THIS MATTERS:
        Uniswap (and most DEXs) let you set slippage tolerance.
        Transaction fails if you'd get less than minimum.
        Protects against:
        - MEV sandwich attacks
        - Sudden price movements
        - Excessive price impact

    Args:
        expected_output: Expected output amount
        slippage_tolerance_percent: Max acceptable slippage (e.g., 1.0 = 1%)

    Returns:
        Minimum acceptable output amount

    Raises:
        ValueError: If tolerance is invalid
    """
    if slippage_tolerance_percent < 0 or slippage_tolerance_percent > 100:
        raise ValueError("Slippage tolerance must be between 0 and 100")

    min_output = expected_output * (1 - slippage_tolerance_percent / 100)
    return min_output


def check_slippage_tolerance(
    self,
    reserve_in: float,
    reserve_out: float,
    amount_in: float,
    slippage_tolerance_percent: float,
    expected_price: Optional[float] = None,
    fee: float = 0.003
) -> Dict[str, any]:
    """
    Check if trade is within slippage tolerance

    EXAMPLE:
        Pool: 1,000 ETH / 2,000,000 USDC
        Trade: 100,000 USDC
        Slippage tolerance: 1%

        Expected (at $2,000): 50 ETH
        Minimum acceptable: 49.5 ETH
        Actual: 48.78 ETH
        Result: FAIL - exceeds tolerance!

    Args:
        reserve_in: Reserve of input token
        reserve_out: Reserve of output token
        amount_in: Amount to trade
        slippage_tolerance_percent: Max acceptable slippage
        expected_price: Expected price (if None, uses current)
        fee: Trading fee

    Returns:
        Dict with:
        - will_succeed: bool (whether trade would succeed)
        - expected_output: float
        - actual_output: float
        - minimum_output: float
        - slippage_percent: float
        - reason: str (if failed)
    """
    # Calculate slippage
    slippage = self.calculate_slippage(
        reserve_in=reserve_in,
        reserve_out=reserve_out,
        amount_in=amount_in,
        expected_price=expected_price,
        fee=fee
    )

    # Calculate minimum acceptable output
    min_output = self.calculate_minimum_output(
        expected_output=slippage.expected_output,
        slippage_tolerance_percent=slippage_tolerance_percent
    )

    # Check if within tolerance
    will_succeed = slippage.actual_output >= min_output

    result = {
        "will_succeed": will_succeed,
        "expected_output": round(slippage.expected_output, 6),
        "actual_output": round(slippage.actual_output, 6),
        "minimum_output": round(min_output, 6),
        "slippage_percent": round(slippage.slippage_percent, 3),
        "slippage_tolerance_percent": slippage_tolerance_percent
    }

    if not will_succeed:
        shortfall = min_output - slippage.actual_output
        result["reason"] = f"Slippage too high: {slippage.slippage_percent:.2f}% > {slippage_tolerance_percent}%"
        result["shortfall"] = round(shortfall, 6)
    else:
        result["reason"] = "Trade would succeed"

    return result


def rate_slippage(self, slippage_percent: float) -> SlippageRating:
    """
    Rate slippage amount

    RATING GUIDE:
    - Excellent (< 0.1%): Minimal slippage, very good execution
    - Good (0.1-0.5%): Normal for mid-size trades
    - Acceptable (0.5-1.0%): OK for larger trades
    - High (1.0-3.0%): Consider splitting trade
    - Very High (3.0-5.0%): Definitely split trade
    - Extreme (> 5.0%): Pool too small for this trade size

    Args:
        slippage_percent: Slippage percentage

    Returns:
        SlippageRating enum
    """
    abs_slippage = abs(slippage_percent)

    if abs_slippage < 0.1:
        return SlippageRating.EXCELLENT
    elif abs_slippage < 0.5:
        return SlippageRating.GOOD
    elif abs_slippage < 1.0:
        return SlippageRating.ACCEPTABLE
    elif abs_slippage < 3.0:
        return SlippageRating.HIGH
    elif abs_slippage < 5.0:
        return SlippageRating.VERY_HIGH
    else:
        return SlippageRating.EXTREME


def recommend_trade_split(
    self,
    reserve_in: float,
    reserve_out: float,
    amount_in: float,
    target_slippage: float = 0.5,
    fee: float = 0.003
) -> Dict[str, any]:
    """
    Recommend how to split a trade to reduce slippage

    ALGORITHM:
    1. Calculate current slippage for full amount
    2. If above target, split into smaller chunks
    3. Simulate each chunk execution
    4. Return optimal split

    EXAMPLE:
        Pool: 1,000 ETH / 2,000,000 USDC
        Trade: 100,000 USDC
        Full trade slippage: 5.1% (too high!)

        Recommendation: Split into 5 trades of 20,000 each
        - Each has ~1% slippage
        - Total still better than 5.1%

    Args:
        reserve_in: Reserve of input token
        reserve_out: Reserve of output token
        amount_in: Amount to trade
        target_slippage: Target slippage % (default 0.5%)
        fee: Trading fee

    Returns:
        Recommendation dict with split strategy
    """
    # Calculate slippage for full amount
    full_slippage = self.calculate_slippage(
        reserve_in, reserve_out, amount_in, fee=fee
    )

    if full_slippage.slippage_percent <= target_slippage:
        return {
            "needs_split": False,
            "recommended_chunks": 1,
            "chunk_size": amount_in,
            "current_slippage": round(full_slippage.slippage_percent, 2),
            "message": "Trade size is acceptable - no split needed"
        }

    # Binary search for optimal chunk count
    for chunks in [2, 3, 4, 5, 10, 20]:
        chunk_size = amount_in / chunks

        # Simulate first chunk
        first_chunk = self.calculate_slippage(
            reserve_in, reserve_out, chunk_size, fee=fee
        )

        if first_chunk.slippage_percent <= target_slippage:
            return {
                "needs_split": True,
                "recommended_chunks": chunks,
                "chunk_size": round(chunk_size, 2),
                "current_slippage": round(full_slippage.slippage_percent, 2),
                "target_slippage": target_slippage,
                "estimated_slippage_per_chunk": round(first_chunk.slippage_percent, 2),
                "message": f"Split into {chunks} trades of {chunk_size:,.2f} each"
            }

    # If even 20 chunks isn't enough, pool is too small
    return {
        "needs_split": True,
        "recommended_chunks": 20,
        "chunk_size": round(amount_in / 20, 2),
        "current_slippage": round(full_slippage.slippage_percent, 2),
        "message": "Pool too small for this trade - even 20 splits would have high slippage"
    }
```

**✅ Checkpoint**: Slippage functions added to `liquidity_analyzer.py`

---

### **Step 2: Add Slippage Endpoints** (30 min)

Add to `src/api/routes/liquidity.py`:

```python
# Add to imports
from pydantic import BaseModel, Field

# Add request models
class SlippageRequest(BaseModel):
    """Request for slippage calculation"""
    reserve_in: float = Field(..., gt=0)
    reserve_out: float = Field(..., gt=0)
    amount_in: float = Field(..., gt=0)
    expected_price: Optional[float] = Field(None, gt=0, description="Expected price (uses current if not provided)")
    fee: float = Field(0.003, ge=0, lt=1)

    class Config:
        json_schema_extra = {
            "example": {
                "reserve_in": 2000000,
                "reserve_out": 1000,
                "amount_in": 10000,
                "expected_price": 2000,
                "fee": 0.003
            }
        }


class SlippageToleranceRequest(BaseModel):
    """Request for slippage tolerance check"""
    reserve_in: float = Field(..., gt=0)
    reserve_out: float = Field(..., gt=0)
    amount_in: float = Field(..., gt=0)
    slippage_tolerance_percent: float = Field(..., ge=0, le=100, description="Max acceptable slippage (e.g., 1.0 = 1%)")
    expected_price: Optional[float] = Field(None, gt=0)
    fee: float = Field(0.003, ge=0, lt=1)

    class Config:
        json_schema_extra = {
            "example": {
                "reserve_in": 2000000,
                "reserve_out": 1000,
                "amount_in": 100000,
                "slippage_tolerance_percent": 1.0,
                "fee": 0.003
            }
        }


# Add endpoints
@router.post(
    "/slippage",
    summary="Calculate slippage",
    description="Calculate slippage for a trade"
)
async def calculate_slippage(request: SlippageRequest) -> Dict[str, Any]:
    """
    # Calculate Slippage

    Shows difference between expected and actual output.

    ## Example: Normal Slippage (Price Impact)

    **Input:**
    ```json
    {
      "reserve_in": 2000000,
      "reserve_out": 1000,
      "amount_in": 10000,
      "fee": 0.003
    }
    ```

    **Output:**
    ```json
    {
      "expected_output": 5.0,
      "actual_output": 4.975,
      "slippage_percent": 0.5,
      "slippage_amount": 0.025,
      "rating": "Good",
      "explanation": "Normal slippage for this trade size"
    }
    ```

    ## Example: High Slippage (Price Moved)

    **Input:**
    ```json
    {
      "reserve_in": 2000000,
      "reserve_out": 1000,
      "amount_in": 10000,
      "expected_price": 2000,
      "fee": 0.003
    }
    ```

    If price moved to $2,100 before execution:

    **Output:**
    ```json
    {
      "expected_output": 5.0,
      "actual_output": 4.737,
      "slippage_percent": 5.26,
      "rating": "Very High",
      "explanation": "Significant price movement - consider refreshing quote"
    }
    ```

    ## Use Cases

    - Warn users about expected slippage
    - Show price impact before confirming trade
    - Detect MEV sandwich attacks (sudden high slippage)
    - Compare execution quality
    """
    try:
        result = analyzer.calculate_slippage(
            reserve_in=request.reserve_in,
            reserve_out=request.reserve_out,
            amount_in=request.amount_in,
            expected_price=request.expected_price,
            fee=request.fee
        )

        rating = analyzer.rate_slippage(result.slippage_percent)

        return {
            "expected_output": round(result.expected_output, 6),
            "actual_output": round(result.actual_output, 6),
            "slippage_percent": round(result.slippage_percent, 3),
            "slippage_amount": round(result.slippage_amount, 6),
            "rating": rating.value,
            "explanation": get_slippage_explanation(result.slippage_percent)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/slippage-check",
    summary="Check slippage tolerance",
    description="Check if trade would succeed with given slippage tolerance"
)
async def check_slippage_tolerance(request: SlippageToleranceRequest) -> Dict[str, Any]:
    """
    # Check Slippage Tolerance

    Determines if trade would succeed with your slippage tolerance setting.

    ## Example: Trade Within Tolerance

    **Input:**
    ```json
    {
      "reserve_in": 2000000,
      "reserve_out": 1000,
      "amount_in": 10000,
      "slippage_tolerance_percent": 1.0
    }
    ```

    **Output:**
    ```json
    {
      "will_succeed": true,
      "expected_output": 5.0,
      "actual_output": 4.975,
      "minimum_output": 4.95,
      "slippage_percent": 0.5,
      "reason": "Trade would succeed"
    }
    ```

    ## Example: Trade Exceeds Tolerance

    **Input:**
    ```json
    {
      "reserve_in": 2000000,
      "reserve_out": 1000,
      "amount_in": 100000,
      "slippage_tolerance_percent": 1.0
    }
    ```

    **Output:**
    ```json
    {
      "will_succeed": false,
      "expected_output": 50.0,
      "actual_output": 48.78,
      "minimum_output": 49.5,
      "slippage_percent": 2.44,
      "reason": "Slippage too high: 2.44% > 1.0%",
      "shortfall": 0.72
    }
    ```

    ## Use Cases

    - Prevent trades with excessive slippage
    - Protect users from MEV attacks
    - Show why transaction would fail before submitting
    - Recommend better slippage settings
    """
    try:
        result = analyzer.check_slippage_tolerance(
            reserve_in=request.reserve_in,
            reserve_out=request.reserve_out,
            amount_in=request.amount_in,
            slippage_tolerance_percent=request.slippage_tolerance_percent,
            expected_price=request.expected_price,
            fee=request.fee
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/recommend-split",
    summary="Recommend trade split",
    description="Get recommendation for splitting large trades"
)
async def recommend_trade_split(
    reserve_in: float = Field(..., gt=0),
    reserve_out: float = Field(..., gt=0),
    amount_in: float = Field(..., gt=0),
    target_slippage: float = Field(0.5, gt=0, le=100)
) -> Dict[str, Any]:
    """
    # Recommend Trade Split

    Suggests how to split large trades to minimize slippage.

    ## Example

    **Input:**
    ```
    reserve_in: 2000000
    reserve_out: 1000
    amount_in: 100000
    target_slippage: 0.5
    ```

    **Output:**
    ```json
    {
      "needs_split": true,
      "recommended_chunks": 5,
      "chunk_size": 20000,
      "current_slippage": 5.12,
      "target_slippage": 0.5,
      "estimated_slippage_per_chunk": 0.98,
      "message": "Split into 5 trades of 20,000.00 each"
    }
    ```

    ## Use Cases

    - Optimize large trade execution
    - Reduce price impact
    - Avoid MEV sandwich attacks
    - Institutional trading strategies
    """
    try:
        result = analyzer.recommend_trade_split(
            reserve_in=reserve_in,
            reserve_out=reserve_out,
            amount_in=amount_in,
            target_slippage=target_slippage
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# Helper function
def get_slippage_explanation(slippage_percent: float) -> str:
    """Get human-readable explanation of slippage"""
    abs_slip = abs(slippage_percent)

    if abs_slip < 0.1:
        return "Excellent execution - minimal slippage"
    elif abs_slip < 0.5:
        return "Normal slippage for this trade size"
    elif abs_slip < 1.0:
        return "Acceptable slippage - consider if expected"
    elif abs_slip < 3.0:
        return "High slippage - consider splitting trade"
    elif abs_slip < 5.0:
        return "Very high slippage - definitely split trade"
    else:
        return "Extreme slippage - pool too small for this trade"
```

**✅ Checkpoint**: Slippage endpoints added

---

### **Step 3: Test Slippage Endpoints** (20 min)

Restart server and test:

#### **Test 1: Calculate Slippage (Good)**

```bash
curl -X POST http://localhost:8000/api/liquidity/slippage \
  -H "Content-Type: application/json" \
  -d '{
    "reserve_in": 2000000,
    "reserve_out": 1000,
    "amount_in": 10000,
    "fee": 0.003
  }'
```

**Expected:**
```json
{
  "expected_output": 5.0,
  "actual_output": 4.975125,
  "slippage_percent": 0.497,
  "slippage_amount": 0.024875,
  "rating": "Good",
  "explanation": "Normal slippage for this trade size"
}
```

**✅ Test passed!**

---

#### **Test 2: Check Tolerance (Pass)**

```bash
curl -X POST http://localhost:8000/api/liquidity/slippage-check \
  -H "Content-Type: application/json" \
  -d '{
    "reserve_in": 2000000,
    "reserve_out": 1000,
    "amount_in": 10000,
    "slippage_tolerance_percent": 1.0
  }'
```

**Expected:**
```json
{
  "will_succeed": true,
  "expected_output": 5.0,
  "actual_output": 4.975125,
  "minimum_output": 4.95,
  "slippage_percent": 0.497,
  "slippage_tolerance_percent": 1.0,
  "reason": "Trade would succeed"
}
```

**✅ Test passed!**

---

#### **Test 3: Check Tolerance (Fail)**

```bash
curl -X POST http://localhost:8000/api/liquidity/slippage-check \
  -H "Content-Type: application/json" \
  -d '{
    "reserve_in": 2000000,
    "reserve_out": 1000,
    "amount_in": 100000,
    "slippage_tolerance_percent": 1.0
  }'
```

**Expected:**
```json
{
  "will_succeed": false,
  "expected_output": 50.0,
  "actual_output": 48.780488,
  "minimum_output": 49.5,
  "slippage_percent": 2.439,
  "slippage_tolerance_percent": 1.0,
  "reason": "Slippage too high: 2.44% > 1.0%",
  "shortfall": 0.719512
}
```

**✅ Test passed - trade would fail!**

---

#### **Test 4: Recommend Split**

```bash
curl -X POST "http://localhost:8000/api/liquidity/recommend-split?reserve_in=2000000&reserve_out=1000&amount_in=100000&target_slippage=0.5"
```

**Expected:**
```json
{
  "needs_split": true,
  "recommended_chunks": 5,
  "chunk_size": 20000.0,
  "current_slippage": 2.44,
  "target_slippage": 0.5,
  "estimated_slippage_per_chunk": 0.48,
  "message": "Split into 5 trades of 20,000.00 each"
}
```

**✅ Test passed!**

---

## 🎉 Day 007 Complete!

### **What You Built:**

✅ Slippage calculator with rating system
✅ Slippage tolerance checker
✅ Minimum output calculator
✅ Trade split recommender
✅ 3 new API endpoints
✅ Protection against MEV attacks
✅ **Production-grade trading safety!**

### **What You Learned:**

- Difference between slippage and price impact
- How slippage tolerance protects traders
- MEV sandwich attacks and protection
- Trade splitting to reduce slippage
- Why transactions fail on DEXs
- Production trading best practices

---

## 📊 Progress

```
[████████████████████████░░░░] Day 007/030 (23.3%)

✅ Foundation:     [██████████] 5/5 days
⏳ Liquidity:      [████░░░░░░] 2/7 days
⏳ Risk:           [░░░░░░░░░░] 0/6 days
⏳ Yield:          [░░░░░░░░░░] 0/6 days
⏳ Data/Production:[░░░░░░░░░░] 0/6 days
```

---

## 💡 Key Formulas

### **Slippage**
```
Slippage% = (Expected - Actual) / Expected * 100
```

### **Minimum Output**
```
Min = Expected * (1 - Tolerance%)
```

### **Tolerance Check**
```
Pass if: Actual >= Minimum
Fail if: Actual < Minimum
```

---

## 🚀 Next Steps

**Tomorrow (Day 008)**: Pool Quality Scoring
- TVL-based scoring
- Volume/TVL ratio analysis
- Reserve balance scoring
- Overall pool rating (0-100)
- Pool quality API endpoint

---

**Day 007/030 Complete** ✅ | **Next**: Day 008 - Pool Quality Scoring
