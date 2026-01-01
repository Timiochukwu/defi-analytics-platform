# DeFi Analytics Platform - Complete Tutorial Guide

> **30-Day Journey from Zero to DeFi Analytics Expert**
>
> Build a production-ready DeFi analytics platform with yield optimization, risk assessment, and portfolio management.

---

## 📊 Executive Summary

### Project Overview
**DeFi Analytics & Risk Management Platform** - A comprehensive backend system for analyzing and managing DeFi portfolios, optimizing yields across 15+ protocols, and assessing smart contract and liquidation risks.

### Technology Stack
- **Backend**: FastAPI (Python 3.9+)
- **Data Science**: Pandas, NumPy, SciPy
- **Blockchain**: Web3.py, eth-abi
- **ML/Analytics**: scikit-learn, TensorFlow, XGBoost
- **Database**: PostgreSQL, Redis (caching)
- **API**: REST with Pydantic validation

### Complexity Rating
- **Skill Level Required**: Intermediate to Advanced
- **Prerequisites**:
  - Python programming (intermediate)
  - REST API concepts
  - Basic DeFi knowledge (AMMs, lending, staking)
  - Financial mathematics basics
  - Database fundamentals

### Code Statistics
```
Total Backend Lines: ~6,125 lines of Python

Module Breakdown:
├── risk/defi_risk_models.py        1,192 lines (23.3%)
├── optimization/defi_portfolio.py  1,041 lines (20.3%)
├── optimization/yield_optimizer.py 1,036 lines (20.2%)
├── analytics/liquidity_analyzer.py   926 lines (18.1%)
├── api/main.py                       654 lines (12.8%)
└── data/defi_data_collector.py       535 lines ( 10.4%)
```

### What This Platform Does

#### 1. **Portfolio Management**
- Build Conservative, Balanced, and Aggressive portfolios
- Monitor portfolio health and performance
- Automated rebalancing recommendations

#### 2. **Yield Optimization**
- Discover yield opportunities across 15+ DeFi protocols
- Calculate risk-adjusted returns (Sharpe ratio)
- Optimize allocations using mean-variance optimization

#### 3. **Risk Assessment**
- **Smart Contract Risk**: Audit quality, code complexity, time deployed
- **Liquidation Risk**: Health factor calculation, cascade modeling
- **Systemic Risk**: Protocol interconnection analysis

#### 4. **Liquidity Analysis**
- Slippage calculation for AMMs (Uniswap V2/V3, Curve)
- Pool quality scoring (TVL, volume, balance)
- Impermanent loss calculation for LPs

#### 5. **Data Collection**
- Real-time data from Ethereum mainnet
- Web3 integration with Uniswap, Aave, Compound, Curve
- The Graph Protocol for historical data

---

## 📅 Tutorial Timeline

### Total Duration: 30 Days
- **Days 1-5**: Foundation & Setup (Environment, FastAPI basics)
- **Days 6-12**: Core Analytics (Liquidity, slippage, pool scoring)
- **Days 13-18**: Risk Models (Smart contract, liquidation, systemic)
- **Days 19-24**: Yield Optimization (Discovery, portfolio optimization)
- **Days 25-28**: Integration & Testing (Full API, curl testing)
- **Days 29-30**: Production Polish (Error handling, documentation)

### Daily Time Commitment
- **1-2 hours per day**
- **Flexible pacing** - adjust based on complexity
- **Hands-on coding** - no passive learning

---

## 🎯 Learning Outcomes

By Day 30, you will have built:
- ✅ A production-ready FastAPI backend with 10+ endpoints
- ✅ Risk assessment algorithms for DeFi protocols
- ✅ Portfolio optimization using modern portfolio theory
- ✅ Liquidity analysis with slippage calculation
- ✅ Web3 integration for real-time blockchain data
- ✅ Complete API documentation with Swagger/ReDoc

---

## 📚 Complete Day-by-Day Breakdown

### **PHASE 1: FOUNDATION (Days 1-5)**

---

#### **Day 001: Environment Setup & Project Structure**

**Topic**: Python Environment, FastAPI Hello World

**Time**: 1-2 hours

**What You'll Build**:
- Virtual environment with all dependencies
- Basic FastAPI server with `/health` endpoint
- Project folder structure

**Dependencies to Install** (Day 1 ONLY):
```bash
# Core API
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.4.0
python-multipart>=0.0.6

# Utilities
python-dotenv>=1.0.0
```

**Files to Create**:
```
project/
├── src/
│   ├── __init__.py
│   └── api/
│       ├── __init__.py
│       └── main.py          ← CREATE THIS
├── requirements.txt          ← CREATE THIS
└── .env                      ← CREATE THIS
```

**Key Concepts**:
- Virtual environments (venv)
- FastAPI app initialization
- Uvicorn ASGI server
- CORS middleware
- Pydantic models

**Deliverable**:
- `/health` endpoint returns `{"status": "healthy"}`
- Server runs on `http://localhost:8000`
- API docs accessible at `/docs`

**Test with curl**:
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","timestamp":"..."}
```

---

#### **Day 002: FastAPI Request/Response Models**

**Topic**: Pydantic schemas, POST endpoints, validation

**Time**: 1-2 hours

**What You'll Build**:
- Pydantic request/response models
- POST endpoint with validation
- Error handling basics

**Dependencies** (NONE - use Day 1 dependencies)

**Files to Modify**:
- `src/api/main.py` - Add Pydantic models and POST endpoint

**Key Concepts**:
- Pydantic BaseModel
- Field validation
- Request body parsing
- HTTP status codes (200, 400, 500)
- Exception handling

**Deliverable**:
```python
# POST /api/calculate
# Input: {"value": 100, "percentage": 10}
# Output: {"result": 110}
```

**Test with curl**:
```bash
curl -X POST http://localhost:8000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"value": 100, "percentage": 10}'
```

---

#### **Day 003: Data Structures & Enums**

**Topic**: Enums, dataclasses, type hints

**Time**: 1-2 hours

**What You'll Build**:
- Risk level enums
- Yield type enums
- Dataclasses for responses

**Dependencies** (NONE)

**Files to Create**:
- `src/models/__init__.py`
- `src/models/types.py` - Enums and dataclasses

**Key Concepts**:
- Python Enum
- @dataclass decorator
- Type hints (List, Dict, Optional)
- JSON serialization

**Deliverable**:
```python
class RiskLevel(Enum):
    VERY_LOW = "Very Low"
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    CRITICAL = "Critical"

