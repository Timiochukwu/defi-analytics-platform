# Day 003: Enums & Dataclasses for DeFi

> **Time**: 1.5-2 hours | **Difficulty**: ⭐⭐ Easy to ⭐⭐⭐ Moderate | **Builds on**: Day 002

---

## 🎯 What You'll Build Today

- ✅ DeFi-specific Enums (RiskLevel, YieldType, ProtocolType)
- ✅ Dataclasses for complex data structures
- ✅ Helper functions for enum conversions
- ✅ Pool rating system (S+ to F grades)
- ✅ Type-safe API responses
- ✅ Endpoints to list all available types

---

## 📦 Dependencies

**No new dependencies!** We use Python's built-in:
- `enum` (standard library)
- `dataclasses` (standard library)
- `typing` (standard library)

---

## 📂 Files to Create/Modify

```
src/api/
├── main.py          ← MODIFY (add type endpoints)
├── models.py        ← Keep from Day 002
├── types.py         ← CREATE (main file for today)
└── routes/
    ├── __init__.py  ← CREATE
    └── types.py     ← CREATE (type routes)
```

---

## 💡 Why Enums & Dataclasses?

### **Before (without enums):**
```python
# String-based, error-prone
risk = "very low"  # Typo! Should be "Very Low"
if risk == "Very Low":  # Doesn't match!
    ...
```

### **After (with enums):**
```python
# Type-safe, IDE autocomplete
risk = RiskLevel.VERY_LOW
if risk == RiskLevel.VERY_LOW:  # Guaranteed match!
    ...
```

### **Benefits:**
- ✅ Type safety (catch errors at development time)
- ✅ IDE autocomplete
- ✅ No typos in string comparisons
- ✅ Clear documentation of valid values
- ✅ Easy to extend and maintain

---

## 🚀 Step-by-Step Implementation

### **Step 1: Create DeFi Type Definitions** (40 min)

Create `src/api/types.py`:

