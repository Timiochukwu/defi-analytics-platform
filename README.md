# DeFi Analytics & Risk Management Platform

> **Comprehensive DeFi portfolio management, yield optimization, and risk assessment platform built for Economics & Finance MSc students**

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🎯 Overview

The **DeFi Analytics Platform** is a production-ready, research-grade system for analyzing, managing, and optimizing decentralized finance (DeFi) portfolios. Built specifically for Economics and Finance MSc students, this platform provides:

- **📊 Portfolio Management**: Build, monitor, and rebalance DeFi portfolios
- **💰 Yield Optimization**: Find and compare best yields across 15+ protocols
- **⚠️ Risk Assessment**: Comprehensive smart contract, liquidation, and systemic risk analysis
- **💧 Liquidity Analysis**: Calculate slippage, analyze pool depth, and score liquidity quality
- **🔬 Research Tools**: Academic-grade analytics suitable for thesis research

### Why This Platform?

Traditional finance tools don't work for DeFi. This platform addresses DeFi-specific challenges:

1. **Impermanent Loss**: Calculate IL for liquidity provider positions
2. **Liquidation Risk**: Monitor health factors and simulate price shock scenarios
3. **Smart Contract Risk**: Score protocols based on audits, code complexity, and time deployed
4. **Yield Sustainability**: Forecast whether high APYs are sustainable or temporary
5. **Multi-Protocol Optimization**: Optimize across Aave, Uniswap, Curve, and more

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- (Optional) Ethereum RPC endpoint (Infura, Alchemy)

### Installation

```bash
# Clone the repository
cd defi-analytics-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Dashboard

```bash
# Start Streamlit dashboard
streamlit run dashboard/defi_dashboard.py
```

Dashboard will open at `http://localhost:8501`

### Run the API

```bash
# Start FastAPI server
cd src/api
python main.py
```

API documentation available at `http://localhost:8000/docs`

---

## 📂 Project Structure

```
defi-analytics-platform/
│
├── data/                          # Data storage
│   ├── raw/                       # Raw data from protocols
│   └── processed/                 # Processed analytics data
│
├── src/                           # Source code
│   ├── data/
│   │   └── defi_data_collector.py    # Fetch data from Uniswap, Aave, Compound
│   │
│   ├── analytics/
│   │   └── liquidity_analyzer.py     # Slippage, depth, pool quality analysis
│   │
│   ├── risk/
│   │   └── defi_risk_models.py       # Smart contract, liquidation, systemic risk
│   │
│   ├── optimization/
│   │   ├── yield_optimizer.py        # Yield discovery and portfolio optimization
│   │   └── defi_portfolio.py         # Portfolio construction and rebalancing
│   │
│   └── api/
│       └── main.py                   # FastAPI REST API
│
├── dashboard/
│   └── defi_dashboard.py         # Streamlit interactive dashboard
│
├── reports/                       # Generated reports and analysis
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 💡 Key Features

### 1. Liquidity Analysis

**Calculate slippage before trading:**

```python
from analytics.liquidity_analyzer import LiquidityAnalyzer

analyzer = LiquidityAnalyzer()

# ETH/USDC pool: 1,000 ETH, 2,000,000 USDC
result = analyzer.calculate_slippage_constant_product(
    reserve_in=2_000_000,   # USDC reserve
    reserve_out=1_000,      # ETH reserve
    amount_in=10_000,       # Trade 10,000 USDC
    fee=0.003               # 0.3% fee
)

print(f"Slippage: {result.slippage_percent:.2f}%")
# Output: Slippage: 0.50%
```

**Score pool quality:**

```python
score = analyzer.calculate_pool_quality_score(
    tvl=100_000_000,         # $100M TVL
    volume_24h=80_000_000,   # $80M daily volume
    fee_tier=0.0005,         # 0.05% fee
    reserve_ratio=0.98       # Well-balanced
)

print(f"Pool Score: {score['overall_score']}/100 ({score['rating']})")
# Output: Pool Score: 93.5/100 (A+)
```

### 2. Risk Assessment

**Assess smart contract risk:**

```python
from risk.defi_risk_models import SmartContractRiskAnalyzer

analyzer = SmartContractRiskAnalyzer()

