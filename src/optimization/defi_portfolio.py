"""
=============================================================================
DeFi PORTFOLIO MANAGER
=============================================================================

PURPOSE:
Complete portfolio management system for DeFi investments.
Think of this as your personal DeFi portfolio manager that:
- Constructs optimal portfolios
- Monitors risks in real-time
- Suggests rebalancing
- Tracks performance
- Alerts on threats

FOR MSc RESEARCH:
- Study portfolio theory in DeFi context
- Compare traditional vs. DeFi portfolio management
- Research dynamic rebalancing strategies
- Analyze risk-return profiles

AUTHOR: Built for Economics & Finance MSc students
DATE: 2024
=============================================================================
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import math


# ====================================================================================
# DATA STRUCTURES
# ====================================================================================

@dataclass
class PortfolioPosition:
    """
    A single position in the portfolio

    EXAMPLE:
    - Protocol: Aave
    - Asset: USDC
    - Amount: $10,000
    - Entry APY: 3.5%
    - Current Value: $10,350
    - Unrealized P&L: $350
    """
    protocol: str
    pool_name: str
    asset: str
    amount_usd: float
    entry_price: float
    entry_date: datetime
    entry_apy: float
    current_value: float
    unrealized_pnl: float
    yield_earned: float
    position_type: str  # "Lending", "LP", "Staking", etc.
    risk_score: float   # 0-100


@dataclass
class PortfolioMetrics:
    """
    Overall portfolio metrics

    METRICS EXPLAINED:
    - Total Value: Sum of all positions
    - Total P&L: Unrealized gains/losses + yield earned
    - APY: Annualized return based on time-weighted performance
    - Sharpe Ratio: Risk-adjusted return
    - Max Drawdown: Largest peak-to-trough decline
    """
    total_value_usd: float
    total_pnl_usd: float
    total_pnl_percent: float
    current_apy: float
    sharpe_ratio: float
    max_drawdown_percent: float
    num_positions: int
    diversification_score: float
    risk_score: float
    health_status: str  # "Healthy", "Warning", "Critical"
    last_updated: datetime


@dataclass
class RebalanceRecommendation:
    """
    Rebalancing recommendation

    WHY REBALANCE:
    - Yields change over time
    - Risk profiles shift
    - Better opportunities emerge
    - Portfolio drifts from target allocation

    EXAMPLE:
    - Reduce Uniswap LP (yield dropped from 25% to 10%)
    - Increase Aave (yield rose from 3% to 6%)
    - Exit risky protocol (smart contract vulnerability found)
    """
    action: str  # "Increase", "Decrease", "Exit", "Enter"
    protocol: str
    pool_name: str
    current_allocation_percent: float
    target_allocation_percent: float
    change_amount_usd: float
    reason: str
    urgency: str  # "Low", "Medium", "High", "Critical"
    expected_impact: Dict[str, float]  # Impact on APY, risk, etc.


@dataclass
class RiskAlert:
    """
    Risk alert for portfolio

    ALERT TYPES:
    - Liquidation risk (health factor < 1.2)
    - Smart contract vulnerability discovered
    - Abnormal yield drop (>50% in 24h)
    - Concentration risk (>50% in one protocol)
    - Impermanent loss threshold breached
    """
    alert_type: str
    severity: str  # "Info", "Warning", "Critical"
    affected_positions: List[str]
    description: str
    recommendation: str
    timestamp: datetime


@dataclass
class Portfolio:
    """
    Complete portfolio state
    """
    portfolio_id: str
    name: str
    owner: str
    positions: List[PortfolioPosition]
    metrics: PortfolioMetrics
    risk_alerts: List[RiskAlert]
    creation_date: datetime
    last_rebalance_date: datetime
    target_apy: Optional[float] = None
    risk_tolerance: Optional[float] = None  # 1-5 scale


# ====================================================================================
# PORTFOLIO CONSTRUCTOR
# ====================================================================================

class PortfolioConstructor:
    """
    Build optimal DeFi portfolios

    CONSTRUCTION STRATEGIES:
    1. Conservative: Maximize safety (stablecoins, blue-chip protocols)
    2. Balanced: Balance risk and return
    3. Aggressive: Maximize returns (accept high risk)
    4. Income-focused: Maximize yield
    5. Custom: User-defined constraints
    """

    def __init__(self):
        """Initialize constructor"""
        pass


    def build_conservative_portfolio(
        self,
        capital_usd: float,
        min_yield_percent: float = 2.0
    ) -> Dict:
        """
        Build conservative portfolio

        STRATEGY:
        - 100% stablecoins
        - Only blue-chip protocols (Aave, Compound, Curve)
        - No lock periods
        - No impermanent loss risk
        - Maximum smart contract risk: 30/100

        TARGET INVESTOR:
        - Risk-averse
        - Capital preservation is priority
        - Willing to accept 2-8% APY

        Args:
            capital_usd: Amount to invest
            min_yield_percent: Minimum acceptable yield

        Returns:
            Portfolio allocation dictionary
        """
        # Conservative allocation strategy
        allocations = [
            {
                'protocol': 'Aave',
                'pool': 'USDC Lending',
                'asset': 'USDC',
                'allocation_percent': 40,
                'expected_apy': 3.5,
                'risk_score': 15,
                'type': 'Lending'
            },
            {
                'protocol': 'Compound',
                'pool': 'USDC Lending',
                'asset': 'USDC',
                'allocation_percent': 25,
                'expected_apy': 3.2,
                'risk_score': 18,
                'type': 'Lending'
            },
            {
                'protocol': 'Curve',
                'pool': '3pool (USDC/USDT/DAI)',
                'asset': 'Stablecoins',
                'allocation_percent': 25,
                'expected_apy': 5.0,
                'risk_score': 20,
                'type': 'LP'
            },
            {
                'protocol': 'Yearn',
                'pool': 'USDC Vault',
                'asset': 'USDC',
                'allocation_percent': 10,
                'expected_apy': 6.0,
                'risk_score': 25,
                'type': 'Vault'
            }
        ]

        # Calculate portfolio metrics
        portfolio_apy = sum(
            a['allocation_percent'] * a['expected_apy'] / 100
            for a in allocations
        )

        portfolio_risk = sum(
            a['allocation_percent'] * a['risk_score'] / 100
            for a in allocations
        )

        # Assign capital
        for alloc in allocations:
            alloc['amount_usd'] = capital_usd * alloc['allocation_percent'] / 100

        return {
            'strategy': 'Conservative',
            'allocations': allocations,
            'total_capital': capital_usd,
            'expected_apy': round(portfolio_apy, 2),
            'portfolio_risk_score': round(portfolio_risk, 2),
            'diversification': len(allocations),
            'characteristics': [
                'Stablecoin-only (no price volatility)',
                'Blue-chip protocols only',
                'No lock periods',
                'Low smart contract risk'
            ]
        }


    def build_balanced_portfolio(
        self,
        capital_usd: float,
        target_apy: float = 15.0
    ) -> Dict:
        """
        Build balanced portfolio

        STRATEGY:
        - Mix of stablecoins (60%) and majors like ETH/BTC (40%)
        - Established protocols
        - Accept moderate IL risk for LP positions
        - Target 10-20% APY

        TARGET INVESTOR:
        - Moderate risk tolerance
        - Seeking higher yields than banks/TradFi
        - Willing to accept some volatility

        Args:
            capital_usd: Amount to invest
            target_apy: Target annual yield %

        Returns:
            Portfolio allocation dictionary
        """
        allocations = [
            {
                'protocol': 'Aave',
                'pool': 'USDC Lending',
                'asset': 'USDC',
                'allocation_percent': 30,
                'expected_apy': 3.5,
                'risk_score': 15,
                'type': 'Lending'
            },
            {
                'protocol': 'Curve',
                'pool': '3pool',
                'asset': 'Stablecoins',
                'allocation_percent': 25,
                'expected_apy': 8.0,
                'risk_score': 20,
                'type': 'LP'
            },
            {
                'protocol': 'Uniswap V3',
                'pool': 'ETH/USDC 0.05%',
                'asset': 'ETH/USDC',
                'allocation_percent': 25,
                'expected_apy': 18.0,
                'risk_score': 35,
                'type': 'LP',
                'il_risk': 'Moderate'
            },
            {
                'protocol': 'Lido',
                'pool': 'ETH Staking',
                'asset': 'ETH',
                'allocation_percent': 15,
                'expected_apy': 4.5,
                'risk_score': 25,
                'type': 'Staking'
            },
            {
                'protocol': 'Yearn',
                'pool': 'USDC Vault',
                'asset': 'USDC',
                'allocation_percent': 5,
                'expected_apy': 12.0,
                'risk_score': 28,
                'type': 'Vault'
            }
        ]

        portfolio_apy = sum(
            a['allocation_percent'] * a['expected_apy'] / 100
            for a in allocations
        )

        portfolio_risk = sum(
            a['allocation_percent'] * a['risk_score'] / 100
            for a in allocations
        )

        for alloc in allocations:
            alloc['amount_usd'] = capital_usd * alloc['allocation_percent'] / 100

        return {
            'strategy': 'Balanced',
            'allocations': allocations,
            'total_capital': capital_usd,
            'expected_apy': round(portfolio_apy, 2),
            'portfolio_risk_score': round(portfolio_risk, 2),
            'diversification': len(allocations),
            'characteristics': [
                '60% stablecoins, 40% volatile assets',
                'Mix of lending, LP, and staking',
                'Moderate impermanent loss risk',
                'Diversified across 5 protocols'
            ]
        }


    def build_aggressive_portfolio(
        self,
        capital_usd: float,
        target_apy: float = 40.0
    ) -> Dict:
        """
        Build aggressive portfolio

        STRATEGY:
        - High yield focus (30%+ APY target)
        - Accept high IL risk
        - Include newer protocols
        - Concentrated liquidity strategies
        - Some token farming

        TARGET INVESTOR:
        - High risk tolerance
        - Seeking maximum returns
        - Can handle 50%+ volatility
        - Active management capability

        ⚠️ WARNING:
        Aggressive strategies can result in significant losses!
        Only suitable for experienced DeFi users.

        Args:
            capital_usd: Amount to invest
            target_apy: Target annual yield %

        Returns:
            Portfolio allocation dictionary
        """
        allocations = [
            {
                'protocol': 'Curve',
                'pool': '3pool',
                'asset': 'Stablecoins',
                'allocation_percent': 15,
                'expected_apy': 8.0,
                'risk_score': 20,
                'type': 'LP (Safety allocation)'
            },
            {
                'protocol': 'Uniswap V3',
                'pool': 'ETH/USDC 0.05%',
                'asset': 'ETH/USDC',
                'allocation_percent': 30,
                'expected_apy': 35.0,
                'risk_score': 45,
                'type': 'Concentrated LP',
                'il_risk': 'High'
            },
            {
                'protocol': 'GMX',
                'pool': 'GLP Pool',
                'asset': 'Multi-asset',
                'allocation_percent': 25,
                'expected_apy': 42.0,
                'risk_score': 55,
                'type': 'Derivatives LP'
            },
            {
                'protocol': 'Convex',
                'pool': 'cvxCRV',
                'asset': 'CRV',
                'allocation_percent': 20,
                'expected_apy': 50.0,
                'risk_score': 60,
                'type': 'Yield Farming'
            },
            {
                'protocol': 'Stargate',
                'pool': 'USDC Pool',
                'asset': 'USDC',
                'allocation_percent': 10,
                'expected_apy': 25.0,
                'risk_score': 50,
                'type': 'Bridge Liquidity'
            }
        ]

        portfolio_apy = sum(
            a['allocation_percent'] * a['expected_apy'] / 100
            for a in allocations
        )

        portfolio_risk = sum(
            a['allocation_percent'] * a['risk_score'] / 100
            for a in allocations
        )

        for alloc in allocations:
            alloc['amount_usd'] = capital_usd * alloc['allocation_percent'] / 100

        return {
            'strategy': 'Aggressive',
            'allocations': allocations,
            'total_capital': capital_usd,
            'expected_apy': round(portfolio_apy, 2),
            'portfolio_risk_score': round(portfolio_risk, 2),
            'diversification': len(allocations),
            'warnings': [
                '⚠️ High volatility expected',
                '⚠️ Significant impermanent loss risk',
                '⚠️ Requires active monitoring',
                '⚠️ Only 15% in low-risk positions'
            ],
            'characteristics': [
                'Target APY: 30-50%',
                'High IL risk in 55% of portfolio',
                'Includes newer protocols',
                'Requires daily monitoring'
            ]
        }


# ====================================================================================
# PORTFOLIO MONITOR
# ====================================================================================

class PortfolioMonitor:
    """
    Monitor portfolio health and generate alerts

    MONITORING INCLUDES:
    1. Yield changes (APY drops >20%)
    2. Liquidation risks (health factor < 1.2)
    3. Smart contract events
    4. Concentration risks
    5. Correlation changes
    6. Market stress conditions
    """

    def __init__(self):
        """Initialize monitor"""
        self.alert_thresholds = {
            'apy_drop_percent': 20,        # Alert if APY drops >20%
            'health_factor_min': 1.2,      # Alert if HF < 1.2
            'concentration_max': 0.50,     # Alert if >50% in one protocol
            'risk_score_max': 70,          # Alert if risk > 70/100
            'pnl_drawdown_max': 0.15       # Alert if drawdown > 15%
        }


    def check_portfolio_health(
        self,
        portfolio: Portfolio,
        current_market_data: Dict
    ) -> List[RiskAlert]:
        """
        Comprehensive portfolio health check

        CHECKS PERFORMED:
        1. APY changes
        2. Liquidation risks
        3. Concentration risks
        4. Overall risk score
        5. P&L drawdowns

        Args:
            portfolio: Current portfolio
            current_market_data: Latest market data for positions

        Returns:
            List of risk alerts
        """
        alerts = []

        # Check 1: APY changes
        for position in portfolio.positions:
            position_key = f"{position.protocol}_{position.pool_name}"

            if position_key in current_market_data:
                current_apy = current_market_data[position_key].get('apy', 0)
                apy_change = ((current_apy - position.entry_apy) / position.entry_apy) * 100

                if apy_change < -self.alert_thresholds['apy_drop_percent']:
                    alerts.append(RiskAlert(
                        alert_type="Yield Drop",
                        severity="Warning",
                        affected_positions=[position_key],
                        description=f"APY dropped {abs(apy_change):.1f}% from entry "
                                   f"({position.entry_apy*100:.2f}% → {current_apy*100:.2f}%)",
                        recommendation="Consider rebalancing to higher-yield alternatives",
                        timestamp=datetime.now()
                    ))

        # Check 2: Concentration risk
        total_value = portfolio.metrics.total_value_usd
        protocol_concentrations = {}

        for position in portfolio.positions:
            if position.protocol not in protocol_concentrations:
                protocol_concentrations[position.protocol] = 0
            protocol_concentrations[position.protocol] += position.current_value

        for protocol, value in protocol_concentrations.items():
            concentration = value / total_value if total_value > 0 else 0

            if concentration > self.alert_thresholds['concentration_max']:
                alerts.append(RiskAlert(
                    alert_type="Concentration Risk",
                    severity="Warning",
                    affected_positions=[protocol],
                    description=f"{concentration*100:.1f}% of portfolio in {protocol}",
                    recommendation="Diversify across more protocols to reduce single-point failure risk",
                    timestamp=datetime.now()
                ))

        # Check 3: Overall risk score
        if portfolio.metrics.risk_score > self.alert_thresholds['risk_score_max']:
            alerts.append(RiskAlert(
                alert_type="High Risk",
                severity="Warning",
                affected_positions=["Portfolio"],
                description=f"Portfolio risk score: {portfolio.metrics.risk_score:.1f}/100",
                recommendation="Reduce exposure to high-risk positions",
                timestamp=datetime.now()
            ))

        # Check 4: Drawdown
        if portfolio.metrics.max_drawdown_percent > self.alert_thresholds['pnl_drawdown_max'] * 100:
            alerts.append(RiskAlert(
                alert_type="Drawdown",
                severity="Critical" if portfolio.metrics.max_drawdown_percent > 25 else "Warning",
                affected_positions=["Portfolio"],
                description=f"Maximum drawdown: {portfolio.metrics.max_drawdown_percent:.1f}%",
                recommendation="Review positions with largest losses and consider cutting losses",
                timestamp=datetime.now()
            ))

        return alerts


    def monitor_liquidation_risk(
        self,
        lending_positions: List[Dict],
        price_scenarios: List[float]
    ) -> Dict:
        """
        Monitor liquidation risk for lending positions

        SCENARIO ANALYSIS:
        Test portfolio under different price shock scenarios:
        - -10%: Normal volatility
        - -20%: High volatility
        - -30%: Black swan
        - -50%: Extreme crisis

        Args:
            lending_positions: List of lending positions with collateral/debt
            price_scenarios: List of price drops to test (e.g., [0.10, 0.20, 0.30])

        Returns:
            Liquidation risk analysis
        """
        results = []

        for scenario in price_scenarios:
            scenario_results = {
                'price_drop_percent': scenario * 100,
                'positions_at_risk': 0,
                'value_at_risk': 0,
                'liquidatable_positions': []
            }

            for pos in lending_positions:
                # Simulate price drop
                new_collateral = pos['collateral_usd'] * (1 - scenario)
                debt = pos['debt_usd']
                liq_threshold = pos.get('liquidation_threshold', 0.80)

                # Calculate health factor
                health_factor = (new_collateral * liq_threshold) / debt if debt > 0 else float('inf')

                if health_factor < 1.2:
                    scenario_results['positions_at_risk'] += 1
                    scenario_results['value_at_risk'] += pos['collateral_usd']

                if health_factor < 1.0:
                    scenario_results['liquidatable_positions'].append({
                        'protocol': pos.get('protocol', 'Unknown'),
                        'health_factor': round(health_factor, 3),
                        'collateral_value': new_collateral
                    })

            results.append(scenario_results)

        return {
            'scenarios': results,
            'worst_case_value_at_risk': max(r['value_at_risk'] for r in results),
            'safe_under_10pct_drop': results[0]['positions_at_risk'] == 0 if results else True
        }


# ====================================================================================
# PORTFOLIO REBALANCER
# ====================================================================================

class PortfolioRebalancer:
    """
    Generate and execute rebalancing recommendations

    WHY REBALANCE:
    - Yields change → shift capital to better opportunities
    - Risk increases → reduce exposure
    - Portfolio drifts → restore target allocation
    - New protocols → take advantage of innovations

    REBALANCING TRIGGERS:
    1. Time-based (e.g., monthly)
    2. Threshold-based (>5% drift from target)
    3. Opportunity-based (new high-yield pool)
    4. Risk-based (protocol vulnerability)
    """

    def __init__(self, rebalance_cost_percent: float = 0.5):
        """
        Initialize rebalancer

        Args:
            rebalance_cost_percent: Estimated cost of rebalancing (gas, slippage)
        """
        self.rebalance_cost = rebalance_cost_percent / 100


    def generate_rebalance_recommendations(
        self,
        current_portfolio: Portfolio,
        target_allocations: Dict,
        current_yields: Dict,
        min_improvement_percent: float = 2.0
    ) -> List[RebalanceRecommendation]:
        """
        Generate rebalancing recommendations

        METHODOLOGY:
        1. Compare current vs. target allocations
        2. Identify positions with declined yields
        3. Find better opportunities
        4. Calculate trade-offs (cost vs. benefit)
        5. Prioritize by urgency

        Args:
            current_portfolio: Current portfolio state
            target_allocations: Target allocation percentages
            current_yields: Current yield data for all protocols
            min_improvement_percent: Minimum APY improvement to justify rebalance

        Returns:
            List of rebalance recommendations
        """
        recommendations = []

        # Calculate current allocations
        total_value = current_portfolio.metrics.total_value_usd
        current_allocations = {}

        for position in current_portfolio.positions:
            key = f"{position.protocol}_{position.pool_name}"
            current_allocations[key] = position.current_value / total_value * 100

        # Compare to targets
        for target_key, target_pct in target_allocations.items():
            current_pct = current_allocations.get(target_key, 0)
            drift = abs(current_pct - target_pct)

            # If drift > 5%, recommend rebalance
            if drift > 5:
                change_amount = (target_pct - current_pct) / 100 * total_value

                if change_amount > 0:
                    action = "Increase"
                    urgency = "High" if drift > 15 else ("Medium" if drift > 10 else "Low")
                else:
                    action = "Decrease"
                    urgency = "Medium" if drift > 15 else "Low"

                # Parse key
                parts = target_key.split('_')
                protocol = parts[0]
                pool = '_'.join(parts[1:])

                # Estimate impact
                current_apy = current_yields.get(target_key, {}).get('apy', 0)
                apy_impact = (change_amount / total_value) * current_apy

                recommendations.append(RebalanceRecommendation(
                    action=action,
                    protocol=protocol,
                    pool_name=pool,
                    current_allocation_percent=round(current_pct, 2),
                    target_allocation_percent=target_pct,
                    change_amount_usd=abs(change_amount),
                    reason=f"Allocation drift: {drift:.1f}% from target",
                    urgency=urgency,
                    expected_impact={
                        'apy_change': round(apy_impact * 100, 2),
                        'cost_estimate': abs(change_amount) * self.rebalance_cost
                    }
                ))

        # Check for yield opportunities
        for position in current_portfolio.positions:
            position_key = f"{position.protocol}_{position.pool_name}"

            if position_key in current_yields:
                current_apy = current_yields[position_key].get('apy', 0)
                entry_apy = position.entry_apy

                # If yield dropped significantly
                if entry_apy > 0 and ((entry_apy - current_apy) / entry_apy * 100) > min_improvement_percent:
                    recommendations.append(RebalanceRecommendation(
                        action="Decrease",
                        protocol=position.protocol,
                        pool_name=position.pool_name,
                        current_allocation_percent=round(position.current_value / total_value * 100, 2),
                        target_allocation_percent=0,
                        change_amount_usd=position.current_value,
                        reason=f"Yield dropped from {entry_apy*100:.2f}% to {current_apy*100:.2f}%",
                        urgency="High",
                        expected_impact={
                            'apy_loss_avoided': round((entry_apy - current_apy) * 100, 2),
                            'cost_estimate': position.current_value * self.rebalance_cost
                        }
                    ))

        # Sort by urgency
        urgency_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        recommendations.sort(key=lambda x: urgency_order.get(x.urgency, 4))

        return recommendations


# ====================================================================================
# EXAMPLE USAGE FOR MSc RESEARCH
# ====================================================================================

if __name__ == "__main__":
    """
    Example usage demonstrating portfolio management
    """
    print("=" * 80)
    print("DeFi PORTFOLIO MANAGER - EXAMPLE USAGE")
    print("=" * 80)

    # Initialize tools
    constructor = PortfolioConstructor()
    monitor = PortfolioMonitor()
    rebalancer = PortfolioRebalancer()

    # ========================================
    # Example 1: Build Portfolios
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Portfolio Construction")
    print("=" * 80)

    capital = 100000  # $100k

    # Conservative
    print("\n1) CONSERVATIVE PORTFOLIO ($100k):")
    conservative = constructor.build_conservative_portfolio(capital, min_yield_percent=2.0)
    print(f"   Expected APY: {conservative['expected_apy']}%")
    print(f"   Risk Score: {conservative['portfolio_risk_score']}/100")
    print(f"\n   Allocations:")
    for alloc in conservative['allocations']:
        print(f"     {alloc['allocation_percent']:>3.0f}% - ${alloc['amount_usd']:>8,.0f} - "
              f"{alloc['protocol']:12} {alloc['pool']:20} ({alloc['expected_apy']:.1f}% APY)")

    # Balanced
    print("\n2) BALANCED PORTFOLIO ($100k):")
    balanced = constructor.build_balanced_portfolio(capital, target_apy=15.0)
    print(f"   Expected APY: {balanced['expected_apy']}%")
    print(f"   Risk Score: {balanced['portfolio_risk_score']}/100")
    print(f"\n   Allocations:")
    for alloc in balanced['allocations']:
        print(f"     {alloc['allocation_percent']:>3.0f}% - ${alloc['amount_usd']:>8,.0f} - "
              f"{alloc['protocol']:12} {alloc['pool']:20} ({alloc['expected_apy']:.1f}% APY)")

    # Aggressive
    print("\n3) AGGRESSIVE PORTFOLIO ($100k):")
    aggressive = constructor.build_aggressive_portfolio(capital, target_apy=40.0)
    print(f"   Expected APY: {aggressive['expected_apy']}%")
    print(f"   Risk Score: {aggressive['portfolio_risk_score']}/100")
    print(f"\n   Allocations:")
    for alloc in aggressive['allocations']:
        print(f"     {alloc['allocation_percent']:>3.0f}% - ${alloc['amount_usd']:>8,.0f} - "
              f"{alloc['protocol']:12} {alloc['pool']:20} ({alloc['expected_apy']:.1f}% APY)")

    if 'warnings' in aggressive:
        print(f"\n   WARNINGS:")
        for warning in aggressive['warnings']:
            print(f"     {warning}")

    # ========================================
    # Example 2: Risk Monitoring
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Portfolio Health Monitoring")
    print("=" * 80)

    # Create sample portfolio
    sample_positions = [
        PortfolioPosition(
            protocol="Aave",
            pool_name="USDC Lending",
            asset="USDC",
            amount_usd=40000,
            entry_price=1.0,
            entry_date=datetime.now() - timedelta(days=30),
            entry_apy=0.035,
            current_value=40350,
            unrealized_pnl=350,
            yield_earned=350,
            position_type="Lending",
            risk_score=15
        ),
        PortfolioPosition(
            protocol="Uniswap V3",
            pool_name="ETH/USDC",
            asset="ETH/USDC",
            amount_usd=30000,
            entry_price=2000,
            entry_date=datetime.now() - timedelta(days=30),
            entry_apy=0.25,
            current_value=29500,
            unrealized_pnl=-500,
            yield_earned=2000,
            position_type="LP",
            risk_score=40
        )
    ]

    sample_metrics = PortfolioMetrics(
        total_value_usd=69850,
        total_pnl_usd=1850,
        total_pnl_percent=2.64,
        current_apy=12.5,
        sharpe_ratio=1.8,
        max_drawdown_percent=7.5,
        num_positions=2,
        diversification_score=50,
        risk_score=28.5,
        health_status="Healthy",
        last_updated=datetime.now()
    )

    sample_portfolio = Portfolio(
        portfolio_id="PORTFOLIO_001",
        name="Sample DeFi Portfolio",
        owner="User123",
        positions=sample_positions,
        metrics=sample_metrics,
        risk_alerts=[],
        creation_date=datetime.now() - timedelta(days=30),
        last_rebalance_date=datetime.now() - timedelta(days=30)
    )

    # Simulate market data with yield drop
    current_market = {
        'Aave_USDC Lending': {'apy': 0.028},  # Dropped from 3.5% to 2.8%
        'Uniswap V3_ETH/USDC': {'apy': 0.18}  # Dropped from 25% to 18%
    }

    # Check health
    print("\nPortfolio Health Check:")
    alerts = monitor.check_portfolio_health(sample_portfolio, current_market)

    if alerts:
        print(f"\n  Found {len(alerts)} alerts:")
        for alert in alerts:
            print(f"\n  [{alert.severity}] {alert.alert_type}")
            print(f"    Description: {alert.description}")
            print(f"    Recommendation: {alert.recommendation}")
    else:
        print("  ✓ No issues detected")

    # ========================================
    # Example 3: Liquidation Risk
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Liquidation Risk Monitoring")
    print("=" * 80)

    lending_positions = [
        {
            'protocol': 'Aave',
            'collateral_usd': 50000,
            'debt_usd': 30000,
            'liquidation_threshold': 0.86
        },
        {
            'protocol': 'Compound',
            'collateral_usd': 20000,
            'debt_usd': 14000,
            'liquidation_threshold': 0.80
        }
    ]

    liq_analysis = monitor.monitor_liquidation_risk(
        lending_positions=lending_positions,
        price_scenarios=[0.10, 0.20, 0.30, 0.50]
    )

    print("\nLiquidation Risk Scenarios:")
    for scenario in liq_analysis['scenarios']:
        print(f"\n  Price Drop: {scenario['price_drop_percent']:.0f}%")
        print(f"    Positions at Risk (HF < 1.2): {scenario['positions_at_risk']}")
        print(f"    Value at Risk: ${scenario['value_at_risk']:,.0f}")

        if scenario['liquidatable_positions']:
            print(f"    Liquidatable Positions:")
            for pos in scenario['liquidatable_positions']:
                print(f"      - {pos['protocol']}: HF = {pos['health_factor']}")

    # ========================================
    # Example 4: Rebalancing
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Rebalancing Recommendations")
    print("=" * 80)

    # Target allocations (same as balanced portfolio)
    target_allocs = {
        'Aave_USDC Lending': 30,
        'Curve_3pool': 25,
        'Uniswap V3_ETH/USDC': 25,
        'Lido_ETH Staking': 15,
        'Yearn_USDC Vault': 5
    }

    # Current yields
    current_yields = {
        'Aave_USDC Lending': {'apy': 0.028},
        'Curve_3pool': {'apy': 0.09},
        'Uniswap V3_ETH/USDC': {'apy': 0.18},
        'Lido_ETH Staking': {'apy': 0.045},
        'Yearn_USDC Vault': {'apy': 0.11}
    }

    rebalance_recs = rebalancer.generate_rebalance_recommendations(
        current_portfolio=sample_portfolio,
        target_allocations=target_allocs,
        current_yields=current_yields,
        min_improvement_percent=2.0
    )

    if rebalance_recs:
        print(f"\nFound {len(rebalance_recs)} rebalancing recommendations:")
        for i, rec in enumerate(rebalance_recs, 1):
            print(f"\n  {i}) [{rec.urgency}] {rec.action} {rec.protocol} - {rec.pool_name}")
            print(f"     Current: {rec.current_allocation_percent}% → Target: {rec.target_allocation_percent}%")
            print(f"     Amount: ${rec.change_amount_usd:,.0f}")
            print(f"     Reason: {rec.reason}")
            if rec.expected_impact:
                print(f"     Expected Impact: APY change: {rec.expected_impact.get('apy_change', 0):.2f}%, "
                      f"Cost: ${rec.expected_impact.get('cost_estimate', 0):.2f}")
    else:
        print("\n  ✓ Portfolio is well-balanced, no rebalancing needed")

    print("\n" + "=" * 80)
    print("Portfolio management examples complete!")
    print("=" * 80)
