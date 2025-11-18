"""
=============================================================================
DeFi YIELD OPTIMIZER
=============================================================================

PURPOSE:
Find the best yield opportunities across DeFi protocols and optimize
asset allocation to maximize risk-adjusted returns.

WHAT IS YIELD FARMING:
Earning returns on crypto assets through:
1. Lending (Aave, Compound) - Earn interest on deposits
2. Liquidity Provision (Uniswap, Curve) - Earn trading fees
3. Staking (Lido, Rocket Pool) - Earn validation rewards
4. Yield Aggregation (Yearn, Beefy) - Auto-compound returns

FOR MSc RESEARCH:
- Study yield dynamics in DeFi vs traditional finance
- Analyze risk-return tradeoffs
- Research optimal portfolio allocation strategies
- Model yield sustainability and APY inflation

AUTHOR: Built for Economics & Finance MSc students
DATE: 2024
=============================================================================
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import math


# ====================================================================================
# ENUMS AND CONSTANTS
# ====================================================================================

class YieldType(Enum):
    """Types of yield opportunities"""
    LENDING = "Lending"              # Aave, Compound
    LP_FEES = "Liquidity Provider"   # Uniswap, Curve
    STAKING = "Staking"              # ETH staking, governance
    FARMING = "Yield Farming"        # Token rewards
    VAULT = "Yield Vault"            # Yearn, Beefy
    STABLE_FARM = "Stable Farming"   # Low-risk stablecoin yields


class RiskRating(Enum):
    """Risk ratings for yield strategies"""
    VERY_LOW = 1    # Stablecoins on blue-chip protocols
    LOW = 2         # Major assets on established protocols
    MODERATE = 3    # Liquidity provision on majors
    HIGH = 4        # New protocols or volatile assets
    VERY_HIGH = 5   # Exotic pairs or unaudited protocols


# ====================================================================================
# DATA STRUCTURES
# ====================================================================================

@dataclass
class YieldOpportunity:
    """
    A single yield opportunity

    EXAMPLE:
    - Protocol: Aave
    - Asset: USDC
    - APY: 3.5%
    - TVL: $2B
    - Risk: Very Low
    """
    protocol_name: str
    pool_name: str
    asset: str
    apy: float              # Annual Percentage Yield (decimal, e.g., 0.035 = 3.5%)
    apy_breakdown: Dict[str, float]  # {'base': 0.02, 'rewards': 0.015}
    tvl_usd: float
    liquidity_depth: float  # How much can be deposited without affecting APY
    yield_type: YieldType
    risk_rating: RiskRating
    lock_period_days: int   # 0 = no lock
    impermanent_loss_risk: Optional[float]  # For LP positions
    smart_contract_risk: float  # 0-100
    last_updated: datetime


@dataclass
class OptimalAllocation:
    """
    Optimal portfolio allocation across strategies

    EXAMPLE OUTPUT:
    - 40% USDC in Aave (3.5% APY, Very Low Risk)
    - 30% ETH/USDC LP on Uniswap (25% APY, Moderate Risk)
    - 30% ETH Staking via Lido (4.2% APY, Low Risk)
    Expected Portfolio APY: 9.2%
    """
    allocations: List[Dict]     # List of {opportunity, weight, expected_return}
    total_expected_apy: float
    total_risk_score: float
    sharpe_ratio: float
    diversification_score: float
    warnings: List[str]


@dataclass
class YieldForecast:
    """
    Forecast of yield sustainability

    WHY FORECAST:
    Many DeFi yields are unsustainable:
    - Token rewards may run out
    - APYs drop as more capital enters
    - Protocol incentives change

    FAMOUS EXAMPLE:
    Anchor Protocol offered 20% on stablecoins → unsustainable → collapsed
    """
    current_apy: float
    forecasted_apy_30d: float
    forecasted_apy_90d: float
    sustainability_score: float  # 0-100
    risk_of_collapse: float      # 0-1
    key_assumptions: List[str]


# ====================================================================================
# YIELD OPPORTUNITY ANALYZER
# ====================================================================================

class YieldOpportunityAnalyzer:
    """
    Analyze and compare yield opportunities

    WHAT IT DOES:
    1. Fetch yields from multiple protocols
    2. Calculate risk-adjusted returns
    3. Account for hidden costs (gas, IL, lock periods)
    4. Rank opportunities
    """

    def __init__(self):
        """Initialize the analyzer"""
        pass


    def calculate_real_apy(
        self,
        nominal_apy: float,
        gas_cost_usd: float,
        deposit_amount: float,
        hold_period_days: int = 365,
        compounding_frequency: int = 365
    ) -> Dict[str, float]:
        """
        Calculate real APY after accounting for costs

        WHY THIS MATTERS:
        Advertised APYs are often misleading:
        - Don't include gas costs
        - Assume perfect compounding
        - Ignore price volatility

        EXAMPLE:
        - Advertised: 100% APY
        - Deposit: $1,000
        - Gas costs: $200 (deposit + claim + withdraw)
        - Real APY after gas: 80%

        Small deposits can have negative real yields due to gas!

        Args:
            nominal_apy: Advertised APY (e.g., 0.50 for 50%)
            gas_cost_usd: Total gas costs (deposit + harvest + withdraw)
            deposit_amount: Amount to deposit
            hold_period_days: How long you'll hold (affects gas impact)
            compounding_frequency: Times per year APY is compounded

        Returns:
            Dictionary with real APY calculations
        """
        # Convert to daily rate
        daily_rate = (1 + nominal_apy) ** (1/365) - 1

        # Calculate returns over hold period
        days = hold_period_days
        gross_return = deposit_amount * ((1 + daily_rate) ** days - 1)

        # Subtract gas costs
        net_return = gross_return - gas_cost_usd

        # Calculate real APY
        if deposit_amount > 0 and days > 0:
            # Annualize the return
            real_apy = ((net_return / deposit_amount) + 1) ** (365 / days) - 1
        else:
            real_apy = 0

        # Calculate break-even deposit amount (where gas costs = 0 real APY)
        if nominal_apy > 0 and hold_period_days > 0:
            # Solve: gas_cost = deposit * ((1 + daily_rate)^days - 1)
            breakeven_deposit = gas_cost_usd / ((1 + daily_rate) ** days - 1)
        else:
            breakeven_deposit = float('inf')

        return {
            'nominal_apy': round(nominal_apy * 100, 2),
            'real_apy': round(real_apy * 100, 2),
            'gross_return_usd': round(gross_return, 2),
            'gas_cost_usd': round(gas_cost_usd, 2),
            'net_return_usd': round(net_return, 2),
            'gas_impact_percent': round((gas_cost_usd / gross_return * 100) if gross_return > 0 else 100, 2),
            'breakeven_deposit': round(breakeven_deposit, 2),
            'is_profitable': net_return > 0
        }


    def calculate_impermanent_loss_adjusted_apy(
        self,
        lp_apy: float,
        price_change_percent: float,
        correlation: float = 0.0
    ) -> Dict[str, float]:
        """
        Calculate APY adjusted for impermanent loss (IL)

        WHAT IS IMPERMANENT LOSS:
        When you provide liquidity to a pool (e.g., ETH/USDC), if prices change,
        you lose money compared to just holding the assets.

        EXAMPLE:
        - Deposit: 1 ETH + 2,000 USDC (when ETH = $2,000)
        - ETH rises to $3,000
        - IL: ~5.7% loss
        - If LP APY is 25%, net return: 25% - 5.7% = 19.3%

        FORMULA:
        IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1

        Args:
            lp_apy: Liquidity provider APY from fees/rewards
            price_change_percent: Expected price change of asset (e.g., 0.50 for +50%)
            correlation: Correlation between assets (0 = uncorrelated, 1 = perfect)

        Returns:
            Dictionary with IL-adjusted returns
        """
        # Calculate impermanent loss
        if correlation < 0.99:  # If not perfectly correlated
            price_ratio = 1 + price_change_percent
            il_percent = (2 * math.sqrt(price_ratio) / (1 + price_ratio) - 1) * 100
        else:
            # Perfectly correlated assets (e.g., stablecoins) have no IL
            il_percent = 0

        # Adjust APY for IL
        adjusted_apy = (lp_apy * 100) + il_percent  # IL is negative

        # Calculate break-even APY (APY needed to offset IL)
        breakeven_apy = abs(il_percent)

        return {
            'lp_apy': round(lp_apy * 100, 2),
            'impermanent_loss_percent': round(il_percent, 2),
            'adjusted_apy': round(adjusted_apy, 2),
            'breakeven_apy': round(breakeven_apy, 2),
            'is_profitable': adjusted_apy > 0,
            'recommendation': self._il_recommendation(lp_apy * 100, il_percent)
        }


    def _il_recommendation(self, lp_apy: float, il_percent: float) -> str:
        """Generate recommendation based on IL vs APY"""
        net = lp_apy + il_percent

        if net > 20:
            return "Excellent - High rewards more than offset IL risk"
        elif net > 10:
            return "Good - Positive returns expected despite IL"
        elif net > 0:
            return "Moderate - Small positive return after IL"
        elif net > -5:
            return "Caution - IL may exceed rewards"
        else:
            return "Not Recommended - High IL risk, insufficient rewards"


    def rank_opportunities(
        self,
        opportunities: List[YieldOpportunity],
        risk_tolerance: RiskRating = RiskRating.MODERATE,
        min_liquidity: float = 1_000_000,
        prefer_no_lock: bool = True
    ) -> pd.DataFrame:
        """
        Rank yield opportunities by risk-adjusted returns

        RANKING METHODOLOGY:
        1. Filter by risk tolerance and liquidity
        2. Calculate risk-adjusted APY (APY / risk_score)
        3. Apply penalties for locks, low liquidity, high SC risk
        4. Sort by adjusted score

        WHY RISK-ADJUSTED:
        - 50% APY with Very High risk may be worse than
        - 10% APY with Very Low risk

        Args:
            opportunities: List of YieldOpportunity objects
            risk_tolerance: Maximum acceptable risk
            min_liquidity: Minimum TVL required
            prefer_no_lock: Penalize locked positions

        Returns:
            DataFrame with ranked opportunities
        """
        rankings = []

        for opp in opportunities:
            # Filter by risk tolerance
            if opp.risk_rating.value > risk_tolerance.value:
                continue

            # Filter by liquidity
            if opp.tvl_usd < min_liquidity:
                continue

            # Base score: APY
            base_score = opp.apy * 100

            # Risk adjustment (divide by risk level)
            risk_adjusted_score = base_score / opp.risk_rating.value

            # Penalty for lock periods
            if prefer_no_lock and opp.lock_period_days > 0:
                lock_penalty = min(20, opp.lock_period_days / 365 * 30)
                risk_adjusted_score -= lock_penalty

            # Penalty for smart contract risk
            sc_penalty = opp.smart_contract_risk / 10  # 0-10 point penalty
            risk_adjusted_score -= sc_penalty

            # Bonus for high liquidity depth
            if opp.liquidity_depth > 10_000_000:
                risk_adjusted_score += 5
            elif opp.liquidity_depth > 100_000_000:
                risk_adjusted_score += 10

            # Penalty for impermanent loss risk
            if opp.impermanent_loss_risk:
                risk_adjusted_score -= opp.impermanent_loss_risk * 10

            rankings.append({
                'rank': 0,  # Will be assigned after sorting
                'protocol': opp.protocol_name,
                'pool': opp.pool_name,
                'asset': opp.asset,
                'apy_percent': round(opp.apy * 100, 2),
                'tvl_millions': round(opp.tvl_usd / 1_000_000, 2),
                'risk_rating': opp.risk_rating.name,
                'yield_type': opp.yield_type.value,
                'lock_days': opp.lock_period_days,
                'risk_adjusted_score': round(risk_adjusted_score, 2),
                'il_risk': opp.impermanent_loss_risk,
                'sc_risk': opp.smart_contract_risk
            })

        # Sort by risk-adjusted score
        df = pd.DataFrame(rankings)
        if not df.empty:
            df = df.sort_values('risk_adjusted_score', ascending=False).reset_index(drop=True)
            df['rank'] = range(1, len(df) + 1)

        return df


# ====================================================================================
# PORTFOLIO OPTIMIZER
# ====================================================================================

class PortfolioOptimizer:
    """
    Optimize portfolio allocation across yield strategies

    OPTIMIZATION GOALS:
    1. Maximize expected returns
    2. Minimize risk
    3. Ensure diversification
    4. Stay within risk tolerance

    METHODS:
    - Mean-Variance Optimization (Markowitz)
    - Risk Parity
    - Maximum Sharpe Ratio
    """

    def __init__(self, risk_free_rate: float = 0.02):
        """
        Initialize optimizer

        Args:
            risk_free_rate: Risk-free rate for Sharpe calculation (default 2%)
        """
        self.risk_free_rate = risk_free_rate


    def optimize_max_sharpe(
        self,
        opportunities: List[YieldOpportunity],
        risk_tolerance: float = 3.0,
        max_concentration: float = 0.40
    ) -> OptimalAllocation:
        """
        Optimize for maximum Sharpe ratio

        WHAT IS SHARPE RATIO:
        (Return - Risk_Free_Rate) / Risk

        Higher Sharpe = better risk-adjusted returns

        EXAMPLE:
        - Strategy A: 30% return, 20% volatility → Sharpe = (30-2)/20 = 1.4
        - Strategy B: 15% return, 5% volatility → Sharpe = (15-2)/5 = 2.6
        Strategy B is better risk-adjusted!

        Args:
            opportunities: List of opportunities to consider
            risk_tolerance: Max average risk level (1-5)
            max_concentration: Max % in single strategy (e.g., 0.40 = 40%)

        Returns:
            OptimalAllocation with weights and metrics
        """
        if not opportunities:
            return self._empty_allocation()

        # Filter by risk tolerance
        filtered_opps = [
            opp for opp in opportunities
            if opp.risk_rating.value <= risk_tolerance
        ]

        if not filtered_opps:
            return self._empty_allocation()

        # Simple optimization (for demo - in production use scipy.optimize)
        # Strategy: Weight by APY/Risk ratio, subject to max concentration
        scores = []
        for opp in filtered_opps:
            risk_adjusted_return = (opp.apy * 100) / opp.risk_rating.value
            scores.append(risk_adjusted_return)

        total_score = sum(scores)

        # Calculate initial weights
        weights = [score / total_score for score in scores]

        # Apply max concentration constraint
        weights = [min(w, max_concentration) for w in weights]

        # Renormalize to sum to 1
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        else:
            # Equal weight fallback
            weights = [1.0 / len(filtered_opps)] * len(filtered_opps)

        # Calculate portfolio metrics
        allocations = []
        total_apy = 0
        total_risk = 0

        for opp, weight in zip(filtered_opps, weights):
            if weight < 0.01:  # Skip allocations < 1%
                continue

            expected_return = opp.apy * weight
            total_apy += expected_return
            total_risk += (opp.risk_rating.value * weight)

            allocations.append({
                'protocol': opp.protocol_name,
                'pool': opp.pool_name,
                'asset': opp.asset,
                'weight_percent': round(weight * 100, 2),
                'apy': round(opp.apy * 100, 2),
                'contribution_to_portfolio_apy': round(expected_return * 100, 2),
                'risk_rating': opp.risk_rating.name,
                'yield_type': opp.yield_type.value
            })

        # Calculate Sharpe ratio
        if total_risk > 0:
            sharpe = (total_apy - self.risk_free_rate) / (total_risk / 3.0)  # Normalize risk to ~volatility
        else:
            sharpe = 0

        # Calculate diversification score
        # Higher is better (using Herfindahl index)
        diversification_score = self._calculate_diversification_score(weights)

        # Generate warnings
        warnings = []
        if total_risk > risk_tolerance:
            warnings.append(f"Portfolio risk ({total_risk:.2f}) exceeds tolerance ({risk_tolerance})")
        if max(weights) > max_concentration:
            warnings.append(f"Concentration risk: {max(weights)*100:.1f}% in single strategy")
        if len(allocations) < 3:
            warnings.append("Low diversification: consider more strategies")

        return OptimalAllocation(
            allocations=allocations,
            total_expected_apy=round(total_apy * 100, 2),
            total_risk_score=round(total_risk, 2),
            sharpe_ratio=round(sharpe, 3),
            diversification_score=round(diversification_score, 2),
            warnings=warnings
        )


    def optimize_risk_parity(
        self,
        opportunities: List[YieldOpportunity],
        target_risk: float = 2.5
    ) -> OptimalAllocation:
        """
        Optimize using Risk Parity approach

        WHAT IS RISK PARITY:
        Instead of equal dollar weights, allocate so each strategy
        contributes equally to portfolio risk.

        EXAMPLE:
        - Strategy A: 20% APY, Very High risk (5) → allocate 10%
        - Strategy B: 5% APY, Very Low risk (1) → allocate 50%
        Result: Balanced risk contribution

        WHY USE IT:
        - More stable returns
        - Less dependent on any single strategy
        - Popular in institutional investing

        Args:
            opportunities: List of opportunities
            target_risk: Target average risk level

        Returns:
            OptimalAllocation with risk-balanced weights
        """
        if not opportunities:
            return self._empty_allocation()

        # Calculate inverse risk weights
        # Lower risk → higher weight
        inverse_risks = [1.0 / opp.risk_rating.value for opp in opportunities]
        total_inverse_risk = sum(inverse_risks)

        weights = [ir / total_inverse_risk for ir in inverse_risks]

        # Calculate metrics
        allocations = []
        total_apy = 0
        total_risk = 0
        risk_contributions = []

        for opp, weight in zip(opportunities, weights):
            if weight < 0.01:
                continue

            expected_return = opp.apy * weight
            risk_contribution = opp.risk_rating.value * weight

            total_apy += expected_return
            total_risk += risk_contribution
            risk_contributions.append(risk_contribution)

            allocations.append({
                'protocol': opp.protocol_name,
                'pool': opp.pool_name,
                'asset': opp.asset,
                'weight_percent': round(weight * 100, 2),
                'apy': round(opp.apy * 100, 2),
                'contribution_to_portfolio_apy': round(expected_return * 100, 2),
                'risk_contribution': round(risk_contribution, 2),
                'risk_rating': opp.risk_rating.name,
                'yield_type': opp.yield_type.value
            })

        # Sharpe ratio
        sharpe = (total_apy - self.risk_free_rate) / (total_risk / 3.0) if total_risk > 0 else 0

        # Diversification
        diversification_score = self._calculate_diversification_score(weights)

        # Warnings
        warnings = []
        if total_risk > target_risk:
            warnings.append(f"Portfolio risk ({total_risk:.2f}) exceeds target ({target_risk})")

        # Check if risk is truly balanced
        risk_std = np.std(risk_contributions) if risk_contributions else 0
        if risk_std > 0.5:
            warnings.append("Risk contributions are not well-balanced")

        return OptimalAllocation(
            allocations=allocations,
            total_expected_apy=round(total_apy * 100, 2),
            total_risk_score=round(total_risk, 2),
            sharpe_ratio=round(sharpe, 3),
            diversification_score=round(diversification_score, 2),
            warnings=warnings
        )


    def _calculate_diversification_score(self, weights: List[float]) -> float:
        """
        Calculate diversification using Herfindahl-Hirschman Index

        FORMULA:
        HHI = sum of squared weights
        Diversification Score = (1 - HHI) * 100

        INTERPRETATION:
        - 0: Fully concentrated (all in one)
        - 100: Perfectly diversified (equal weights across many)
        """
        if not weights:
            return 0

        hhi = sum(w ** 2 for w in weights)
        # Normalize: perfect diversification (equal weights) should give 100
        n = len(weights)
        perfect_hhi = 1 / n if n > 0 else 1
        diversification = (1 - (hhi - perfect_hhi) / (1 - perfect_hhi)) * 100 if n > 1 else 0

        return max(0, min(100, diversification))


    def _empty_allocation(self) -> OptimalAllocation:
        """Return empty allocation"""
        return OptimalAllocation(
            allocations=[],
            total_expected_apy=0,
            total_risk_score=0,
            sharpe_ratio=0,
            diversification_score=0,
            warnings=["No suitable opportunities found"]
        )


# ====================================================================================
# YIELD FORECASTER
# ====================================================================================

class YieldForecaster:
    """
    Forecast yield sustainability

    WHY FORECAST:
    Many DeFi yields are temporary:
    - Token incentives run out
    - APY drops as more capital enters
    - Protocol economics change

    FORECASTING FACTORS:
    1. Historical APY trend
    2. Token emission schedule
    3. Protocol revenue vs. incentives
    4. TVL growth rate
    """

    def __init__(self):
        """Initialize forecaster"""
        pass


    def forecast_yield_sustainability(
        self,
        current_apy: float,
        apy_history: List[float],
        protocol_revenue_apy: float,
        token_incentive_apy: float,
        tvl_growth_rate: float,
        token_emission_remaining_days: Optional[int] = None
    ) -> YieldForecast:
        """
        Forecast yield sustainability

        METHODOLOGY:
        1. Separate sustainable (protocol revenue) vs. unsustainable (token incentives)
        2. Model APY decay as TVL grows
        3. Project incentive end date
        4. Calculate sustainability score

        EXAMPLE:
        - Current APY: 50%
        - Protocol revenue: 5% (sustainable)
        - Token incentives: 45% (unsustainable)
        - Forecast: APY will drop to ~5% when incentives end

        Args:
            current_apy: Current total APY
            apy_history: Historical APY values (past 30-90 days)
            protocol_revenue_apy: APY from actual protocol fees (sustainable)
            token_incentive_apy: APY from token rewards (often unsustainable)
            tvl_growth_rate: Monthly TVL growth rate (e.g., 0.20 for 20%/month)
            token_emission_remaining_days: Days until token incentives end

        Returns:
            YieldForecast with projections
        """
        # Calculate APY trend
        if len(apy_history) >= 7:
            recent_apy = np.mean(apy_history[-7:])
            older_apy = np.mean(apy_history[:7])
            apy_trend = (recent_apy - older_apy) / older_apy if older_apy > 0 else 0
        else:
            apy_trend = 0

        # Forecast 30-day APY
        # Assumption: APY declines as TVL grows (dilution effect)
        tvl_impact_30d = 1 / (1 + tvl_growth_rate) if tvl_growth_rate > 0 else 1
        forecasted_apy_30d = (protocol_revenue_apy + token_incentive_apy * tvl_impact_30d)

        # Forecast 90-day APY
        tvl_impact_90d = 1 / ((1 + tvl_growth_rate) ** 3) if tvl_growth_rate > 0 else 1

        # Check if incentives run out
        if token_emission_remaining_days and token_emission_remaining_days < 90:
            # Incentives end during forecast period
            days_ratio = token_emission_remaining_days / 90
            forecasted_apy_90d = protocol_revenue_apy + token_incentive_apy * tvl_impact_90d * days_ratio
        else:
            forecasted_apy_90d = protocol_revenue_apy + token_incentive_apy * tvl_impact_90d

        # Calculate sustainability score (0-100)
        # Higher % from protocol revenue = more sustainable
        revenue_ratio = protocol_revenue_apy / current_apy if current_apy > 0 else 0
        sustainability_score = revenue_ratio * 100

        # Adjust for trends
        if apy_trend < -0.20:  # Declining >20%
            sustainability_score *= 0.8
        elif apy_trend > 0.10:  # Growing >10%
            sustainability_score *= 1.1

        sustainability_score = min(100, max(0, sustainability_score))

        # Calculate risk of collapse
        # High if: unsustainable yield, declining trend, incentives ending soon
        collapse_risk = 0

        # Factor 1: Unsustainable yield
        if revenue_ratio < 0.30:  # < 30% from protocol revenue
            collapse_risk += 0.4

        # Factor 2: Negative trend
        if apy_trend < -0.20:
            collapse_risk += 0.3

        # Factor 3: Incentives ending
        if token_emission_remaining_days and token_emission_remaining_days < 180:
            collapse_risk += 0.3

        collapse_risk = min(1.0, collapse_risk)

        # Key assumptions
        assumptions = [
            f"Protocol revenue APY: {protocol_revenue_apy*100:.1f}% (sustainable)",
            f"Token incentive APY: {token_incentive_apy*100:.1f}% (may be temporary)",
            f"TVL growth: {tvl_growth_rate*100:.1f}% per month",
        ]

        if token_emission_remaining_days:
            assumptions.append(f"Token incentives end in {token_emission_remaining_days} days")

        return YieldForecast(
            current_apy=round(current_apy * 100, 2),
            forecasted_apy_30d=round(forecasted_apy_30d * 100, 2),
            forecasted_apy_90d=round(forecasted_apy_90d * 100, 2),
            sustainability_score=round(sustainability_score, 2),
            risk_of_collapse=round(collapse_risk, 3),
            key_assumptions=assumptions
        )


# ====================================================================================
# EXAMPLE USAGE FOR MSc STUDENTS
# ====================================================================================

if __name__ == "__main__":
    """
    Example usage demonstrating yield optimization
    """
    print("=" * 80)
    print("DeFi YIELD OPTIMIZER - EXAMPLE USAGE")
    print("=" * 80)

    # Initialize tools
    opp_analyzer = YieldOpportunityAnalyzer()
    portfolio_optimizer = PortfolioOptimizer(risk_free_rate=0.02)
    forecaster = YieldForecaster()

    # ========================================
    # Example 1: Real APY Calculation
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Real APY After Gas Costs")
    print("=" * 80)

    # Test different deposit sizes
    deposit_sizes = [500, 1000, 5000, 10000, 50000]
    nominal_apy = 0.50  # 50% APY
    gas_cost = 150      # $150 in gas fees

    print(f"\nNominal APY: {nominal_apy*100}%")
    print(f"Gas Costs: ${gas_cost}")
    print("\nReal APY by deposit size:")

    for size in deposit_sizes:
        result = opp_analyzer.calculate_real_apy(
            nominal_apy=nominal_apy,
            gas_cost_usd=gas_cost,
            deposit_amount=size,
            hold_period_days=365
        )
        print(f"\n  ${size:,} deposit:")
        print(f"    Real APY: {result['real_apy']}%")
        print(f"    Gas Impact: {result['gas_impact_percent']}%")
        print(f"    Net Return: ${result['net_return_usd']}")
        print(f"    Profitable: {result['is_profitable']}")

    # ========================================
    # Example 2: Impermanent Loss Analysis
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Impermanent Loss Adjusted Returns")
    print("=" * 80)

    lp_apy = 0.25  # 25% APY from LP fees
    price_changes = [-0.50, -0.30, -0.10, 0, 0.10, 0.30, 0.50, 1.00]

    print(f"\nLP APY: {lp_apy*100}%\n")
    print("Price Change | IL % | Adjusted APY | Recommendation")
    print("-" * 75)

    for change in price_changes:
        result = opp_analyzer.calculate_impermanent_loss_adjusted_apy(
            lp_apy=lp_apy,
            price_change_percent=change
        )
        print(f"{change*100:>+11.0f}% | {result['impermanent_loss_percent']:>6.2f}% | "
              f"{result['adjusted_apy']:>11.2f}% | {result['recommendation']}")

    # ========================================
    # Example 3: Ranking Opportunities
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Ranking Yield Opportunities")
    print("=" * 80)

    # Create sample opportunities
    opportunities = [
        YieldOpportunity(
            protocol_name="Aave",
            pool_name="USDC Lending",
            asset="USDC",
            apy=0.035,
            apy_breakdown={'base': 0.035},
            tvl_usd=2_000_000_000,
            liquidity_depth=500_000_000,
            yield_type=YieldType.LENDING,
            risk_rating=RiskRating.VERY_LOW,
            lock_period_days=0,
            impermanent_loss_risk=None,
            smart_contract_risk=15,
            last_updated=datetime.now()
        ),
        YieldOpportunity(
            protocol_name="Curve",
            pool_name="3pool",
            asset="USDC/USDT/DAI",
            apy=0.08,
            apy_breakdown={'base': 0.03, 'rewards': 0.05},
            tvl_usd=1_500_000_000,
            liquidity_depth=200_000_000,
            yield_type=YieldType.LP_FEES,
            risk_rating=RiskRating.LOW,
            lock_period_days=0,
            impermanent_loss_risk=0.01,
            smart_contract_risk=20,
            last_updated=datetime.now()
        ),
        YieldOpportunity(
            protocol_name="Uniswap V3",
            pool_name="ETH/USDC 0.05%",
            asset="ETH/USDC",
            apy=0.25,
            apy_breakdown={'base': 0.20, 'rewards': 0.05},
            tvl_usd=800_000_000,
            liquidity_depth=100_000_000,
            yield_type=YieldType.LP_FEES,
            risk_rating=RiskRating.MODERATE,
            lock_period_days=0,
            impermanent_loss_risk=0.15,
            smart_contract_risk=25,
            last_updated=datetime.now()
        ),
        YieldOpportunity(
            protocol_name="Yearn",
            pool_name="USDC Vault",
            asset="USDC",
            apy=0.12,
            apy_breakdown={'base': 0.12},
            tvl_usd=300_000_000,
            liquidity_depth=50_000_000,
            yield_type=YieldType.VAULT,
            risk_rating=RiskRating.LOW,
            lock_period_days=0,
            impermanent_loss_risk=None,
            smart_contract_risk=30,
            last_updated=datetime.now()
        ),
        YieldOpportunity(
            protocol_name="New Protocol",
            pool_name="High Yield Pool",
            asset="EXOTIC",
            apy=1.20,  # 120% APY!
            apy_breakdown={'base': 0.20, 'rewards': 1.00},
            tvl_usd=5_000_000,
            liquidity_depth=1_000_000,
            yield_type=YieldType.FARMING,
            risk_rating=RiskRating.VERY_HIGH,
            lock_period_days=90,
            impermanent_loss_risk=0.50,
            smart_contract_risk=80,
            last_updated=datetime.now()
        ),
    ]

    # Rank for conservative investor
    print("\nRanking for CONSERVATIVE investor (max Moderate risk):")
    conservative_ranking = opp_analyzer.rank_opportunities(
        opportunities=opportunities,
        risk_tolerance=RiskRating.MODERATE,
        min_liquidity=100_000_000,
        prefer_no_lock=True
    )
    print(conservative_ranking.to_string(index=False))

    # ========================================
    # Example 4: Portfolio Optimization
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Portfolio Optimization")
    print("=" * 80)

    # Max Sharpe optimization
    print("\nMAX SHARPE RATIO OPTIMIZATION:")
    optimal = portfolio_optimizer.optimize_max_sharpe(
        opportunities=opportunities,
        risk_tolerance=3.0,
        max_concentration=0.40
    )

    print(f"\nExpected Portfolio APY: {optimal.total_expected_apy}%")
    print(f"Portfolio Risk Score: {optimal.total_risk_score}/5")
    print(f"Sharpe Ratio: {optimal.sharpe_ratio}")
    print(f"Diversification Score: {optimal.diversification_score}/100")

    print("\nAllocations:")
    for alloc in optimal.allocations:
        print(f"  {alloc['weight_percent']:>5.1f}% - {alloc['protocol']} {alloc['pool']} "
              f"({alloc['apy']}% APY, {alloc['risk_rating']} risk)")

    if optimal.warnings:
        print("\nWarnings:")
        for warning in optimal.warnings:
            print(f"  ⚠ {warning}")

    # Risk Parity optimization
    print("\n\nRISK PARITY OPTIMIZATION:")
    risk_parity = portfolio_optimizer.optimize_risk_parity(
        opportunities=opportunities[:4],  # Exclude very risky one
        target_risk=2.0
    )

    print(f"\nExpected Portfolio APY: {risk_parity.total_expected_apy}%")
    print(f"Portfolio Risk Score: {risk_parity.total_risk_score}/5")
    print(f"Sharpe Ratio: {risk_parity.sharpe_ratio}")
    print(f"Diversification Score: {risk_parity.diversification_score}/100")

    print("\nAllocations:")
    for alloc in risk_parity.allocations:
        print(f"  {alloc['weight_percent']:>5.1f}% - {alloc['protocol']} {alloc['pool']} "
              f"(Risk Contribution: {alloc['risk_contribution']:.2f})")

    # ========================================
    # Example 5: Yield Forecasting
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Yield Sustainability Forecasting")
    print("=" * 80)

    # Forecast for a high-yield farm
    apy_history = [0.60, 0.58, 0.55, 0.53, 0.50, 0.48, 0.45]  # Declining trend

    forecast = forecaster.forecast_yield_sustainability(
        current_apy=0.45,
        apy_history=apy_history,
        protocol_revenue_apy=0.05,   # Only 5% is sustainable
        token_incentive_apy=0.40,    # 40% from token rewards
        tvl_growth_rate=0.15,        # 15% monthly TVL growth
        token_emission_remaining_days=120
    )

    print(f"\nYield Forecast:")
    print(f"  Current APY: {forecast.current_apy}%")
    print(f"  Forecasted APY (30 days): {forecast.forecasted_apy_30d}%")
    print(f"  Forecasted APY (90 days): {forecast.forecasted_apy_90d}%")
    print(f"  Sustainability Score: {forecast.sustainability_score}/100")
    print(f"  Risk of Collapse: {forecast.risk_of_collapse*100:.1f}%")

    print(f"\n  Key Assumptions:")
    for assumption in forecast.key_assumptions:
        print(f"    - {assumption}")

    print("\n" + "=" * 80)
    print("Yield optimization complete! Use these tools for your DeFi research.")
    print("=" * 80)