risk = analyzer.assess_smart_contract_risk(
    protocol_name="Aave",
    contract_address="0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",
    auditors=["Trail of Bits", "OpenZeppelin", "ConsenSys Diligence"],
    code_lines=15000,
    days_deployed=900,
    tvl_usd=5_000_000_000,
    upgrade_mechanism="Timelock + Multisig",
    has_bug_bounty=True,
    admin_control_level="Low"
)

print(f"Risk Score: {risk.overall_risk_score}/100 ({risk.risk_level.value})")
# Output: Risk Score: 18.2/100 (Very Low)
```

**Monitor liquidation risk:**

```python
from risk.defi_risk_models import LiquidationRiskAnalyzer

analyzer = LiquidationRiskAnalyzer()

risk = analyzer.assess_liquidation_risk(
    protocol_name="Aave",
    asset="ETH",
    collateral_value_usd=100_000,
    debt_value_usd=60_000
)

print(f"Health Factor: {risk.health_factor}")
print(f"Distance to Liquidation: {risk.distance_to_liquidation_percent:.2f}%")
# Output: Health Factor: 1.433
#         Distance to Liquidation: 30.23%
```

### 3. Yield Optimization

**Find best yields:**

```python
from optimization.yield_optimizer import YieldOpportunityAnalyzer

analyzer = YieldOpportunityAnalyzer()

# Rank opportunities by risk-adjusted returns
ranked = analyzer.rank_opportunities(
    opportunities=opportunity_list,
    risk_tolerance=RiskRating.MODERATE,
    min_liquidity=1_000_000,
    prefer_no_lock=True
)

print(ranked.head())
```

**Optimize portfolio:**

```python
from optimization.yield_optimizer import PortfolioOptimizer

optimizer = PortfolioOptimizer(risk_free_rate=0.02)

optimal = optimizer.optimize_max_sharpe(
    opportunities=opportunity_list,
    risk_tolerance=3.0,
    max_concentration=0.40
)

print(f"Expected APY: {optimal.total_expected_apy}%")
print(f"Sharpe Ratio: {optimal.sharpe_ratio}")
print("\nAllocations:")
for alloc in optimal.allocations:
    print(f"  {alloc['weight_percent']:.1f}% - {alloc['protocol']} ({alloc['apy']}% APY)")
```

### 4. Portfolio Management

**Build Conservative Portfolio:**

```python
from optimization.defi_portfolio import PortfolioConstructor

constructor = PortfolioConstructor()

portfolio = constructor.build_conservative_portfolio(
    capital_usd=100_000,
    min_yield_percent=2.0
)

print(f"Strategy: {portfolio['strategy']}")
print(f"Expected APY: {portfolio['expected_apy']}%")
print(f"Risk Score: {portfolio['portfolio_risk_score']}/100")
# Output: Strategy: Conservative
#         Expected APY: 4.1%
#         Risk Score: 18.5/100
```

**Build Balanced Portfolio:**

```python
portfolio = constructor.build_balanced_portfolio(
    capital_usd=100_000,
    target_apy=15.0
)

# Output: Expected APY: 9.5%
#         Risk Score: 28.5/100
#         Allocations: Aave 30%, Curve 25%, Uniswap V3 25%, Lido 15%, Yearn 5%
```

**Build Aggressive Portfolio:**

```python
portfolio = constructor.build_aggressive_portfolio(
    capital_usd=100_000,
    target_apy=40.0
)

# Output: Expected APY: 35.7%
#         Risk Score: 48.5/100
#         ⚠️ High volatility expected
```

---

## 🔬 For MSc Research

This platform is specifically designed to support academic research in:

### Research Topics

1. **Market Microstructure in DeFi**
   - Study liquidity provision strategies
   - Analyze price impact and slippage
   - Compare AMM designs (Uniswap V2 vs V3, Curve stableswap)

2. **Risk Management**
   - Liquidation cascade modeling
   - Systemic risk analysis
   - Smart contract vulnerability assessment

3. **Portfolio Theory**
   - Mean-variance optimization in DeFi
   - Risk parity strategies
   - Dynamic rebalancing

4. **Yield Economics**
   - Sustainability of high APYs
   - Token incentive analysis
   - Protocol revenue models

### Example Research Questions

**Q1: How does Uniswap V3 concentrated liquidity affect impermanent loss?**

```python
from analytics.liquidity_analyzer import LiquidityAnalyzer

analyzer = LiquidityAnalyzer()