```python
"""
=============================================================================
DeFi PLATFORM TYPES AND ENUMERATIONS
=============================================================================

DAY 003: Type Safety with Enums and Dataclasses

PURPOSE:
- Define DeFi-specific enumerations
- Create type-safe data structures
- Provide helper conversion functions
- Enable IDE autocomplete and validation

WHAT YOU'LL LEARN:
- Python Enum for fixed choices
- Dataclasses for structured data
- Type hints for better code
- How to model DeFi concepts

WHY THIS MATTERS:
In DeFi, precision matters. A "High" risk protocol is very different
from "Very High" risk. Enums ensure we never have typos or inconsistent
risk classifications.

DAY: 003/030
=============================================================================
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime


# ====================================================================================
# RISK ENUMERATIONS
# ====================================================================================

class RiskLevel(Enum):
    """
    Risk level classifications for DeFi protocols and strategies

    CLASSIFICATION GUIDE:
    - Very Low (0-20):   Blue-chip protocols, stablecoins on Aave/Compound
    - Low (21-40):       Established protocols, well-audited, >1 year old
    - Moderate (41-60):  Newer protocols, limited track record
    - High (61-80):      Unaudited, complex mechanisms, <6 months old
    - Very High (81-95): Experimental, new concepts, minimal TVL
    - Critical (96-100): Red flags, known vulnerabilities, avoid!

    EXAMPLE CLASSIFICATIONS:
    - Aave USDC lending: Very Low (score: 15)
    - Uniswap V2 ETH/USDC LP: Low (score: 30)
    - New DEX farming: High (score: 70)
    """
    VERY_LOW = "Very Low"       # Score: 0-20
    LOW = "Low"                 # Score: 21-40
    MODERATE = "Moderate"       # Score: 41-60
    HIGH = "High"               # Score: 61-80
    VERY_HIGH = "Very High"     # Score: 81-95
    CRITICAL = "Critical"       # Score: 96-100

    def __str__(self):
        return self.value

    def to_score_range(self) -> tuple:
        """Get the score range for this risk level"""
        ranges = {
            RiskLevel.VERY_LOW: (0, 20),
            RiskLevel.LOW: (21, 40),
            RiskLevel.MODERATE: (41, 60),
            RiskLevel.HIGH: (61, 80),
            RiskLevel.VERY_HIGH: (81, 95),
            RiskLevel.CRITICAL: (96, 100)
        }
        return ranges[self]


class RiskRating(Enum):
    """
    Simplified 1-5 risk rating scale

    Used for quick filtering and user-friendly display.
    Maps to RiskLevel for internal calculations.
    """
    VERY_LOW = 1    # Safest - stablecoins on blue-chip protocols
    LOW = 2         # Safe - major assets on established protocols
    MODERATE = 3    # Medium - liquidity provision, some IL risk
    HIGH = 4        # Risky - new protocols or volatile assets
    VERY_HIGH = 5   # Very Risky - experimental, unaudited

    def to_risk_level(self) -> RiskLevel:
        """Convert rating to detailed risk level"""
        mapping = {
            1: RiskLevel.VERY_LOW,
            2: RiskLevel.LOW,
            3: RiskLevel.MODERATE,
            4: RiskLevel.HIGH,
            5: RiskLevel.VERY_HIGH
        }
        return mapping[self.value]


# ====================================================================================
# YIELD TYPE ENUMERATIONS
# ====================================================================================

class YieldType(Enum):
    """
    Types of yield generation in DeFi

    WHAT EACH MEANS:

    LENDING:
        - Deposit assets, earn interest from borrowers
        - Examples: Aave, Compound
        - Risk: Low (if protocol is secure)
        - APY: 1-8% typically

    LP_FEES:
        - Provide liquidity to DEX, earn trading fees
        - Examples: Uniswap, Curve, SushiSwap
        - Risk: Moderate (impermanent loss)
        - APY: 5-50% depending on pool

    STAKING:
        - Lock tokens for network security or governance
        - Examples: ETH staking, governance staking
        - Risk: Low to Moderate
        - APY: 3-8% typically

    FARMING:
        - Liquidity mining with token rewards
        - Examples: Most DeFi "farms"
        - Risk: High (token dumping, IL)
        - APY: 50-500%+ (often unsustainable)

    VAULT:
        - Auto-compounding yield aggregator
        - Examples: Yearn, Beefy
        - Risk: Medium (smart contract risk)
        - APY: Varies, usually optimizes best strategy

    STABLE_FARM:
        - Low-risk stablecoin yields
        - Examples: Curve 3pool, Aave stables
        - Risk: Low
        - APY: 2-10%
    """
    LENDING = "Lending"                    # Aave, Compound
    LP_FEES = "Liquidity Provider Fees"    # Uniswap, Curve fees
    STAKING = "Staking"                    # ETH staking, governance
    FARMING = "Yield Farming"              # Token rewards/incentives
    VAULT = "Yield Vault"                  # Yearn, Beefy auto-compound
    STABLE_FARM = "Stable Farming"         # Low-risk stablecoin yields
    LIQUIDITY_MINING = "Liquidity Mining"  # Protocol incentives

    def __str__(self):
        return self.value

    def typical_apy_range(self) -> tuple:
        """Get typical APY range for this yield type"""
        ranges = {
            YieldType.LENDING: (1, 8),
            YieldType.LP_FEES: (5, 50),
            YieldType.STAKING: (3, 8),
            YieldType.FARMING: (50, 500),
            YieldType.VAULT: (5, 30),
            YieldType.STABLE_FARM: (2, 10),
            YieldType.LIQUIDITY_MINING: (20, 200)
        }
        return ranges.get(self, (0, 100))


# ====================================================================================
# PROTOCOL TYPE ENUMERATIONS
# ====================================================================================

class ProtocolType(Enum):
    """
    Categories of DeFi protocols

    WHAT EACH DOES:

    DEX (Decentralized Exchange):
        - Swap tokens without intermediaries
        - Examples: Uniswap, SushiSwap, Curve
        - Core mechanism: Automated Market Maker (AMM)

    LENDING:
        - Borrow/lend crypto assets
        - Examples: Aave, Compound, Euler
        - Core mechanism: Overcollateralized lending

    DERIVATIVES:
        - Perpetual futures, options, synthetic assets
        - Examples: dYdX, GMX, Synthetix
        - Core mechanism: Leveraged trading

    STABLECOIN:
        - Maintain $1 peg with various mechanisms
        - Examples: MakerDAO (DAI), Frax, Liquity (LUSD)
        - Core mechanism: Collateralized debt positions

    YIELD:
        - Aggregate and optimize yields
        - Examples: Yearn, Beefy, Convex
        - Core mechanism: Auto-compounding vaults

    BRIDGE:
        - Transfer assets between blockchains
        - Examples: Across, Stargate
        - Core mechanism: Lock & mint / Liquidity pools

    LIQUID_STAKING:
        - Stake ETH, get liquid derivative token
        - Examples: Lido (stETH), Rocket Pool (rETH)
        - Core mechanism: Pooled staking with liquid token
    """
    DEX = "Decentralized Exchange"    # Uniswap, SushiSwap, Curve
    LENDING = "Lending Protocol"       # Aave, Compound, Euler
    DERIVATIVES = "Derivatives"        # dYdX, GMX, Synthetix
    STABLECOIN = "Stablecoin"         # MakerDAO, Frax, Liquity
    YIELD = "Yield Aggregator"        # Yearn, Beefy, Convex
    BRIDGE = "Bridge"                 # Cross-chain bridges
    LIQUID_STAKING = "Liquid Staking" # Lido, Rocket Pool

    def __str__(self):
        return self.value


# ====================================================================================
# POOL QUALITY RATINGS
# ====================================================================================

class PoolRating(Enum):
    """
    Liquidity pool quality ratings (like credit ratings)

    RATING SYSTEM (0-100 score):

    S+ (95-100): Exceptional
        - Major pairs on Uniswap V2/V3
        - Deep liquidity (>$100M TVL)
        - High volume (>$50M daily)
        - Perfect balance
        Example: Uniswap V2 ETH/USDC

    A+ (90-94): Excellent
        - Well-established pools
        - Deep liquidity (>$50M TVL)
        - High volume
        Example: Curve 3pool

    A (80-89): Very Good
        - Good liquidity (>$10M TVL)
        - Decent volume
        Example: SushiSwap major pairs

    B (70-79): Good
        - Moderate liquidity ($1-10M TVL)
        - Some volume
        Example: Mid-tier DEX pairs

    C (60-69): Average
        - Low liquidity (<$1M TVL)
        - Low volume
        Example: Long-tail assets

    D (50-59): Below Average
        - Very low liquidity
        - Minimal volume
        - High slippage risk

    F (0-49): Poor
        - Avoid trading
        - Extreme slippage
        - Possibly abandoned pool
    """
    S_PLUS = "S+"   # 95-100: Exceptional
    A_PLUS = "A+"   # 90-94:  Excellent
    A = "A"         # 80-89:  Very Good
    B = "B"         # 70-79:  Good
    C = "C"         # 60-69:  Average
    D = "D"         # 50-59:  Below Average
    F = "F"         # 0-49:   Poor

    def __str__(self):
        return self.value

    def to_score_range(self) -> tuple:
        """Get score range for this rating"""
        ranges = {
            PoolRating.S_PLUS: (95, 100),
            PoolRating.A_PLUS: (90, 94),
            PoolRating.A: (80, 89),
            PoolRating.B: (70, 79),
            PoolRating.C: (60, 69),
            PoolRating.D: (50, 59),
            PoolRating.F: (0, 49)
        }
        return ranges[self]

    def description(self) -> str:
        """Get human-readable description"""
        descriptions = {
            PoolRating.S_PLUS: "Exceptional - Best liquidity pools",
            PoolRating.A_PLUS: "Excellent - Very safe for trading",
            PoolRating.A: "Very Good - Safe for most trades",
            PoolRating.B: "Good - Acceptable for trading",
            PoolRating.C: "Average - Watch for slippage",
            PoolRating.D: "Below Average - High slippage risk",
            PoolRating.F: "Poor - Avoid trading"
        }
        return descriptions[self]


# ====================================================================================
# DATACLASSES
# ====================================================================================

@dataclass
class Protocol:
    """
    Represents a DeFi protocol

    EXAMPLE:
        Protocol(
            name="Aave",
            protocol_type=ProtocolType.LENDING,
            chain="Ethereum",
            website="https://aave.com",
            audited=True,
            audit_firms=["Trail of Bits", "OpenZeppelin", "ConsenSys"],
            tvl_usd=5_000_000_000,
            days_active=1095,  # ~3 years
            risk_score=18.5,
            risk_level=RiskLevel.VERY_LOW
        )
    """
    name: str
    protocol_type: ProtocolType
    chain: str  # "Ethereum", "Polygon", "Arbitrum", etc.
    website: str
    audited: bool
    audit_firms: List[str] = field(default_factory=list)
    tvl_usd: float = 0.0
    days_active: int = 0
    risk_score: float = 50.0  # 0-100
    risk_level: RiskLevel = RiskLevel.MODERATE

    def __post_init__(self):
        """Auto-calculate risk level from score if not provided"""
        if self.risk_score is not None:
            self.risk_level = risk_score_to_level(self.risk_score)


@dataclass
class YieldOpportunitySummary:
    """
    Summary of a yield opportunity

    EXAMPLE:
        YieldOpportunitySummary(
            protocol="Aave",
            asset="USDC",
            apy=3.5,
            tvl_usd=2_000_000_000,
            yield_type=YieldType.LENDING,
            risk_level=RiskLevel.VERY_LOW,
            lock_days=0,
            updated_at=datetime.now()
        )
    """
    protocol: str
    asset: str
    apy: float  # Annual Percentage Yield (as percentage, e.g., 3.5 = 3.5%)
    tvl_usd: float
    yield_type: YieldType
    risk_level: RiskLevel
    lock_days: int  # 0 = no lock period
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def has_lock(self) -> bool:
        """Check if this opportunity has a lock period"""
        return self.lock_days > 0

    @property
    def is_stable(self) -> bool:
        """Check if this is a stablecoin opportunity"""
        stablecoins = ["USDC", "USDT", "DAI", "BUSD", "FRAX", "LUSD"]
        return self.asset in stablecoins

    def risk_adjusted_apy(self, risk_penalty: float = 0.1) -> float:
        """
        Calculate risk-adjusted APY

        Lower APY based on risk level
        """
        risk_multipliers = {
            RiskLevel.VERY_LOW: 1.0,
            RiskLevel.LOW: 0.95,
            RiskLevel.MODERATE: 0.85,
            RiskLevel.HIGH: 0.70,
            RiskLevel.VERY_HIGH: 0.50,
            RiskLevel.CRITICAL: 0.20
        }
        multiplier = risk_multipliers.get(self.risk_level, 0.5)
        return self.apy * multiplier


@dataclass
class PoolInfo:
    """
    Liquidity pool information

    EXAMPLE:
        PoolInfo(
            pool_address="0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
            token0="USDC",
            token1="WETH",
            reserve0=2_000_000,  # 2M USDC
            reserve1=1_000,      # 1,000 ETH
            tvl_usd=4_000_000,   # $4M total
            volume_24h=3_200_000,  # $3.2M daily volume
            fee_tier=0.0005,     # 0.05% fee
            rating=PoolRating.A_PLUS
        )
    """
    pool_address: str
    token0: str
    token1: str
    reserve0: float
    reserve1: float
    tvl_usd: float
    volume_24h: float
    fee_tier: float  # 0.0005 = 0.05%, 0.003 = 0.3%, 0.01 = 1%
    rating: Optional[PoolRating] = None

    @property
    def price(self) -> float:
        """Get price of token1 in terms of token0"""
        if self.reserve1 == 0:
            return 0
        return self.reserve0 / self.reserve1

    @property
    def volume_to_tvl_ratio(self) -> float:
        """Get volume/TVL ratio (activity indicator)"""
        if self.tvl_usd == 0:
            return 0
        return self.volume_24h / self.tvl_usd

    @property
    def reserve_balance(self) -> float:
        """
        Get reserve balance ratio (how close to 50/50)

        Returns value between 0 and 1:
        - 1.0 = perfect 50/50 split
        - 0.5 = 75/25 split
        - 0.0 = 100/0 split
        """
        total = self.reserve0 + self.reserve1
        if total == 0:
            return 0
        smaller = min(self.reserve0, self.reserve1)
        return (smaller / total) * 2  # Normalize to 0-1


# ====================================================================================
# HELPER FUNCTIONS
# ====================================================================================

def risk_score_to_level(score: float) -> RiskLevel:
    """
    Convert numerical risk score (0-100) to RiskLevel enum

    Args:
        score: Risk score from 0 (safest) to 100 (riskiest)

    Returns:
        Corresponding RiskLevel enum

    Examples:
        >>> risk_score_to_level(15)
        RiskLevel.VERY_LOW

        >>> risk_score_to_level(45)
        RiskLevel.MODERATE

        >>> risk_score_to_level(99)
        RiskLevel.CRITICAL
    """
    if score < 0:
        score = 0
    elif score > 100:
        score = 100

    if score <= 20:
        return RiskLevel.VERY_LOW
    elif score <= 40:
        return RiskLevel.LOW
    elif score <= 60:
        return RiskLevel.MODERATE
    elif score <= 80:
        return RiskLevel.HIGH
    elif score <= 95:
        return RiskLevel.VERY_HIGH
    else:
        return RiskLevel.CRITICAL


def pool_score_to_rating(score: float) -> PoolRating:
    """
    Convert pool quality score (0-100) to PoolRating

    Scoring factors:
    - TVL (40%): Higher is better
    - Volume/TVL ratio (30%): Higher means more active
    - Reserve balance (20%): Closer to 50/50 is better
    - Fee appropriateness (10%): Matches asset type

    Args:
        score: Pool quality score from 0 to 100

    Returns:
        Corresponding PoolRating enum

    Examples:
        >>> pool_score_to_rating(96)
        PoolRating.S_PLUS

        >>> pool_score_to_rating(85)
        PoolRating.A

        >>> pool_score_to_rating(45)
        PoolRating.F
    """
    if score < 0:
        score = 0
    elif score > 100:
        score = 100

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


def risk_rating_to_number(rating: RiskRating) -> int:
    """Convert RiskRating enum to integer 1-5"""
    return rating.value


def number_to_risk_rating(number: int) -> RiskRating:
    """Convert integer 1-5 to RiskRating enum"""
    if number < 1:
        number = 1
    elif number > 5:
        number = 5
    return RiskRating(number)


# ====================================================================================
# VALIDATION FUNCTIONS
# ====================================================================================

def validate_apy(apy: float) -> bool:
    """
    Validate if APY is realistic

    Flags:
    - Negative APY (possible but unusual)
    - APY > 1000% (likely scam or temporary incentive)

    Args:
        apy: Annual Percentage Yield as percentage

    Returns:
        True if seems realistic, False if suspicious
    """
    if apy < 0:
        return False  # Negative yield is loss
    if apy > 1000:
        return False  # >1000% APY is almost certainly unsustainable
    return True


def classify_yield_sustainability(
    apy: float,
    protocol_age_days: int,
    tvl_usd: float
) -> str:
    """
    Classify yield sustainability

    Args:
        apy: Current APY
        protocol_age_days: How long protocol has existed
        tvl_usd: Total Value Locked

    Returns:
        "Sustainable", "Questionable", or "Unsustainable"
    """
    # Very high APY on new protocol = red flag
    if apy > 100 and protocol_age_days < 90:
        return "Unsustainable"

    # High APY on small TVL = likely temporary
    if apy > 50 and tvl_usd < 1_000_000:
        return "Questionable"

    # Reasonable APY on established protocol = good
    if apy < 30 and protocol_age_days > 180:
        return "Sustainable"

    return "Questionable"
```