@dataclass
class RiskAssessment:
    risk_score: float
    risk_level: RiskLevel
    recommendation: str
```

---

#### **Day 004: Basic Math Functions**

**Topic**: Financial calculations, formulas

**Time**: 1-2 hours

**What You'll Build**:
- APY calculation
- Percentage change
- Simple ratio calculations

**Dependencies to Install**:
```bash
numpy>=1.24.0
```

**Files to Create**:
- `src/utils/__init__.py`
- `src/utils/calculations.py`

**Key Concepts**:
- Compound interest formula: `APY = (1 + r/n)^(n*t) - 1`
- Percentage change: `((new - old) / old) * 100`
- NumPy arrays for vectorized operations

**Deliverable**:
```python
def calculate_apy(deposit: float, earned: float, days: int) -> float:
    """Calculate Annual Percentage Yield"""
    # Implementation

def calculate_percentage_change(old: float, new: float) -> float:
    """Calculate percentage change"""
    # Implementation
```

**Test with curl**:
```bash
curl -X POST http://localhost:8000/api/calculate-apy \
  -H "Content-Type: application/json" \
  -d '{"deposit": 10000, "earned": 500, "days": 365}'
```

---

#### **Day 005: API Structure & Routing**

**Topic**: API versioning, route organization

**Time**: 1-2 hours

**What You'll Build**:
- Organized route structure
- API versioning (`/api/v1/...`)
- Route tags for documentation

**Dependencies** (NONE)

**Files to Create**:
- `src/api/routes/__init__.py`
- `src/api/routes/liquidity.py`
- `src/api/routes/risk.py`
- `src/api/routes/yield_routes.py`

**Key Concepts**:
- FastAPI APIRouter
- Route prefixes and tags
- Modular API design
- OpenAPI documentation groups

**Deliverable**:
```
API Structure:
├── /api/liquidity/*    (Liquidity routes)
├── /api/risk/*         (Risk routes)
├── /api/yield/*        (Yield routes)
└── /api/portfolio/*    (Portfolio routes)
```

**Test with curl**:
```bash
curl http://localhost:8000/docs
# View organized API documentation
```

---

### **PHASE 2: LIQUIDITY ANALYSIS (Days 6-12)**

---

#### **Day 006: Constant Product AMM - Theory**

**Topic**: Uniswap V2 math, constant product formula

**Time**: 1-2 hours

**What You'll Build**:
- Understanding of `x * y = k` formula
- Basic swap calculation
- Price calculation from reserves

**Dependencies to Install**:
```bash
pandas>=2.0.0
scipy>=1.11.0
```

**Files to Create**:
- `src/analytics/__init__.py`
- `src/analytics/liquidity_analyzer.py` (start)

**Key Concepts**:
- **Constant Product Formula**: `reserve_X * reserve_Y = k`
- **Swap Formula**: `Δy = (y * Δx) / (x + Δx)`
- **Price**: `P = reserve_Y / reserve_X`

**Deliverable**:
```python
def calculate_swap_output(
    reserve_in: float,
    reserve_out: float,
    amount_in: float
) -> float:
    """Calculate output amount for AMM swap"""
    # x * y = k implementation
```

---

#### **Day 007: Slippage Calculation**

**Topic**: Slippage in AMMs, price impact

**Time**: 1-2 hours

**What You'll Build**:
- Slippage calculator
- Price impact assessment
- Trade size recommendations

**Dependencies** (NONE - use Day 6)

**Files to Modify**:
- `src/analytics/liquidity_analyzer.py` - Add slippage calculation

**Key Concepts**:
- **Slippage**: Difference between expected and execution price
- **Formula**: `Slippage = (ExecutionPrice - ExpectedPrice) / ExpectedPrice`
- **Fee impact**: `amountIn * (1 - fee)`

**Deliverable**:
```python
def calculate_slippage_constant_product(
    reserve_in: float,
    reserve_out: float,
    amount_in: float,
    fee: float = 0.003
) -> SlippageResult:
    """
    Calculate slippage for constant product AMM

    Example:
        Pool: 1,000 ETH / 2,000,000 USDC
        Trade: 10,000 USDC → ETH
        Fee: 0.3%
        Expected Slippage: ~0.5%
    """
```

**Test with curl**:
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

---

#### **Day 008: Pool Quality Scoring**

**Topic**: Liquidity pool metrics, TVL, volume

**Time**: 1-2 hours

**What You'll Build**:
- Pool quality scorer (0-100)
- TVL analysis
- Volume-to-TVL ratio

**Dependencies** (NONE)

**Files to Modify**:
- `src/analytics/liquidity_analyzer.py` - Add pool scoring

**Key Concepts**:
- **TVL** (Total Value Locked): Total assets in pool
- **Volume/TVL Ratio**: Activity indicator (>0.5 = very active)
- **Reserve Balance**: How close to 50/50 split
- **Score Formula**: Weighted average of all factors

**Deliverable**:
```python
def calculate_pool_quality_score(
    tvl: float,
    volume_24h: float,
    fee_tier: float,
    reserve_ratio: float
) -> Dict[str, Any]:
    """
    Score pool quality 0-100

    Factors:
    - TVL (40%): Higher is better
    - Volume/TVL (30%): Higher means more fees
    - Balance (20%): Closer to 50/50 better
    - Fee tier (10%): Appropriate for pair type

    Returns:
        {
            'overall_score': 93.5,
            'rating': 'A+',
            'tvl_score': 95.0,
            'volume_score': 100.0,
            ...
        }
    """
```

**Test with curl**:
```bash
curl -X POST http://localhost:8000/api/liquidity/pool-quality \
  -H "Content-Type: application/json" \
  -d '{
    "tvl": 100000000,
    "volume_24h": 80000000,
    "fee_tier": 0.0005,
    "reserve_ratio": 0.98
  }'
```

---

#### **Day 009: Impermanent Loss Calculator**

**Topic**: IL calculation, LP risks

**Time**: 1-2 hours

**What You'll Build**:
- IL calculator for 2-asset pools
- Price change impact analysis
- Break-even fee calculation

**Dependencies** (NONE)

**Files to Modify**:
- `src/analytics/liquidity_analyzer.py` - Add IL functions

**Key Concepts**:
- **Impermanent Loss Formula**:
  ```
  IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1
  ```
- **Example**: ETH $1000→$2000 (2x) = -5.7% IL
- **Break-even**: Fees earned must exceed IL

**Deliverable**:
```python
def calculate_impermanent_loss(
    price_start: float,
    price_end: float
) -> Dict[str, float]:
    """
    Calculate IL for liquidity providers

    Example:
        price_start = 1000  # $1000/ETH
        price_end = 2000    # $2000/ETH
        Result: -5.7% IL

        Meaning: LP lost 5.7% vs holding assets
    """
```

---

#### **Day 010: Concentrated Liquidity (Uniswap V3)**

**Topic**: Range orders, capital efficiency

**Time**: 1-2 hours

**What You'll Build**:
- Concentrated liquidity calculator
- Capital efficiency comparison
- Out-of-range detection

**Dependencies** (NONE)

**Files to Modify**:
- `src/analytics/liquidity_analyzer.py` - Add V3 functions

**Key Concepts**:
- **V3 Innovation**: Provide liquidity in price ranges
- **Capital Efficiency**: 2-4000x vs V2
- **Risks**: More IL, more out-of-range risk

**Deliverable**:
```python
def calculate_concentrated_liquidity_position(
    current_price: float,
    lower_price: float,
    upper_price: float,
    liquidity_amount: float
) -> ConcentratedLPPosition:
    """
    Calculate V3 concentrated position

    Example:
        ETH at $2000
        Range: $1900-$2100
        Capital efficiency: 10x vs full-range
    """
```

---

#### **Day 011: StableSwap (Curve) Math**

**Topic**: Stablecoin AMM, low slippage

**Time**: 1-2 hours

**What You'll Build**:
- Curve stableswap calculator
- Slippage comparison vs constant product
- Amplification coefficient analysis

**Dependencies** (NONE)

**Files to Modify**:
- `src/analytics/liquidity_analyzer.py` - Add Curve functions

**Key Concepts**:
- **StableSwap Formula**: Hybrid of constant product + constant sum
- **Amplification (A)**: Higher A = lower slippage for stables
- **Use case**: USDC/USDT/DAI swaps with ~0.01% slippage

**Deliverable**:
```python
def calculate_stableswap_output(
    reserves: List[float],
    amount_in: float,
    token_in_index: int,
    token_out_index: int,
    amplification: float = 100
) -> float:
    """
    Curve StableSwap calculation

    Much lower slippage than Uniswap for stables
    """
```

---

#### **Day 012: Complete Liquidity API Endpoints**

**Topic**: Integration, testing, documentation

**Time**: 1-2 hours

**What You'll Build**:
- Complete liquidity endpoints
- Comprehensive error handling
- API documentation with examples

**Dependencies** (NONE)

**Files to Modify**:
- `src/api/routes/liquidity.py` - Add all endpoints

**Deliverable**:
```
Liquidity Endpoints:
├── POST /api/liquidity/slippage
├── POST /api/liquidity/pool-quality
├── POST /api/liquidity/impermanent-loss
├── POST /api/liquidity/v3-position
└── POST /api/liquidity/stableswap
```

**Full Test Suite** (curl):
```bash
# Test all 5 endpoints
./test-liquidity-api.sh
```

---

### **PHASE 3: RISK ASSESSMENT (Days 13-18)**

---

#### **Day 013: Smart Contract Risk - Data Model**

**Topic**: Risk factors, scoring methodology

**Time**: 1-2 hours

**What You'll Build**:
- SmartContractRisk dataclass
- Risk factor enumeration
- Scoring framework

**Dependencies** (NONE - use existing)

**Files to Create**:
- `src/risk/__init__.py`
- `src/risk/defi_risk_models.py` (start)

**Key Concepts**:
- **Audit Quality**: Number and reputation of auditors
- **Code Complexity**: Lines of code, contract interdependencies
- **Time Deployed**: Battle-tested = safer (Lindy effect)
- **TVL at Risk**: Larger honeypot = more attack incentive
- **Admin Keys**: Centralization risk

**Deliverable**:
```python
@dataclass
class SmartContractRisk:
    protocol_name: str
    audit_score: float          # 0-100
    code_complexity: float      # 0-100
    time_deployed_days: int
    total_value_at_risk: float
    number_of_audits: int
    overall_risk_score: float   # 0-100 (higher = riskier)
    risk_level: RiskLevel
```

---

#### **Day 014: Smart Contract Risk - Scoring Algorithm**

**Topic**: Multi-factor risk scoring

**Time**: 1-2 hours

**What You'll Build**:
- Weighted risk score calculator
- Risk level classification
- Recommendations engine

**Dependencies** (NONE)

**Files to Modify**:
- `src/risk/defi_risk_models.py` - Add SmartContractRiskAnalyzer

**Key Concepts**:
- **Weighted Scoring**:
  - Audits (30%)
  - Code complexity (20%)
  - Time deployed (20%)
  - TVL (15%)
  - Admin control (15%)

**Deliverable**:
```python
class SmartContractRiskAnalyzer:
    def assess_smart_contract_risk(
        self,
        protocol_name: str,
        auditors: List[str],
        code_lines: int,
        days_deployed: int,
        tvl_usd: float,
        has_bug_bounty: bool,
        admin_control_level: str
    ) -> SmartContractRisk:
        """
        Example:
            Aave:
            - 3 top audits
            - 900 days deployed
            - $5B TVL
            - Bug bounty
            → Risk: 18/100 (Very Low)
        """
```

**Test with curl**:
```bash
curl -X POST http://localhost:8000/api/risk/smart-contract \
  -H "Content-Type: application/json" \
  -d '{
    "protocol_name": "Aave",
    "auditors": ["Trail of Bits", "OpenZeppelin", "ConsenSys"],
    "code_lines": 15000,
    "days_deployed": 900,
    "tvl_usd": 5000000000,
    "has_bug_bounty": true,
    "admin_control_level": "Low"
  }'
```

---

#### **Day 015: Liquidation Risk - Health Factor**

**Topic**: Lending protocol liquidation mechanics

**Time**: 1-2 hours

**What You'll Build**:
- Health factor calculator
- Liquidation threshold analysis
- Price shock simulator

**Dependencies** (NONE)

**Files to Modify**:
- `src/risk/defi_risk_models.py` - Add LiquidationRiskAnalyzer

**Key Concepts**:
- **Health Factor**: `HF = (Collateral * LiqThreshold) / Debt`
- **Safe**: HF > 1.5
- **Moderate**: HF 1.2-1.5
- **High Risk**: HF 1.0-1.2
- **Liquidatable**: HF < 1.0

**Deliverable**:
```python
class LiquidationRiskAnalyzer:
    def assess_liquidation_risk(
        self,
        protocol_name: str,
        collateral_value_usd: float,
        debt_value_usd: float,
        liquidation_threshold: float = 0.86
    ) -> LiquidationRisk:
        """
        Example:
            Collateral: $100k ETH
            Debt: $60k USDC
            Threshold: 86%

            HF = (100k * 0.86) / 60k = 1.43
            Risk: Moderate
        """
```

**Test with curl**:
```bash
curl -X POST http://localhost:8000/api/risk/liquidation \
  -H "Content-Type: application/json" \
  -d '{
    "protocol_name": "Aave",
    "asset": "ETH",
    "collateral_value_usd": 100000,
    "debt_value_usd": 60000
  }'
```

---

#### **Day 016: Liquidation Cascade Modeling**

**Topic**: Systemic liquidation risk

**Time**: 1-2 hours

**What You'll Build**:
- Cascade probability calculator
- Multi-position simulation
- Amplification factor

**Dependencies** (NONE)

**Files to Modify**:
- `src/risk/defi_risk_models.py` - Add cascade functions

**Key Concepts**:
- **Cascade**: One liquidation triggers others
- **Amplification**: How much a price drop amplifies
- **Example**: ETH drops 20% → $100M liquidated → price drops more → more liquidations

**Deliverable**:
```python
def calculate_cascade_probability(
    positions: List[Position],
    price_shock: float  # e.g., 0.20 = 20% drop
) -> CascadeRisk:
    """
    Simulate liquidation cascade

    Returns:
        - Cascade probability
        - Total value at risk
        - Amplification factor
    """
```

---

#### **Day 017: Systemic Risk Analysis**

**Topic**: Protocol interconnection, contagion

**Time**: 1-2 hours

**What You'll Build**:
- Protocol dependency graph
- Contagion risk scorer
- Systemic importance rating

**Dependencies to Install**:
```bash
networkx>=3.2.0  # For graph analysis
matplotlib>=3.8.0
```

**Files to Modify**:
- `src/risk/defi_risk_models.py` - Add SystemicRiskAnalyzer

**Key Concepts**:
- **Interconnection**: Protocol A depends on Protocol B
- **Contagion**: Failure spreads through dependencies
- **Example**: Terra/Luna collapse affected entire DeFi ecosystem

**Deliverable**:
```python
class SystemicRiskAnalyzer:
    def assess_protocol_systemic_risk(
        self,
        protocol_dependencies: List[str],
        shared_collateral_ratio: float,
        market_correlation: float
    ) -> SystemicRisk:
        """
        Example:
            Protocol depends on: [Chainlink, Uniswap, USDC]
            Shared collateral: 40%
            → High systemic risk
        """
```

---

#### **Day 018: Complete Risk API Endpoints**

**Topic**: Integration, testing, documentation

**Time**: 1-2 hours

**What You'll Build**:
- Complete risk endpoints
- Comprehensive error handling
- Risk report generator

**Dependencies** (NONE)

**Files to Modify**:
- `src/api/routes/risk.py` - Add all endpoints

**Deliverable**:
```
Risk Endpoints:
├── POST /api/risk/smart-contract
├── POST /api/risk/liquidation
├── POST /api/risk/cascade
└── POST /api/risk/systemic
```

**Full Test Suite** (curl):
```bash
# Test smart contract risk
curl -X POST http://localhost:8000/api/risk/smart-contract -d '{...}'

# Test liquidation risk
curl -X POST http://localhost:8000/api/risk/liquidation -d '{...}'

# Test cascade probability
curl -X POST http://localhost:8000/api/risk/cascade -d '{...}'

# Test systemic risk
curl -X POST http://localhost:8000/api/risk/systemic -d '{...}'
```

---

### **PHASE 4: YIELD OPTIMIZATION (Days 19-24)**

---

#### **Day 019: Yield Discovery - Data Model**

**Topic**: Yield opportunities, APY breakdown

**Time**: 1-2 hours

**What You'll Build**:
- YieldOpportunity dataclass
- Yield type categorization
- APY component breakdown

**Dependencies** (NONE)

**Files to Create**:
- `src/optimization/__init__.py`
- `src/optimization/yield_optimizer.py` (start)

**Key Concepts**:
- **APY Components**:
  - Base APY (protocol fees)
  - Reward APY (token incentives)
  - Total APY
- **Yield Types**: Lending, LP, Staking, Farming, Vault

**Deliverable**:
```python
@dataclass
class YieldOpportunity:
    protocol_name: str
    asset: str
    apy: float              # Total APY
    apy_breakdown: Dict[str, float]  # {'base': 0.02, 'rewards': 0.015}
    tvl_usd: float
    yield_type: YieldType
    risk_rating: RiskRating
    lock_period_days: int
```

---

#### **Day 020: Yield Ranking & Filtering**

**Topic**: Multi-criteria sorting

**Time**: 1-2 hours

**What You'll Build**:
- Opportunity ranker
- Multi-filter system
- Risk-adjusted return calculator

**Dependencies to Install**:
```bash
scikit-learn>=1.3.0  # For normalization
```

**Files to Modify**:
- `src/optimization/yield_optimizer.py` - Add YieldOpportunityAnalyzer

**Key Concepts**:
- **Sharpe Ratio**: `(Return - RiskFreeRate) / StdDev`
- **Risk-Adjusted Return**: Higher return per unit of risk
- **Filters**: APY, risk level, TVL, lock period

**Deliverable**:
```python
class YieldOpportunityAnalyzer:
    def rank_opportunities(
        self,
        opportunities: List[YieldOpportunity],
        risk_tolerance: RiskRating,
        min_liquidity: float,
        prefer_no_lock: bool = True
    ) -> pd.DataFrame:
        """
        Rank opportunities by risk-adjusted returns

        Example output:
            1. Curve 3pool: 8% APY, Low Risk, No Lock
            2. Aave USDC: 3.5% APY, Very Low Risk, No Lock
            3. Uniswap V3 ETH/USDC: 25% APY, Moderate Risk, No Lock
        """
```

---

#### **Day 021: Portfolio Optimization - Mean-Variance**

**Topic**: Modern portfolio theory for DeFi

**Time**: 1-2 hours

**What You'll Build**:
- Mean-variance optimizer
- Efficient frontier calculator
- Maximum Sharpe ratio portfolio

**Dependencies** (NONE - use Day 20)

**Files to Modify**:
- `src/optimization/yield_optimizer.py` - Add PortfolioOptimizer

**Key Concepts**:
- **Modern Portfolio Theory** (Markowitz)
- **Efficient Frontier**: Max return for given risk
- **Sharpe Maximization**: Best risk-adjusted portfolio

**Deliverable**:
```python
class PortfolioOptimizer:
    def optimize_max_sharpe(
        self,
        opportunities: List[YieldOpportunity],
        risk_tolerance: float,
        max_concentration: float = 0.40
    ) -> OptimalAllocation:
        """
        Find optimal allocation

        Example:
            Input: 10 opportunities
            Output:
                - 40% Curve 3pool (8% APY)
                - 30% Aave USDC (3.5% APY)
                - 20% Lido ETH (4.2% APY)
                - 10% Yearn USDC (6% APY)
            Expected APY: 6.1%
            Sharpe: 2.3
        """
```

---

#### **Day 022: Portfolio Construction Strategies**

**Topic**: Conservative, Balanced, Aggressive

**Time**: 1-2 hours

**What You'll Build**:
- Pre-built strategy templates
- Risk-appropriate allocations
- Rebalancing thresholds

**Dependencies** (NONE)

**Files to Create**:
- `src/optimization/defi_portfolio.py`

**Key Concepts**:
- **Conservative**: 70%+ stablecoins, 2-8% APY, risk < 25
- **Balanced**: 40-60% stables, 10-20% APY, risk 25-40
- **Aggressive**: <30% stables, 30-50% APY, risk > 40

**Deliverable**:
```python
class PortfolioConstructor:
    def build_conservative_portfolio(
        self,
        capital_usd: float,
        min_yield_percent: float = 2.0
    ) -> Portfolio:
        """
        Conservative portfolio for capital preservation

        Allocation:
            - 40% Aave USDC (3.5% APY)
            - 25% Compound USDC (3.2% APY)
            - 25% Curve 3pool (5% APY)
            - 10% Yearn USDC (6% APY)

        Expected: 4.1% APY, Risk: 18/100
        """

    def build_balanced_portfolio(...) -> Portfolio:
        """Balanced risk-return"""

    def build_aggressive_portfolio(...) -> Portfolio:
        """Maximum yield, higher risk"""
```

**Test with curl**:
```bash
curl -X POST http://localhost:8000/api/portfolio/build \
  -H "Content-Type: application/json" \
  -d '{
    "capital_usd": 100000,
    "strategy": "balanced"
  }'
```

---

#### **Day 023: Portfolio Monitoring**

**Topic**: Performance tracking, alerts

**Time**: 1-2 hours

**What You'll Build**:
- Portfolio performance calculator
- Health monitoring
- Rebalancing triggers

**Dependencies** (NONE)

**Files to Modify**:
- `src/optimization/defi_portfolio.py` - Add PortfolioMonitor

**Key Concepts**:
- **P&L Calculation**: Current value vs initial
- **Drift Detection**: When allocation deviates >10%
- **Performance Metrics**: APY, Sharpe, max drawdown

**Deliverable**:
```python
class PortfolioMonitor:
    def calculate_performance(
        self,
        portfolio: Portfolio,
        current_prices: Dict[str, float]
    ) -> PerformanceReport:
        """
        Track portfolio performance

        Returns:
            - Total value
            - P&L (absolute & %)
            - Current APY
            - Sharpe ratio
            - Max drawdown
            - Health status
        """
```

---

#### **Day 024: Complete Yield & Portfolio API**

**Topic**: Integration, testing, documentation

**Time**: 1-2 hours

**What You'll Build**:
- Complete yield/portfolio endpoints
- Comprehensive testing
- API documentation

**Dependencies** (NONE)

**Files to Modify**:
- `src/api/routes/yield_routes.py`
- `src/api/routes/portfolio.py`

**Deliverable**:
```
Yield & Portfolio Endpoints:
├── GET  /api/yield/opportunities
├── POST /api/yield/optimize
├── POST /api/portfolio/build
├── GET  /api/portfolio/performance
└── POST /api/portfolio/rebalance
```

**Full Test Suite** (curl):
```bash
# Get yield opportunities
curl "http://localhost:8000/api/yield/opportunities?min_apy=5&max_risk=3"

# Build balanced portfolio
curl -X POST http://localhost:8000/api/portfolio/build \
  -H "Content-Type: application/json" \
  -d '{"capital_usd": 100000, "strategy": "balanced"}'

# Check performance
curl "http://localhost:8000/api/portfolio/performance?portfolio_id=abc123"
```

---

### **PHASE 5: DATA INTEGRATION (Days 25-28)**

---

#### **Day 025: Web3 Setup & Blockchain Connection**

**Topic**: Ethereum RPC, Web3.py basics

**Time**: 1-2 hours

**What You'll Build**:
- Web3 connection manager
- Block number fetcher
- Account balance checker

**Dependencies to Install**:
```bash
web3>=6.11.0
eth-abi>=4.2.0
eth-account>=0.10.0
eth-utils>=2.3.0
```

**Files to Modify**:
- `src/data/defi_data_collector.py` (start)

**Key Concepts**:
- **Infura/Alchemy**: Ethereum node providers
- **Web3 Provider**: Connection to blockchain
- **Block Number**: Current Ethereum block

**Deliverable**:
```python
class DeFiDataCollector:
    def __init__(self, provider_url: str):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))

        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect")

    def get_current_block(self) -> int:
        return self.w3.eth.block_number
```

**Setup**:
```bash
# Get free Infura key: https://infura.io/register
# .env file:
WEB3_PROVIDER_URL="https://mainnet.infura.io/v3/YOUR_KEY"
```

---

#### **Day 026: Smart Contract Data Fetching**

**Topic**: Read pool reserves, calculate prices

**Time**: 1-2 hours

**What You'll Build**:
- Contract ABI loading
- Reserve fetching from Uniswap
- Price calculation

**Dependencies** (NONE - use Day 25)

**Files to Modify**:
- `src/data/defi_data_collector.py` - Add Uniswap functions

**Key Concepts**:
- **ABI** (Application Binary Interface): Contract interface
- **getReserves()**: Fetch pool reserves
- **Price from Reserves**: `price = reserve1 / reserve0`

**Deliverable**:
```python
class DeFiDataCollector:
    def get_uniswap_pool_reserves(
        self,
        pool_address: str
    ) -> Tuple[int, int]:
        """
        Fetch reserves from Uniswap V2/V3 pool

        Example:
            ETH/USDC pool:
            reserve0 = 1,000 ETH
            reserve1 = 2,000,000 USDC
            price = 2,000,000 / 1,000 = $2,000/ETH
        """
```

---

#### **Day 027: Multi-Protocol Data Collection**

**Topic**: Aave, Compound, Curve integration

**Time**: 1-2 hours

**What You'll Build**:
- Aave lending rates fetcher
- Compound APY calculator
- Curve pool info

**Dependencies to Install**:
```bash
requests>=2.31.0
aiohttp>=3.9.0  # For async requests
```

**Files to Modify**:
- `src/data/defi_data_collector.py` - Add protocol functions

**Key Concepts**:
- **Aave**: getLendingRateData()
- **Compound**: supplyRatePerBlock()
- **Curve**: get_virtual_price()

**Deliverable**:
```python
class DeFiDataCollector:
    def get_aave_lending_rate(self, asset: str) -> float:
        """Get Aave lending APY for asset"""

    def get_compound_supply_rate(self, asset: str) -> float:
        """Get Compound supply APY"""

    def get_curve_pool_info(self, pool_address: str) -> Dict:
        """Get Curve pool data"""
```

**Test with curl**:
```bash
curl http://localhost:8000/api/data/aave-rates?asset=USDC
curl http://localhost:8000/api/data/compound-rates?asset=ETH
```

---

#### **Day 028: Data Caching & Rate Limiting**

**Topic**: Redis caching, API rate limiting

**Time**: 1-2 hours

**What You'll Build**:
- Redis cache layer
- Rate limiter
- Data freshness checker

**Dependencies to Install**:
```bash
redis>=5.0.0
```

**Files to Modify**:
- `src/data/cache_manager.py` (create)
- `src/data/defi_data_collector.py` - Add caching

**Key Concepts**:
- **Caching**: Store frequently accessed data
- **TTL** (Time To Live): Cache expiration
- **Rate Limiting**: Avoid hitting API limits

**Deliverable**:
```python
class CacheManager:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    def get_cached(self, key: str) -> Optional[Any]:
        """Get from cache"""

    def set_cached(self, key: str, value: Any, ttl: int = 300):
        """Cache with TTL (default 5 min)"""
```

---

### **PHASE 6: PRODUCTION READY (Days 29-30)**

---

#### **Day 029: Error Handling & Validation**

**Topic**: Comprehensive error handling

**Time**: 1-2 hours

**What You'll Build**:
- Custom exception classes
- Input validation
- Error response formatting

**Dependencies** (NONE)

**Files to Create**:
- `src/utils/exceptions.py`
- `src/utils/validators.py`

**Key Concepts**:
- **Custom Exceptions**: InsufficientLiquidityError, InvalidPoolError
- **Pydantic Validators**: Check value ranges
- **HTTP Error Codes**: 400, 404, 500

**Deliverable**:
```python
class InsufficientLiquidityError(Exception):
    """Raised when pool has insufficient liquidity"""

class InvalidPoolAddressError(Exception):
    """Raised when pool address is invalid"""

@app.exception_handler(InsufficientLiquidityError)
async def handle_liquidity_error(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": "Insufficient liquidity", "detail": str(exc)}
    )
```

---

#### **Day 030: Documentation & Final Testing**

**Topic**: API docs, comprehensive testing

**Time**: 1-2 hours

**What You'll Build**:
- Complete API documentation
- Test suite with curl scripts
- Example use cases

**Dependencies** (NONE)

**Files to Create**:
- `docs/API_REFERENCE.md`
- `tests/test_all_endpoints.sh`
- `examples/use_cases.md`

**Deliverable**:
```bash
# Comprehensive test script
./tests/test_all_endpoints.sh

# Tests:
# ✓ Liquidity endpoints (5 tests)
# ✓ Risk endpoints (4 tests)
# ✓ Yield endpoints (2 tests)
# ✓ Portfolio endpoints (3 tests)
# ✓ Data endpoints (3 tests)
#
# Total: 17 endpoints tested
# All passing ✓
```

**API Documentation**:
- OpenAPI/Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Markdown docs: `docs/API_REFERENCE.md`

---

## 🧪 Testing Strategy

### Curl Testing (No Integration Tests)

For each endpoint, test with curl:

```bash
# 1. Basic health check
curl http://localhost:8000/health

# 2. Liquidity analysis
curl -X POST http://localhost:8000/api/liquidity/slippage \
  -H "Content-Type: application/json" \
  -d '{"reserve_in": 2000000, "reserve_out": 1000, "amount_in": 10000, "fee": 0.003}'

# 3. Risk assessment
curl -X POST http://localhost:8000/api/risk/smart-contract \
  -H "Content-Type: application/json" \
  -d '{"protocol_name": "Aave", "auditors": ["Trail of Bits"], "code_lines": 15000, "days_deployed": 900, "tvl_usd": 5000000000, "has_bug_bounty": true, "admin_control_level": "Low"}'

# 4. Yield opportunities
curl "http://localhost:8000/api/yield/opportunities?min_apy=5&max_risk=3&min_tvl=1000000"

# 5. Portfolio construction
curl -X POST http://localhost:8000/api/portfolio/build \
  -H "Content-Type: application/json" \
  -d '{"capital_usd": 100000, "strategy": "balanced"}'
```

### Testing Checklist

- [ ] All endpoints return 200 OK for valid input
- [ ] Invalid input returns 400 Bad Request
- [ ] Missing required fields returns 422 Unprocessable Entity
- [ ] Server errors return 500 Internal Server Error
- [ ] API documentation is accurate and complete
- [ ] Examples in docs match actual responses

---

## 📊 Dependency Installation Timeline

### When to Install What

**Day 1**: Basic API
```bash
fastapi uvicorn pydantic python-multipart python-dotenv
```

**Day 4**: Math & Data
```bash
numpy
```

**Day 6**: Analytics
```bash
pandas scipy
```

**Day 17**: Risk Graphs
```bash
networkx matplotlib
```

**Day 20**: ML & Optimization
```bash
scikit-learn
```

**Day 25**: Blockchain
```bash
web3 eth-abi eth-account eth-utils
```

**Day 27**: HTTP & Async
```bash
requests aiohttp
```

**Day 28**: Caching
```bash
redis
```

### Full requirements.txt (Install at end)
```txt
# Core API
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.4.0
python-multipart>=0.0.6

# Data Science
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.11.0

# Blockchain
web3>=6.11.0
eth-abi>=4.2.0
eth-account>=0.10.0
eth-utils>=2.3.0

# HTTP
requests>=2.31.0
aiohttp>=3.9.0

# ML
scikit-learn>=1.3.0

# Database
redis>=5.0.0

# Visualization
matplotlib>=3.8.0
networkx>=3.2.0

# Utilities
python-dotenv>=1.0.0
```

---

## 🎓 Sample Day 001 - Full Implementation

### Day 001: Environment Setup & FastAPI Hello World

**Goal**: Create a working FastAPI server with health check

**Time**: 1-2 hours

**Step 1: Setup Python Environment** (15 min)

```bash
# Create project folder
mkdir defi-analytics-platform
cd defi-analytics-platform

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

**Step 2: Install Day 1 Dependencies** (5 min)

```bash
# Create requirements.txt
cat > requirements.txt << EOF
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.4.0
python-multipart>=0.0.6
python-dotenv>=1.0.0
EOF

# Install
pip install -r requirements.txt
```

**Step 3: Create Project Structure** (10 min)

```bash
# Create folders
mkdir -p src/api

# Create __init__.py files
touch src/__init__.py
touch src/api/__init__.py

# Create .env file
cat > .env << EOF
# Environment variables
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
EOF

# Create .gitignore
cat > .gitignore << EOF
venv/
__pycache__/
*.pyc
.env
.DS_Store
EOF
```

**Step 4: Create FastAPI Application** (30 min)

```python
# File: src/api/main.py

"""
DeFi Analytics Platform - FastAPI Backend
Day 001: Basic Setup
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict

# ====================================================================================
# INITIALIZE FastAPI APP
# ====================================================================================

app = FastAPI(
    title="DeFi Analytics Platform API",
    description="Comprehensive DeFi analytics for portfolio management and yield optimization",
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
# ENDPOINTS
# ====================================================================================

@app.get("/", tags=["General"])
async def root() -> Dict[str, str]:
    """
    Root endpoint - API information

    Returns basic information about the API
    """
    return {
        "message": "DeFi Analytics Platform API",
        "version": "1.0.0",
        "documentation": "/docs",
        "status": "operational"
    }


@app.get("/health", tags=["General"])
async def health_check() -> Dict[str, any]:
    """
    Health check endpoint

    Returns the health status of the API and its services
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "operational",
            "database": "not_configured",  # Will implement later
            "web3": "not_configured"       # Will implement later
        }
    }


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
```

**Step 5: Run the Server** (5 min)

```bash
# Navigate to API folder
cd src/api

# Run the server
python main.py

# You should see:
# ============================================================================
# DeFi ANALYTICS PLATFORM API
# ============================================================================
#
# Starting server...
# API Documentation: http://localhost:8000/docs
# Alternative docs: http://localhost:8000/redoc
#
# Press CTRL+C to stop
#
# INFO:     Started server process [12345]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Step 6: Test with curl** (10 min)

Open a new terminal and run:

```bash
# Test root endpoint
curl http://localhost:8000/

# Expected output:
# {
#   "message": "DeFi Analytics Platform API",
#   "version": "1.0.0",
#   "documentation": "/docs",
#   "status": "operational"
# }

# Test health endpoint
curl http://localhost:8000/health

# Expected output:
# {
#   "status": "healthy",
#   "timestamp": "2024-01-15T10:30:45.123456",
#   "services": {
#     "api": "operational",
#     "database": "not_configured",
#     "web3": "not_configured"
#   }
# }

# Test with formatted output
curl http://localhost:8000/health | jq

# Test with verbose output (see headers)
curl -v http://localhost:8000/health
```

**Step 7: Explore API Documentation** (10 min)

Open your browser and visit:

1. **Swagger UI**: http://localhost:8000/docs
   - Interactive API documentation
   - Try out endpoints directly
   - See request/response schemas

2. **ReDoc**: http://localhost:8000/redoc
   - Alternative documentation view
   - Better for reading
   - Cleaner layout

**Step 8: Verify Everything Works** (5 min)

Checklist:
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Server starts without errors
- [ ] `/` endpoint returns JSON
- [ ] `/health` endpoint returns status
- [ ] `/docs` shows Swagger UI
- [ ] curl tests work

**Congratulations!** 🎉

You've completed Day 1! You now have:
- ✅ Working FastAPI server
- ✅ Health check endpoint
- ✅ API documentation
- ✅ Development environment ready

**Next Steps** (Day 2):
- Add Pydantic request/response models
- Create POST endpoints with validation
- Implement error handling

**Troubleshooting**:

If server won't start:
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill existing process
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

If imports don't work:
```bash
# Make sure you're in the right directory
cd src/api

# Or use PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

---

## 📈 Progress Tracking

### Week 1 (Days 1-7)
- [x] Day 1: Environment setup ✓
- [ ] Day 2: Pydantic models
- [ ] Day 3: Data structures
- [ ] Day 4: Math functions
- [ ] Day 5: API routing
- [ ] Day 6: AMM theory
- [ ] Day 7: Slippage calculation

### Week 2 (Days 8-14)
- [ ] Day 8: Pool quality scoring
- [ ] Day 9: Impermanent loss
- [ ] Day 10: Concentrated liquidity
- [ ] Day 11: Curve StableSwap
- [ ] Day 12: Liquidity API complete
- [ ] Day 13: Smart contract risk model
- [ ] Day 14: Risk scoring algorithm

### Week 3 (Days 15-21)
- [ ] Day 15: Health factor & liquidation
- [ ] Day 16: Cascade modeling
- [ ] Day 17: Systemic risk
- [ ] Day 18: Risk API complete
- [ ] Day 19: Yield discovery
- [ ] Day 20: Yield ranking
- [ ] Day 21: Portfolio optimization

### Week 4 (Days 22-28)
- [ ] Day 22: Portfolio strategies
- [ ] Day 23: Performance monitoring
- [ ] Day 24: Yield API complete
- [ ] Day 25: Web3 setup
- [ ] Day 26: Smart contract data
- [ ] Day 27: Multi-protocol data
- [ ] Day 28: Caching & rate limiting

### Week 5 (Days 29-30)
- [ ] Day 29: Error handling
- [ ] Day 30: Documentation & testing

---

## 🚀 After Day 30: What's Next?

### Production Deployment
1. **Database Integration**
   - PostgreSQL for persistent storage
   - Historical data tracking
   - User portfolios

2. **Authentication**
   - JWT tokens
   - API keys
   - User accounts

3. **Advanced Features**
   - WebSocket real-time updates
   - Automated rebalancing
   - Price alerts

4. **Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Error tracking (Sentry)

5. **Deployment**
   - Docker containerization
   - Kubernetes orchestration
   - CI/CD pipeline

---

## 📚 Resources

### DeFi Concepts
- [Uniswap V2 Whitepaper](https://uniswap.org/whitepaper.pdf)
- [Uniswap V3 Whitepaper](https://uniswap.org/whitepaper-v3.pdf)
- [Aave Documentation](https://docs.aave.com/)
- [Curve StableSwap Paper](https://curve.fi/files/stableswap-paper.pdf)

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

### Web3
- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Ethereum JSON-RPC](https://ethereum.org/en/developers/docs/apis/json-rpc/)
- [The Graph Protocol](https://thegraph.com/docs/)

### Finance
- [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory)
- [Sharpe Ratio](https://en.wikipedia.org/wiki/Sharpe_ratio)
- [Value at Risk (VaR)](https://en.wikipedia.org/wiki/Value_at_risk)

---

## ❓ FAQ

### Q: Can I skip days?
**A**: Yes, but understand dependencies. Day 15 (liquidation risk) requires Day 13-14 (risk models). Day 21 (optimization) requires Day 19-20 (yield discovery).

### Q: What if I get stuck?
**A**:
1. Read the error message carefully
2. Check the API docs at `/docs`
3. Test with curl to isolate issues
4. Review previous day's code
5. Check file imports and paths

### Q: Do I need blockchain knowledge?
**A**: Basic understanding helps but isn't required for Days 1-24. Deep blockchain knowledge needed for Days 25-27 (Web3 integration).

### Q: Can I use a different database?
**A**: Yes! The tutorial uses PostgreSQL, but you can use MySQL, MongoDB, or any database. Just adapt the connection code.

### Q: Is this production-ready?
**A**: After Day 30, you'll have a production-ready backend. Add authentication, monitoring, and proper deployment for full production use.

---

## 📊 Summary

| Metric | Value |
|--------|-------|
| **Total Days** | 30 |
| **Time per Day** | 1-2 hours |
| **Total Time** | 30-60 hours |
| **Lines of Code** | ~6,125 |
| **Endpoints Built** | 17+ |
| **Skills Learned** | FastAPI, DeFi, Risk Management, Optimization, Web3 |
| **Difficulty** | Intermediate to Advanced |
| **Prerequisites** | Python, REST APIs, Basic Finance |

---

**Ready to start?** Jump to [Day 001](#day-001-environment-setup--project-structure) and begin your DeFi analytics journey!

---

*Built for Economics & Finance MSc students | MIT License | 2024*