# Analyze concentrated liquidity distribution
analysis = analyzer.analyze_concentrated_liquidity(
    current_price=2000,
    tick_spacing=10,
    liquidity_positions=[
        {'lower_price': 1900, 'upper_price': 2100, 'liquidity': 5_000_000},
        {'lower_price': 1800, 'upper_price': 2200, 'liquidity': 3_000_000},
        # More positions...
    ]
)

# Compare to Uniswap V2 (full-range liquidity)
# Conduct statistical analysis on IL differences
```

**Q2: What is the relationship between protocol TVL and liquidation risk in lending protocols?**

```python
from risk.defi_risk_models import LiquidationRiskAnalyzer

analyzer = LiquidationRiskAnalyzer()

# Simulate liquidation cascades under different TVL scenarios
cascade = analyzer.calculate_cascade_probability(
    positions=position_list,
    price_shock=0.20  # 20% drop
)

# Analyze amplification factor vs. total protocol TVL
# Run regression analysis
```

**Q3: How sustainable are current DeFi yields?**

```python
from optimization.yield_optimizer import YieldForecaster

forecaster = YieldForecaster()

forecast = forecaster.forecast_yield_sustainability(
    current_apy=0.50,  # 50% APY
    apy_history=historical_apy_data,
    protocol_revenue_apy=0.05,  # Only 5% from fees
    token_incentive_apy=0.45,   # 45% from token rewards
    tvl_growth_rate=0.15,       # 15% monthly growth
    token_emission_remaining_days=180
)

print(f"Sustainability Score: {forecast.sustainability_score}/100")
print(f"90-day forecast: {forecast.forecasted_apy_90d}%")
# Conclusion: Unsustainable, will drop to ~5% when incentives end
```

### Data Export for Analysis

All modules support DataFrame export for statistical analysis:

```python
# Export to CSV for R/Stata analysis
ranked_opportunities.to_csv('data/processed/yield_opportunities.csv')

# Export for LaTeX tables
print(ranked_opportunities.to_latex())

# Export for econometric analysis
import statsmodels.api as sm

# Run regression: APY ~ Risk + TVL + Age
model = sm.OLS(df['apy'], sm.add_constant(df[['risk_score', 'tvl', 'days_deployed']]))
results = model.fit()
print(results.summary())
```

---

## 🌐 REST API

Full REST API for programmatic access:

### Base URL
```
http://localhost:8000
```

### Key Endpoints

#### Liquidity Analysis

```bash
# Calculate slippage
POST /api/liquidity/slippage
{
  "reserve_in": 2000000,
  "reserve_out": 1000,
  "amount_in": 10000,
  "fee": 0.003
}

# Score pool quality
POST /api/liquidity/pool-quality
{
  "tvl": 100000000,
  "volume_24h": 80000000,
  "fee_tier": 0.0005,
  "reserve_ratio": 0.98
}
```

#### Risk Assessment

```bash
# Assess smart contract risk
POST /api/risk/smart-contract
{
  "protocol_name": "Aave",
  "auditors": ["Trail of Bits", "OpenZeppelin"],
  "code_lines": 15000,
  "days_deployed": 900,
  ...
}

# Assess liquidation risk
POST /api/risk/liquidation
{
  "protocol_name": "Aave",
  "asset": "ETH",
  "collateral_value_usd": 100000,
  "debt_value_usd": 60000
}
```

#### Yield Optimization

```bash
# Get yield opportunities
GET /api/yield/opportunities?min_apy=5&max_risk=3&min_tvl=1000000

# Build portfolio
POST /api/portfolio/build
{
  "capital_usd": 100000,
  "strategy": "balanced"
}
```

Full API documentation: `http://localhost:8000/docs`

---

## 📊 Dashboard Features

The Streamlit dashboard provides interactive analysis:

### 1. Overview Page
- Market statistics across protocols
- Top protocols by TVL
- Yield opportunities by risk level

### 2. Portfolio Builder
- Conservative, Balanced, and Aggressive strategies
- Interactive capital allocation
- Expected returns calculator
- Visual allocation charts

### 3. Yield Explorer
- Filter by APY, risk, and TVL
- Compare protocols side-by-side
- Risk-return scatter plots
- Detailed opportunity tables

### 4. Risk Assessment
- **Smart Contract Risk**: Evaluate protocol security
- **Liquidation Risk**: Calculate health factors and scenarios
- **Portfolio Risk**: Monitor overall portfolio health