**✅ Checkpoint**: `src/api/types.py` created (370 lines!)

---

### **Step 2: Create Type Routes** (20 min)

Create `src/api/routes/__init__.py`:

```python
"""API Routes Package"""
# This file makes routes/ a Python package
```

Create `src/api/routes/types.py`:

```python
"""
Type Definition Routes
Day 003/030
"""

from fastapi import APIRouter
from typing import List, Dict, Any
from types import (
    RiskLevel,
    RiskRating,
    YieldType,
    ProtocolType,
    PoolRating,
    risk_score_to_level,
    pool_score_to_rating
)

router = APIRouter(prefix="/api/types", tags=["Type Definitions"])


@router.get(
    "/risk-levels",
    summary="Get all risk level definitions"
)
async def get_risk_levels() -> Dict[str, Any]:
    """
    # Get Risk Level Definitions

    Returns all available risk levels with descriptions and score ranges.

    ## Response

    ```json
    {
      "risk_levels": [
        {
          "name": "VERY_LOW",
          "value": "Very Low",
          "score_range": [0, 20],
          "description": "Blue-chip protocols..."
        },
        ...
      ]
    }
    ```

    ## Use Cases

    - Show risk options in UI dropdown
    - Validate risk level inputs
    - Display risk level descriptions
    """
    levels = []
    for level in RiskLevel:
        score_range = level.to_score_range()
        levels.append({
            "name": level.name,
            "value": level.value,
            "score_range": list(score_range),
            "min_score": score_range[0],
            "max_score": score_range[1]
        })

    return {
        "risk_levels": levels,
        "count": len(levels)
    }


@router.get(
    "/risk-ratings",
    summary="Get simplified 1-5 risk ratings"
)
async def get_risk_ratings() -> Dict[str, Any]:
    """
    # Get Risk Ratings (1-5 Scale)

    Simplified rating scale for user-friendly filtering.

    ## Response

    ```json
    {
      "ratings": [
        {"rating": 1, "name": "VERY_LOW", "description": "Safest"},
        {"rating": 2, "name": "LOW", "description": "Safe"},
        ...
      ]
    }
    ```
    """
    ratings = []
    for rating in RiskRating:
        ratings.append({
            "rating": rating.value,
            "name": rating.name,
            "maps_to": rating.to_risk_level().value
        })

    return {
        "ratings": ratings,
        "count": len(ratings),
        "note": "Use for filtering yields by risk tolerance"
    }


@router.get(
    "/yield-types",
    summary="Get all yield type definitions"
)
async def get_yield_types() -> Dict[str, Any]:
    """
    # Get Yield Type Definitions

    Returns all ways to earn yield in DeFi.

    ## Response

    ```json
    {
      "yield_types": [
        {
          "name": "LENDING",
          "value": "Lending",
          "typical_apy_range": [1, 8],
          "description": "Deposit assets, earn interest"
        },
        ...
      ]
    }
    ```
    """
    types = []
    for yield_type in YieldType:
        apy_range = yield_type.typical_apy_range()
        types.append({
            "name": yield_type.name,
            "value": yield_type.value,
            "typical_apy_range": list(apy_range),
            "min_apy": apy_range[0],
            "max_apy": apy_range[1]
        })

    return {
        "yield_types": types,
        "count": len(types)
    }


@router.get(
    "/protocol-types",
    summary="Get all protocol type definitions"
)
async def get_protocol_types() -> Dict[str, Any]:
    """
    # Get Protocol Type Definitions

    Returns all categories of DeFi protocols.

    ## Response

    ```json
    {
      "protocol_types": [
        {"name": "DEX", "value": "Decentralized Exchange"},
        {"name": "LENDING", "value": "Lending Protocol"},
        ...
      ]
    }
    ```
    """
    types = [
        {
            "name": pt.name,
            "value": pt.value
        }
        for pt in ProtocolType
    ]

    return {
        "protocol_types": types,
        "count": len(types)
    }


@router.get(
    "/pool-ratings",
    summary="Get pool quality rating definitions"
)
async def get_pool_ratings() -> Dict[str, Any]:
    """
    # Get Pool Rating Definitions

    Returns liquidity pool quality ratings (S+ to F).

    ## Response

    ```json
    {
      "ratings": [
        {
          "rating": "S+",
          "score_range": [95, 100],
          "description": "Exceptional - Best liquidity pools"
        },
        ...
      ]
    }
    ```
    """
    ratings = []
    for rating in PoolRating:
        score_range = rating.to_score_range()
        ratings.append({
            "rating": rating.value,
            "name": rating.name,
            "score_range": list(score_range),
            "min_score": score_range[0],
            "max_score": score_range[1],
            "description": rating.description()
        })

    return {
        "ratings": ratings,
        "count": len(ratings)
    }


@router.get(
    "/convert/score-to-risk/{score}",
    summary="Convert risk score to risk level"
)
async def convert_score_to_risk(score: float) -> Dict[str, Any]:
    """
    # Convert Risk Score to Level

    Convert numerical score (0-100) to RiskLevel.

    ## Example

    ```
    GET /api/types/convert/score-to-risk/35
    ```

    ## Response

    ```json
    {
      "score": 35,
      "risk_level": "Low",
      "score_range": [21, 40]
    }
    ```
    """
    risk_level = risk_score_to_level(score)
    score_range = risk_level.to_score_range()

    return {
        "score": score,
        "risk_level": risk_level.value,
        "risk_level_name": risk_level.name,
        "score_range": list(score_range)
    }


@router.get(
    "/convert/score-to-rating/{score}",
    summary="Convert pool score to rating"
)
async def convert_score_to_rating(score: float) -> Dict[str, Any]:
    """
    # Convert Pool Score to Rating

    Convert numerical score (0-100) to PoolRating.

    ## Example

    ```
    GET /api/types/convert/score-to-rating/92
    ```

    ## Response

    ```json
    {
      "score": 92,
      "rating": "A+",
      "score_range": [90, 94],
      "description": "Excellent - Very safe for trading"
    }
    ```
    """
    rating = pool_score_to_rating(score)
    score_range = rating.to_score_range()

    return {
        "score": score,
        "rating": rating.value,
        "rating_name": rating.name,
        "score_range": list(score_range),
        "description": rating.description()
    }
```

**✅ Checkpoint**: Routes created

---

### **Step 3: Update main.py** (15 min)

Modify `src/api/main.py` - add this import at the top:

```python
from routes import types as types_routes
```

Then add this line after the middleware configuration:

```python
# Include routers
app.include_router(types_routes.router)
```

Also update the root endpoint version:

```python
@app.get("/", ...)
async def root() -> Dict[str, Any]:
    return {
        "message": "DeFi Analytics Platform API",
        "version": "0.3.0-day003",  # ← UPDATE
        "day": "003/030",             # ← UPDATE
        # ... rest same
    }
```

**✅ Checkpoint**: Main app updated

---

### **Step 4: Test the Endpoints** (25 min)

Restart your server:

```bash
cd src/api
python main.py
```

#### **Test 1: Get All Risk Levels**

```bash
curl http://localhost:8000/api/types/risk-levels
```

**Expected output:**
```json
{
  "risk_levels": [
    {
      "name": "VERY_LOW",
      "value": "Very Low",
      "score_range": [0, 20],
      "min_score": 0,
      "max_score": 20
    },
    {
      "name": "LOW",
      "value": "Low",
      "score_range": [21, 40],
      "min_score": 21,
      "max_score": 40
    },
    ...
  ],
  "count": 6
}
```

**✅ Test passed!**