### 5. Liquidity Analysis
- **Slippage Calculator**: Estimate trade execution price
- **Pool Quality Scorer**: Rate liquidity pools 0-100

---

## 🔧 Configuration

### Connect to Ethereum Mainnet

To fetch live data from protocols:

```python
# In src/data/defi_data_collector.py

# Option 1: Infura
WEB3_PROVIDER = "https://mainnet.infura.io/v3/YOUR_PROJECT_ID"

# Option 2: Alchemy
WEB3_PROVIDER = "https://eth-mainnet.alchemyapi.io/v2/YOUR_API_KEY"

# Option 3: Local node
WEB3_PROVIDER = "http://localhost:8545"
```

Get free API keys:
- [Infura](https://infura.io/)
- [Alchemy](https://www.alchemy.com/)

### Database Setup (Optional)

For production use with historical data tracking:

```bash
# Install PostgreSQL
# Create database
createdb defi_analytics

# Update connection string in src/utils/database.py
DATABASE_URL = "postgresql://user:password@localhost/defi_analytics"
```

---

## 🧪 Running Examples

All modules include comprehensive examples:

```bash
# Run liquidity analyzer examples
python src/analytics/liquidity_analyzer.py

# Run risk models examples
python src/risk/defi_risk_models.py

# Run yield optimizer examples
python src/optimization/yield_optimizer.py

# Run portfolio manager examples
python src/optimization/defi_portfolio.py
```

Each example demonstrates real-world use cases with detailed output.

---

## 📚 Code Documentation

Every module includes extensive inline documentation:

- **Plain English Explanations**: What each function does and why it matters
- **Real-World Examples**: Concrete scenarios and use cases
- **Formula Breakdowns**: Mathematical formulas with step-by-step explanations
- **Research Context**: How to use for academic research

Example documentation style:

```python
def calculate_impermanent_loss(self, price_start: float, price_end: float) -> Dict[str, float]:
    """
    Calculate impermanent loss for liquidity providers

    WHAT IS IMPERMANENT LOSS:
    When you provide liquidity to a pool (e.g., ETH/USDC), if prices change,
    you lose money compared to just holding the assets.

    FORMULA:
    IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1

    EXAMPLE:
    If ETH goes from $1000 to $2000 (2x):
    - Price ratio: 2.0
    - IL = 2 * sqrt(2) / (1 + 2) - 1 = -5.7%

    WHY IT MATTERS:
    You need to earn >5.7% from fees to break even!

    FOR RESEARCH:
    - Study IL vs. fee income tradeoffs
    - Analyze optimal LP strategies
    - Compare AMM designs
    """
```

---

## 🎓 Learning Path

### Beginner

1. Start with the **Dashboard** to understand DeFi concepts visually
2. Run the **example scripts** to see code in action
3. Read the **inline documentation** to learn formulas
4. Use the **API** for simple queries

### Intermediate

1. Build custom portfolios using `PortfolioConstructor`
2. Analyze specific protocols with risk models
3. Optimize yields for different risk profiles
4. Export data for statistical analysis

### Advanced

1. Extend models with custom strategies
2. Integrate live data from protocols
3. Build automated rebalancing bots
4. Conduct original research using the platform

---

## 🤝 Contributing

This is a research project. Contributions welcome:

1. Add support for new protocols (Balancer, Curve V2, etc.)
2. Implement additional risk models
3. Enhance optimization algorithms
4. Improve documentation
5. Report bugs

---

## ⚠️ Disclaimer

**FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY**

This platform is built for academic research and learning. It is NOT financial advice.

- Smart contracts can have bugs
- Historical performance ≠ future results
- DeFi protocols can fail
- You can lose all your money

**Always:**
- Do your own research (DYOR)
- Never invest more than you can afford to lose
- Understand the risks before investing
- Verify all data independently

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 📧 Contact

Built for Economics & Finance MSc students

Questions or suggestions? Open an issue on GitHub.

---

## 🙏 Acknowledgments

This platform uses data and concepts from:
- Uniswap V2/V3 documentation
- Aave Protocol documentation
- Curve Finance whitepaper
- Academic research on DeFi risk

Special thanks to the DeFi community for open-source protocols and documentation.

---

**Happy researching! 📊🎓**