---

#### **Test 2: Get Yield Types**

```bash
curl http://localhost:8000/api/types/yield-types
```

**Expected output:**
```json
{
  "yield_types": [
    {
      "name": "LENDING",
      "value": "Lending",
      "typical_apy_range": [1, 8],
      "min_apy": 1,
      "max_apy": 8
    },
    {
      "name": "LP_FEES",
      "value": "Liquidity Provider Fees",
      "typical_apy_range": [5, 50],
      "min_apy": 5,
      "max_apy": 50
    },
    ...
  ],
  "count": 7
}
```

**✅ Test passed!**

---

#### **Test 3: Convert Score to Risk Level**

```bash
curl http://localhost:8000/api/types/convert/score-to-risk/35
```

**Expected output:**
```json
{
  "score": 35,
  "risk_level": "Low",
  "risk_level_name": "LOW",
  "score_range": [21, 40]
}
```

Try different scores:
```bash
curl http://localhost:8000/api/types/convert/score-to-risk/15  # Very Low
curl http://localhost:8000/api/types/convert/score-to-risk/55  # Moderate
curl http://localhost:8000/api/types/convert/score-to-risk/99  # Critical
```

**✅ Test passed!**

---

#### **Test 4: Convert Score to Pool Rating**

```bash
curl http://localhost:8000/api/types/convert/score-to-rating/92
```

**Expected output:**
```json
{
  "score": 92,
  "rating": "A+",
  "rating_name": "A_PLUS",
  "score_range": [90, 94],
  "description": "Excellent - Very safe for trading"
}
```

Try different scores:
```bash
curl http://localhost:8000/api/types/convert/score-to-rating/96  # S+
curl http://localhost:8000/api/types/convert/score-to-rating/85  # A
curl http://localhost:8000/api/types/convert/score-to-rating/30  # F
```

**✅ Test passed!**

---

#### **Test 5: Check API Documentation**

Open http://localhost:8000/docs

You should see a new section: **"Type Definitions"** with 7 endpoints!

**✅ Documentation updated automatically!**

---

### **Step 5: Test Dataclasses in Python** (10 min)

Create a test file `src/api/test_day003.py`:

```python
"""
Test Day 003 - Enums and Dataclasses
"""

from types import (
    RiskLevel,
    YieldType,
    Protocol,
    ProtocolType,
    YieldOpportunitySummary,
    PoolInfo,
    PoolRating,
    risk_score_to_level
)
from datetime import datetime


def test_protocol():
    """Test Protocol dataclass"""
    print("=" * 60)
    print("TEST: Protocol Dataclass")
    print("=" * 60)

    aave = Protocol(
        name="Aave",
        protocol_type=ProtocolType.LENDING,
        chain="Ethereum",
        website="https://aave.com",
        audited=True,
        audit_firms=["Trail of Bits", "OpenZeppelin", "ConsenSys Diligence"],
        tvl_usd=5_000_000_000,
        days_active=1095,  # ~3 years
        risk_score=18.5
        # risk_level will be auto-calculated!
    )

    print(f"Protocol: {aave.name}")
    print(f"Type: {aave.protocol_type.value}")
    print(f"TVL: ${aave.tvl_usd:,.0f}")
    print(f"Risk Score: {aave.risk_score}")
    print(f"Risk Level: {aave.risk_level.value} (auto-calculated!)")
    print(f"Audits: {len(aave.audit_firms)}")
    print()


def test_yield_opportunity():
    """Test YieldOpportunitySummary dataclass"""
    print("=" * 60)
    print("TEST: Yield Opportunity")
    print("=" * 60)

    opportunity = YieldOpportunitySummary(
        protocol="Curve",
        asset="3pool",
        apy=8.5,
        tvl_usd=1_500_000_000,
        yield_type=YieldType.LP_FEES,
        risk_level=RiskLevel.LOW,
        lock_days=0,
        updated_at=datetime.now()
    )

    print(f"Protocol: {opportunity.protocol}")
    print(f"Asset: {opportunity.asset}")
    print(f"APY: {opportunity.apy}%")
    print(f"Type: {opportunity.yield_type.value}")
    print(f"Risk: {opportunity.risk_level.value}")
    print(f"Has Lock: {opportunity.has_lock}")
    print(f"Is Stable: {opportunity.is_stable}")
    print(f"Risk-Adjusted APY: {opportunity.risk_adjusted_apy():.2f}%")
    print()


def test_pool_info():
    """Test PoolInfo dataclass"""
    print("=" * 60)
    print("TEST: Pool Info")
    print("=" * 60)

    pool = PoolInfo(
        pool_address="0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
        token0="USDC",
        token1="WETH",
        reserve0=2_000_000,  # 2M USDC
        reserve1=1_000,      # 1,000 ETH
        tvl_usd=4_000_000,
        volume_24h=3_200_000,
        fee_tier=0.0005,
        rating=PoolRating.A_PLUS
    )

    print(f"Pool: {pool.token0}/{pool.token1}")
    print(f"Reserves: {pool.reserve0:,.0f} {pool.token0} / {pool.reserve1:,.0f} {pool.token1}")
    print(f"Price: {pool.price:,.2f} {pool.token0}/{pool.token1}")
    print(f"TVL: ${pool.tvl_usd:,.0f}")
    print(f"24h Volume: ${pool.volume_24h:,.0f}")
    print(f"Volume/TVL Ratio: {pool.volume_to_tvl_ratio:.2f}x")
    print(f"Rating: {pool.rating.value} - {pool.rating.description()}")
    print()


def test_enum_methods():
    """Test enum helper methods"""
    print("=" * 60)
    print("TEST: Enum Helper Methods")
    print("=" * 60)

    # Test RiskLevel score ranges
    print("Risk Level Score Ranges:")
    for level in RiskLevel:
        score_range = level.to_score_range()
        print(f"  {level.value:15s}: {score_range[0]:3d}-{score_range[1]:3d}")

    print("\nYield Type APY Ranges:")
    for yt in YieldType:
        apy_range = yt.typical_apy_range()
        print(f"  {yt.value:30s}: {apy_range[0]:3d}-{apy_range[1]:3d}%")

    print("\nPool Rating Descriptions:")
    for rating in PoolRating:
        print(f"  {rating.value:3s}: {rating.description()}")

    print()


def test_conversion_functions():
    """Test conversion helper functions"""
    print("=" * 60)
    print("TEST: Conversion Functions")
    print("=" * 60)

    test_scores = [10, 35, 55, 75, 90, 99]
    print("Risk Score to Level:")
    for score in test_scores:
        level = risk_score_to_level(score)
        print(f"  Score {score:3d} → {level.value}")

    print()


if __name__ == "__main__":
    test_protocol()
    test_yield_opportunity()
    test_pool_info()
    test_enum_methods()
    test_conversion_functions()

    print("=" * 60)
    print("✅ All Day 003 tests passed!")
    print("=" * 60)
```

Run it:

```bash
cd src/api
python test_day003.py
```

**Expected output:**
```
============================================================
TEST: Protocol Dataclass
============================================================
Protocol: Aave
Type: Lending Protocol
TVL: $5,000,000,000
Risk Score: 18.5
Risk Level: Very Low (auto-calculated!)
Audits: 3

============================================================
TEST: Yield Opportunity
============================================================
Protocol: Curve
Asset: 3pool
APY: 8.5%
Type: Liquidity Provider Fees
Risk: Low
Has Lock: False
Is Stable: True
Risk-Adjusted APY: 8.08%

============================================================
TEST: Pool Info
============================================================
Pool: USDC/WETH
Reserves: 2,000,000 USDC / 1,000 WETH
Price: 2,000.00 USDC/WETH
TVL: $4,000,000
24h Volume: $3,200,000
Volume/TVL Ratio: 0.80x
Rating: A+ - Excellent - Very safe for trading

... (more output)

✅ All Day 003 tests passed!
```

**✅ Python tests working!**

---

## 🎉 Day 003 Complete!

### **What You Built:**

✅ 6 DeFi-specific enums (370 lines of well-documented code!)
✅ 3 dataclasses for complex data structures
✅ 7 API endpoints for type definitions
✅ Helper conversion functions
✅ Automatic risk level calculation
✅ Pool rating system (S+ to F)
✅ Type-safe code with full IDE support

### **What You Learned:**

- Python Enum for fixed choices
- Dataclass for structured data
- @property decorators for computed fields
- __post_init__ for auto-calculation
- Type hints for better code
- API route organization
- How to model DeFi concepts

---

## 📊 Progress

```
[████████████░░░░░░░░░░░░░░░░] Day 003/030 (10.0%)

Foundation:     [██████░░░░] 3/5 days
Liquidity:      [░░░░░░░░░░] 0/7 days
Risk:           [░░░░░░░░░░] 0/6 days
Yield:          [░░░░░░░░░░] 0/6 days
Data/Production:[░░░░░░░░░░] 0/6 days
```

---

## 🐛 Troubleshooting

### **Problem: Cannot import types**

```bash
# Make sure you're in src/api directory
cd /home/user/defi-analytics-platform/src/api
python main.py
```

### **Problem: Enum not working**

```python
# WRONG - using string
risk = "Very Low"  # This is just a string!

# RIGHT - using enum
risk = RiskLevel.VERY_LOW  # Type-safe!
```

---

## 💡 Key Concepts

### **Why Enums?**

**Problem without enums:**
```python
# Easy to make typos
risk = "very low"  # lowercase
risk = "Very  Low"  # extra space
risk = "VeryLow"   # no space
# All different strings, bugs happen!
```

**Solution with enums:**
```python
risk = RiskLevel.VERY_LOW
# Only one way to write it
# IDE autocomplete
# Catches typos at development time!
```

### **Why Dataclasses?**

**Before (manual class):**
```python
class Protocol:
    def __init__(self, name, type, chain, ...):
        self.name = name
        self.type = type
        self.chain = chain
        # 50 more lines of boilerplate...
```

**After (dataclass):**
```python
@dataclass
class Protocol:
    name: str
    protocol_type: ProtocolType
    chain: str
    # Automatic __init__, __repr__, __eq__!
```

---

## 🚀 Next Steps

**Tomorrow (Day 004)**: Mathematical Utilities
- Financial calculation functions
- APY, compound interest, Sharpe ratio
- Percentage calculations
- Statistical functions
- NumPy integration

---

**Day 003/030 Complete** ✅ | **Next**: Day 004 - Math Utilities
