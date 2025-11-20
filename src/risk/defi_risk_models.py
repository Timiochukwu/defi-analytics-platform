"""
=============================================================================
DeFi RISK ASSESSMENT MODELS
=============================================================================

PURPOSE:
This module provides comprehensive risk assessment for DeFi protocols.
Unlike traditional finance, DeFi has unique risks:
- Smart contract bugs (code vulnerabilities)
- Liquidation cascades (borrowers getting liquidated in chains)
- Protocol dependency risk (one protocol failure affects others)
- Oracle manipulation (price feed attacks)
- Governance attacks (malicious voting)

FOR MSc RESEARCH:
- Study systemic risk in DeFi
- Analyze liquidation mechanics and cascade effects
- Research protocol interconnectedness
- Compare DeFi risk to traditional financial risk

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

class RiskLevel(Enum):
    """Risk level classifications"""
    VERY_LOW = "Very Low"
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    VERY_HIGH = "Very High"
    CRITICAL = "Critical"


class ProtocolType(Enum):
    """Types of DeFi protocols"""
    DEX = "Decentralized Exchange"  # Uniswap, SushiSwap
    LENDING = "Lending Protocol"    # Aave, Compound
    DERIVATIVES = "Derivatives"      # dYdX, GMX
    STABLECOIN = "Stablecoin"       # MakerDAO, Frax
    YIELD = "Yield Aggregator"      # Yearn, Beefy
    BRIDGE = "Bridge"               # Cross-chain bridges


# ====================================================================================
# DATA STRUCTURES
# ====================================================================================

@dataclass
class SmartContractRisk:
    """
    Smart contract risk assessment

    WHY IT MATTERS:
    Code vulnerabilities can lead to total loss. Remember:
    - $600M stolen from Poly Network (2021)
    - $320M from Wormhole Bridge (2022)
    - $100M from Harmony Bridge (2022)
    """
    protocol_name: str
    contract_address: str
    audit_score: float          # 0-100
    code_complexity: float      # 0-100
    time_deployed_days: int
    total_value_at_risk: float
    number_of_audits: int
    has_bug_bounty: bool
    admin_key_risk: float       # 0-100
    upgrade_mechanism: str      # "Immutable", "Timelock", "Multisig", "Single Admin"
    overall_risk_score: float   # 0-100 (higher = more risky)
    risk_level: RiskLevel


@dataclass
class LiquidationRisk:
    """
    Liquidation risk for lending protocols

    WHAT IS LIQUIDATION:
    When you borrow against collateral (e.g., deposit ETH, borrow USDC),
    if your collateral value drops too much, you get liquidated
    (your collateral is seized to repay the loan).

    EXAMPLE:
    - Deposit: 10 ETH at $2,000 = $20,000
    - Borrow: $12,000 USDC (60% LTV - Loan to Value)
    - Liquidation threshold: 80% ($16,000)
    - If ETH drops to $1,600, you get liquidated!
    """
    protocol_name: str
    asset: str
    collateral_value: float
    debt_value: float
    health_factor: float        # > 1 = safe, < 1 = liquidatable
    liquidation_threshold: float  # Price level where liquidation occurs
    current_ltv: float          # Current Loan-to-Value ratio
    max_ltv: float              # Maximum allowed LTV
    distance_to_liquidation_percent: float
    liquidation_penalty: float   # % penalty if liquidated (usually 5-13%)
    risk_level: RiskLevel


@dataclass
class SystemicRisk:
    """
    Systemic risk assessment

    WHAT IS SYSTEMIC RISK:
    Risk that one protocol failure triggers cascade of failures.

    REAL EXAMPLE (May 2022):
    Terra/Luna collapse →
    - 3AC (hedge fund) liquidated
    - Celsius frozen
    - BlockFi near bankruptcy
    - Voyager bankrupt
    Total contagion: >$500B wiped out
    """
    risk_type: str
    protocols_affected: List[str]
    interconnectedness_score: float  # 0-100
    contagion_probability: float     # 0-1
    potential_loss_usd: float
    trigger_events: List[str]
    mitigation_mechanisms: List[str]
    overall_risk_score: float
    risk_level: RiskLevel


# ====================================================================================
# SMART CONTRACT RISK ANALYZER
# ====================================================================================

class SmartContractRiskAnalyzer:
    """
    Analyze smart contract security risks

    RISK FACTORS:
    1. Audit quality - Has it been audited by reputable firms?
    2. Code complexity - More complex = more bugs
    3. Time deployed - Battle-tested > new contracts
    4. Value at risk - Higher TVL = bigger target for hackers
    5. Admin keys - Can admins rug pull?
    6. Upgrade mechanism - Can code be changed maliciously?

    SCORING METHODOLOGY:
    Each factor is scored 0-100, then weighted to get overall risk
    """

    def __init__(self):
        """Initialize the analyzer"""
        # Reputable audit firms (add more as needed)
        self.top_auditors = [
            'Trail of Bits', 'OpenZeppelin', 'ConsenSys Diligence',
            'Quantstamp', 'CertiK', 'PeckShield', 'Halborn'
        ]


    def assess_smart_contract_risk(
        self,
        protocol_name: str,
        contract_address: str,
        auditors: List[str],
        code_lines: int,
        days_deployed: int,
        tvl_usd: float,
        upgrade_mechanism: str = "Unknown",
        has_bug_bounty: bool = False,
        admin_control_level: str = "Unknown"
    ) -> SmartContractRisk:
        """
        Comprehensive smart contract risk assessment

        EXAMPLE USAGE:
        For evaluating if it's safe to invest in a new DeFi protocol

        Args:
            protocol_name: Name of the protocol
            contract_address: Smart contract address
            auditors: List of firms that audited it
            code_lines: Number of lines of code (complexity proxy)
            days_deployed: Days since deployment
            tvl_usd: Total Value Locked
            upgrade_mechanism: How contract can be upgraded
            has_bug_bounty: Whether there's a bug bounty program
            admin_control_level: Level of admin control

        Returns:
            SmartContractRisk assessment
        """
        # Component 1: Audit Score (30% weight)
        audit_score = self._calculate_audit_score(auditors, has_bug_bounty)

        # Component 2: Code Complexity Score (20% weight)
        complexity_score = self._calculate_complexity_score(code_lines)

        # Component 3: Time Battle-Tested Score (20% weight)
        time_score = self._calculate_time_score(days_deployed)

        # Component 4: Value at Risk Score (15% weight)
        # Higher TVL = bigger target but also more scrutinized
        tvl_risk_score = self._calculate_tvl_risk_score(tvl_usd)

        # Component 5: Admin Key Risk (15% weight)
        admin_risk_score = self._calculate_admin_risk_score(
            upgrade_mechanism, admin_control_level
        )

        # Calculate weighted overall risk score
        # Higher score = HIGHER RISK
        overall_risk = (
            (100 - audit_score) * 0.30 +      # Lower audit score = higher risk
            complexity_score * 0.20 +          # Higher complexity = higher risk
            (100 - time_score) * 0.20 +       # Less time = higher risk
            tvl_risk_score * 0.15 +           # Balance of risk/security
            admin_risk_score * 0.15
        )

        # Determine risk level
        risk_level = self._score_to_risk_level(overall_risk)

        return SmartContractRisk(
            protocol_name=protocol_name,
            contract_address=contract_address,
            audit_score=round(audit_score, 2),
            code_complexity=round(complexity_score, 2),
            time_deployed_days=days_deployed,
            total_value_at_risk=tvl_usd,
            number_of_audits=len(auditors),
            has_bug_bounty=has_bug_bounty,
            admin_key_risk=round(admin_risk_score, 2),
            upgrade_mechanism=upgrade_mechanism,
            overall_risk_score=round(overall_risk, 2),
            risk_level=risk_level
        )


    def _calculate_audit_score(self, auditors: List[str], has_bug_bounty: bool) -> float:
        """
        Calculate audit quality score (0-100, higher is better)

        SCORING:
        - No audits: 0
        - 1 audit by unknown firm: 40
        - 1 audit by top firm: 60
        - 2+ audits by top firms: 80-95
        - Bug bounty: +5 to +10 points
        """
        if not auditors:
            base_score = 0
        else:
            # Count top-tier auditors
            top_tier_count = sum(1 for auditor in auditors if auditor in self.top_auditors)
            other_count = len(auditors) - top_tier_count

            # Base score from audits
            base_score = min(95, 30 + (top_tier_count * 25) + (other_count * 15))

        # Bug bounty bonus
        if has_bug_bounty:
            base_score += 10 if base_score < 50 else 5

        return min(100, base_score)


    def _calculate_complexity_score(self, code_lines: int) -> float:
        """
        Calculate complexity risk score (0-100, higher = more complex = riskier)

        BENCHMARKS:
        - < 500 lines: Simple (Low risk)
        - 500-2,000 lines: Moderate
        - 2,000-10,000 lines: Complex
        - > 10,000 lines: Very complex (High risk)
        """
        if code_lines < 500:
            return 20
        elif code_lines < 2000:
            return 40
        elif code_lines < 5000:
            return 60
        elif code_lines < 10000:
            return 80
        else:
            return min(100, 80 + (code_lines - 10000) / 1000)


    def _calculate_time_score(self, days_deployed: int) -> float:
        """
        Calculate battle-tested score (0-100, higher = more battle-tested = safer)

        PHILOSOPHY:
        "Code is not secure until proven secure by time"
        - Lindy Effect: The longer something survives, the longer it will survive

        SCORING:
        - < 30 days: Very new (risky)
        - 30-90 days: New
        - 90-365 days: Established
        - 1-2 years: Well established
        - > 2 years: Battle-tested
        """
        if days_deployed < 30:
            return 10
        elif days_deployed < 90:
            return 30
        elif days_deployed < 180:
            return 50
        elif days_deployed < 365:
            return 70
        elif days_deployed < 730:  # 2 years
            return 85
        else:
            return min(100, 85 + (days_deployed - 730) / 730 * 15)


    def _calculate_tvl_risk_score(self, tvl_usd: float) -> float:
        """
        Calculate TVL-based risk (0-100)

        PARADOX:
        - Low TVL: Less scrutiny, easier to exploit, but smaller loss
        - High TVL: More scrutiny, harder to exploit, but bigger target

        SWEET SPOT: $10M - $500M
        """
        if tvl_usd < 1_000_000:  # < $1M
            return 70  # Too small, not proven
        elif tvl_usd < 10_000_000:  # $1M - $10M
            return 50  # Small but reasonable
        elif tvl_usd < 100_000_000:  # $10M - $100M
            return 30  # Sweet spot
        elif tvl_usd < 500_000_000:  # $100M - $500M
            return 35  # Large, well-tested
        elif tvl_usd < 1_000_000_000:  # $500M - $1B
            return 45  # Major target
        else:  # > $1B
            return 60  # Huge target, "too big to fail" risk


    def _calculate_admin_risk_score(
        self,
        upgrade_mechanism: str,
        admin_control_level: str
    ) -> float:
        """
        Calculate admin/governance risk (0-100, higher = riskier)

        UPGRADE MECHANISMS (from safest to riskiest):
        1. Immutable - Cannot be changed (safest, but no bug fixes!)
        2. Timelock + Multisig - Changes delayed 24-72h, requires multiple signatures
        3. Multisig - Requires multiple signatures (e.g., 5 of 9)
        4. Timelock - Delayed but single admin
        5. DAO Governance - Voting required (can be slow)
        6. Single Admin - One person controls everything (RUG PULL RISK!)

        EXAMPLE RUG PULL:
        AnubisDAO (2021): Single admin key, $60M stolen immediately after launch
        """
        # Upgrade mechanism risk
        upgrade_risk = {
            'Immutable': 10,
            'Timelock + Multisig': 15,
            'Timelock Multisig': 15,
            'Multisig': 25,
            'DAO Governance': 30,
            'DAO': 30,
            'Timelock': 50,
            'Single Admin': 95,
            'Admin': 90,
            'Unknown': 70
        }.get(upgrade_mechanism, 70)

        # Admin control level risk
        control_risk = {
            'None': 0,
            'Very Low': 10,
            'Low': 25,
            'Moderate': 50,
            'High': 75,
            'Very High': 95,
            'Unknown': 60
        }.get(admin_control_level, 60)

        # Return average
        return (upgrade_risk + control_risk) / 2


    def _score_to_risk_level(self, score: float) -> RiskLevel:
        """Convert numerical risk score to risk level"""
        if score < 20:
            return RiskLevel.VERY_LOW
        elif score < 40:
            return RiskLevel.LOW
        elif score < 60:
            return RiskLevel.MODERATE
        elif score < 75:
            return RiskLevel.HIGH
        elif score < 90:
            return RiskLevel.VERY_HIGH
        else:
            return RiskLevel.CRITICAL


# ====================================================================================
# LIQUIDATION RISK ANALYZER
# ====================================================================================

class LiquidationRiskAnalyzer:
    """
    Analyze liquidation risk for lending protocols

    WHAT IS LIQUIDATION:
    In DeFi lending (Aave, Compound, etc.), you can:
    1. Deposit collateral (e.g., ETH)
    2. Borrow against it (e.g., USDC)

    If your collateral value drops, you get liquidated:
    - Your collateral is seized
    - Sold to repay the loan
    - You pay a liquidation penalty (5-13%)

    WHY IT MATTERS:
    - Individual: Losing money to liquidation
    - Systemic: Liquidation cascades can crash markets

    FAMOUS EXAMPLE:
    Black Thursday (March 12, 2020):
    - ETH crashed 50% in hours
    - $8M in bad debt on MakerDAO
    - Network congestion prevented liquidations
    - Protocol nearly failed
    """

    def __init__(self):
        """Initialize the analyzer"""
        # Standard liquidation parameters by protocol
        self.protocol_params = {
            'Aave': {
                'ETH': {'max_ltv': 0.825, 'liq_threshold': 0.86, 'liq_penalty': 0.05},
                'WBTC': {'max_ltv': 0.70, 'liq_threshold': 0.75, 'liq_penalty': 0.10},
                'USDC': {'max_ltv': 0.80, 'liq_threshold': 0.85, 'liq_penalty': 0.05},
            },
            'Compound': {
                'ETH': {'max_ltv': 0.75, 'liq_threshold': 0.80, 'liq_penalty': 0.08},
                'WBTC': {'max_ltv': 0.65, 'liq_threshold': 0.70, 'liq_penalty': 0.08},
                'USDC': {'max_ltv': 0.75, 'liq_threshold': 0.80, 'liq_penalty': 0.08},
            }
        }


    def assess_liquidation_risk(
        self,
        protocol_name: str,
        asset: str,
        collateral_value_usd: float,
        debt_value_usd: float,
        liquidation_threshold: Optional[float] = None,
        liquidation_penalty: Optional[float] = None
    ) -> LiquidationRisk:
        """
        Assess liquidation risk for a lending position

        HEALTH FACTOR EXPLAINED:
        Health Factor = (Collateral * Liquidation Threshold) / Debt

        - HF > 1.5: Safe
        - HF = 1.2-1.5: Moderate risk
        - HF = 1.0-1.2: High risk
        - HF < 1.0: Liquidatable!

        EXAMPLE:
        - Collateral: $20,000 ETH
        - Debt: $12,000 USDC
        - Liquidation Threshold: 86%
        - HF = ($20,000 * 0.86) / $12,000 = 1.43 (moderate risk)

        Args:
            protocol_name: Protocol name (e.g., "Aave", "Compound")
            asset: Collateral asset (e.g., "ETH", "WBTC")
            collateral_value_usd: Current collateral value in USD
            debt_value_usd: Current debt value in USD
            liquidation_threshold: Optional custom threshold (default: from protocol)
            liquidation_penalty: Optional custom penalty (default: from protocol)

        Returns:
            LiquidationRisk assessment

        Raises:
            ValueError: If inputs are invalid
        """
        # Input validation
        if collateral_value_usd < 0:
            raise ValueError(f"collateral_value_usd must be non-negative, got {collateral_value_usd}")
        if debt_value_usd < 0:
            raise ValueError(f"debt_value_usd must be non-negative, got {debt_value_usd}")
        if liquidation_threshold is not None and (liquidation_threshold <= 0 or liquidation_threshold > 1):
            raise ValueError(f"liquidation_threshold must be between 0 and 1, got {liquidation_threshold}")
        if liquidation_penalty is not None and (liquidation_penalty < 0 or liquidation_penalty > 1):
            raise ValueError(f"liquidation_penalty must be between 0 and 1, got {liquidation_penalty}")

        # Get protocol parameters
        if liquidation_threshold is None or liquidation_penalty is None:
            params = self._get_protocol_params(protocol_name, asset)
            if liquidation_threshold is None:
                liquidation_threshold = params['liq_threshold']
            if liquidation_penalty is None:
                liquidation_penalty = params['liq_penalty']
            max_ltv = params['max_ltv']
        else:
            max_ltv = liquidation_threshold * 0.95  # Estimate

        # Calculate current LTV
        current_ltv = debt_value_usd / collateral_value_usd if collateral_value_usd > 0 else 0

        # Calculate Health Factor
        health_factor = (
            (collateral_value_usd * liquidation_threshold) / debt_value_usd
            if debt_value_usd > 0 else float('inf')
        )

        # Calculate liquidation price
        # Price must drop by this much to trigger liquidation
        if health_factor != float('inf'):
            distance_to_liquidation = ((health_factor - 1.0) / health_factor) * 100
        else:
            distance_to_liquidation = 100.0

        # Determine risk level
        risk_level = self._health_factor_to_risk_level(health_factor)

        return LiquidationRisk(
            protocol_name=protocol_name,
            asset=asset,
            collateral_value=collateral_value_usd,
            debt_value=debt_value_usd,
            health_factor=round(health_factor, 3),
            liquidation_threshold=liquidation_threshold,
            current_ltv=round(current_ltv, 4),
            max_ltv=max_ltv,
            distance_to_liquidation_percent=round(distance_to_liquidation, 2),
            liquidation_penalty=liquidation_penalty,
            risk_level=risk_level
        )


    def simulate_price_drop_scenarios(
        self,
        initial_collateral_usd: float,
        debt_usd: float,
        liquidation_threshold: float,
        price_drops: List[float]
    ) -> pd.DataFrame:
        """
        Simulate liquidation risk under various price drop scenarios

        WHY SIMULATE:
        - Risk management: "What if ETH drops 30%?"
        - Research: Study liquidation probability distributions
        - Stress testing: Find breaking points

        REAL USE CASE:
        Before taking a leveraged position, see how much price drop you can handle

        Args:
            initial_collateral_usd: Initial collateral value
            debt_usd: Debt amount
            liquidation_threshold: Liquidation threshold (e.g., 0.86 for 86%)
            price_drops: List of price drop percentages (e.g., [0.05, 0.10, 0.20, 0.30])

        Returns:
            DataFrame with scenarios
        """
        scenarios = []

        for drop in price_drops:
            # New collateral value after price drop
            new_collateral = initial_collateral_usd * (1 - drop)

            # New health factor
            health_factor = (
                (new_collateral * liquidation_threshold) / debt_usd
                if debt_usd > 0 else float('inf')
            )

            # Is it liquidatable?
            is_liquidatable = health_factor < 1.0

            # Loss if liquidated
            if is_liquidatable:
                liquidation_value = debt_usd / liquidation_threshold
                remaining_collateral = new_collateral - liquidation_value
                loss = initial_collateral_usd - remaining_collateral
                loss_percent = (loss / initial_collateral_usd) * 100
            else:
                loss = 0
                loss_percent = 0

            scenarios.append({
                'price_drop_percent': drop * 100,
                'collateral_value': new_collateral,
                'health_factor': round(health_factor, 3),
                'is_liquidatable': is_liquidatable,
                'loss_if_liquidated': round(loss, 2),
                'loss_percent': round(loss_percent, 2),
                'risk_level': self._health_factor_to_risk_level(health_factor).value
            })

        return pd.DataFrame(scenarios)


    def calculate_cascade_probability(
        self,
        positions: List[Dict],
        price_shock: float
    ) -> Dict:
        """
        Calculate probability of liquidation cascade

        WHAT IS A CASCADE:
        1. Price drops → some positions liquidated
        2. Liquidations sell collateral → price drops more
        3. More liquidations triggered → more selling
        4. Death spiral!

        REAL EXAMPLE:
        Black Thursday (March 12, 2020):
        ETH: $195 → $90 in 24 hours
        Liquidations cascaded, nearly broke MakerDAO

        Args:
            positions: List of position dictionaries:
                {
                    'collateral_usd': 100000,
                    'debt_usd': 60000,
                    'liq_threshold': 0.86,
                    'collateral_amount': 50.0  # in tokens
                }
            price_shock: Initial price drop (e.g., 0.20 for 20%)

        Returns:
            Cascade analysis dictionary
        """
        total_collateral = sum(p['collateral_usd'] for p in positions)
        current_price_drop = price_shock
        cascade_rounds = []
        max_rounds = 10  # Prevent infinite loops

        for round_num in range(max_rounds):
            # Calculate which positions get liquidated this round
            liquidated_this_round = []
            total_sell_pressure = 0

            for pos in positions:
                if pos.get('liquidated', False):
                    continue  # Already liquidated

                # Collateral value after price drop
                current_collateral = pos['collateral_usd'] * (1 - current_price_drop)

                # Health factor
                hf = (current_collateral * pos['liq_threshold']) / pos['debt_usd']

                if hf < 1.0:
                    # This position gets liquidated!
                    pos['liquidated'] = True
                    liquidated_this_round.append(pos)
                    # Selling pressure from liquidation
                    total_sell_pressure += current_collateral

            # If no new liquidations, cascade stops
            if not liquidated_this_round:
                break

            # Estimate additional price impact from selling
            # Simplified: selling 1% of total collateral causes 0.5% additional drop
            additional_drop = (total_sell_pressure / total_collateral) * 0.5
            current_price_drop += additional_drop

            cascade_rounds.append({
                'round': round_num + 1,
                'cumulative_price_drop': round(current_price_drop * 100, 2),
                'positions_liquidated': len(liquidated_this_round),
                'value_liquidated': round(total_sell_pressure, 2),
                'additional_price_impact': round(additional_drop * 100, 2)
            })

        # Summary statistics
        total_liquidated = sum(1 for p in positions if p.get('liquidated', False))
        total_value_liquidated = sum(
            p['collateral_usd'] for p in positions if p.get('liquidated', False)
        )

        return {
            'initial_price_shock': price_shock * 100,
            'final_price_drop': round(current_price_drop * 100, 2),
            'cascade_occurred': len(cascade_rounds) > 1,
            'cascade_rounds': cascade_rounds,
            'total_positions': len(positions),
            'positions_liquidated': total_liquidated,
            'liquidation_rate': round((total_liquidated / len(positions)) * 100, 2),
            'total_value_liquidated': round(total_value_liquidated, 2),
            'amplification_factor': round(current_price_drop / price_shock, 2) if price_shock > 0 else 0
        }


    def _get_protocol_params(self, protocol: str, asset: str) -> Dict:
        """Get protocol-specific parameters"""
        if protocol in self.protocol_params and asset in self.protocol_params[protocol]:
            return self.protocol_params[protocol][asset]
        else:
            # Default conservative parameters
            return {
                'max_ltv': 0.70,
                'liq_threshold': 0.75,
                'liq_penalty': 0.10
            }


    def _health_factor_to_risk_level(self, health_factor: float) -> RiskLevel:
        """Convert health factor to risk level"""
        if health_factor >= 2.0:
            return RiskLevel.VERY_LOW
        elif health_factor >= 1.5:
            return RiskLevel.LOW
        elif health_factor >= 1.2:
            return RiskLevel.MODERATE
        elif health_factor >= 1.05:
            return RiskLevel.HIGH
        elif health_factor >= 1.0:
            return RiskLevel.VERY_HIGH
        else:
            return RiskLevel.CRITICAL


# ====================================================================================
# SYSTEMIC RISK ANALYZER
# ====================================================================================

class SystemicRiskAnalyzer:
    """
    Analyze systemic risk and protocol interconnectedness

    WHAT IS SYSTEMIC RISK:
    Risk that affects the entire DeFi ecosystem, not just one protocol

    TYPES:
    1. Contagion Risk - One failure spreads to others
    2. Correlation Risk - All protocols move together
    3. Liquidity Risk - Market-wide liquidity crisis
    4. Oracle Risk - Price feed manipulation affects all
    5. Regulatory Risk - Government action affecting entire space

    FOR RESEARCH:
    - Study network effects in DeFi
    - Analyze protocol dependencies
    - Model contagion pathways
    - Compare to traditional systemic risk (2008 crisis)
    """

    def __init__(self):
        """Initialize the analyzer"""
        pass


    def assess_protocol_interconnectedness(
        self,
        protocol_connections: List[Dict]
    ) -> Dict:
        """
        Assess how interconnected protocols are

        EXAMPLE CONNECTIONS:
        - Yearn uses Curve for swaps
        - Curve uses Aave for lending
        - Aave uses Chainlink oracles
        - If Chainlink fails → Aave fails → Curve affected → Yearn affected

        This creates a dependency chain!

        Args:
            protocol_connections: List of connections:
                {
                    'from_protocol': 'Yearn',
                    'to_protocol': 'Curve',
                    'connection_type': 'Liquidity Provider',
                    'value_at_risk': 50000000
                }

        Returns:
            Interconnectedness analysis
        """
        # Build dependency graph
        protocols = set()
        dependencies = {}
        reverse_dependencies = {}  # Who depends on this protocol
        total_connections = len(protocol_connections)

        for conn in protocol_connections:
            from_p = conn['from_protocol']
            to_p = conn['to_protocol']

            protocols.add(from_p)
            protocols.add(to_p)

            # Track dependencies
            if from_p not in dependencies:
                dependencies[from_p] = []
            dependencies[from_p].append({
                'protocol': to_p,
                'type': conn.get('connection_type', 'Unknown'),
                'value': conn.get('value_at_risk', 0)
            })

            # Track reverse dependencies (who needs me?)
            if to_p not in reverse_dependencies:
                reverse_dependencies[to_p] = []
            reverse_dependencies[to_p].append(from_p)

        # Find most critical protocols (most dependents)
        protocol_criticality = {}
        for protocol in protocols:
            num_dependents = len(reverse_dependencies.get(protocol, []))
            num_dependencies = len(dependencies.get(protocol, []))

            # Criticality score: higher if many depend on it
            criticality = (num_dependents * 2 + num_dependencies)
            protocol_criticality[protocol] = {
                'num_dependents': num_dependents,
                'num_dependencies': num_dependencies,
                'criticality_score': criticality
            }

        # Sort by criticality
        sorted_protocols = sorted(
            protocol_criticality.items(),
            key=lambda x: x[1]['criticality_score'],
            reverse=True
        )

        # Calculate overall interconnectedness
        # More connections relative to protocols = higher interconnectedness
        num_protocols = len(protocols)
        max_possible_connections = num_protocols * (num_protocols - 1)
        interconnectedness_ratio = total_connections / max_possible_connections if max_possible_connections > 0 else 0

        # Interconnectedness score (0-100)
        interconnectedness_score = min(100, interconnectedness_ratio * 1000)

        # Risk level
        if interconnectedness_score < 20:
            risk_level = RiskLevel.VERY_LOW
        elif interconnectedness_score < 40:
            risk_level = RiskLevel.LOW
        elif interconnectedness_score < 60:
            risk_level = RiskLevel.MODERATE
        elif interconnectedness_score < 80:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.VERY_HIGH

        return {
            'num_protocols': num_protocols,
            'total_connections': total_connections,
            'interconnectedness_score': round(interconnectedness_score, 2),
            'risk_level': risk_level.value,
            'most_critical_protocols': sorted_protocols[:5],
            'interpretation': self._interpret_interconnectedness(interconnectedness_score)
        }


    def simulate_contagion(
        self,
        initial_failure: str,
        protocol_connections: List[Dict],
        failure_threshold: float = 0.30
    ) -> Dict:
        """
        Simulate contagion from one protocol failure

        SIMULATION LOGIC:
        1. Protocol A fails
        2. All protocols with >30% exposure to A are at risk
        3. Some of those fail
        4. Repeat until no new failures

        REAL EXAMPLE:
        Terra/Luna collapse (May 2022):
        - Luna fails
        - 3AC (30% in Luna) → fails
        - Celsius (loaned to 3AC) → fails
        - Voyager (loaned to 3AC) → fails
        Contagion spread to 10+ protocols!

        Args:
            initial_failure: Protocol that fails first
            protocol_connections: List of connections (same format as above)
            failure_threshold: % exposure that causes failure (default 30%)

        Returns:
            Contagion simulation results
        """
        failed_protocols = {initial_failure}
        newly_failed = {initial_failure}
        contagion_rounds = []

        # Calculate each protocol's exposure
        protocol_exposures = {}
        for conn in protocol_connections:
            from_p = conn['from_protocol']
            to_p = conn['to_protocol']
            value = conn.get('value_at_risk', 0)

            if from_p not in protocol_exposures:
                protocol_exposures[from_p] = {'total': 0, 'exposures': {}}

            protocol_exposures[from_p]['exposures'][to_p] = value
            protocol_exposures[from_p]['total'] += value

        # Simulate contagion rounds
        round_num = 0
        max_rounds = 10

        while newly_failed and round_num < max_rounds:
            round_num += 1
            next_wave_failures = set()

            # Check all protocols for exposure to newly failed
            for protocol, data in protocol_exposures.items():
                if protocol in failed_protocols:
                    continue  # Already failed

                # Calculate exposure to failed protocols
                exposure_to_failed = sum(
                    data['exposures'].get(failed_p, 0)
                    for failed_p in newly_failed
                )

                # Calculate exposure ratio
                exposure_ratio = exposure_to_failed / data['total'] if data['total'] > 0 else 0

                # Does this protocol fail?
                if exposure_ratio >= failure_threshold:
                    next_wave_failures.add(protocol)

            contagion_rounds.append({
                'round': round_num,
                'newly_failed': list(newly_failed),
                'next_wave': list(next_wave_failures),
                'cumulative_failures': len(failed_protocols) + len(next_wave_failures)
            })

            # Update for next round
            failed_protocols.update(next_wave_failures)
            newly_failed = next_wave_failures

        return {
            'initial_failure': initial_failure,
            'total_failures': len(failed_protocols),
            'failure_list': list(failed_protocols),
            'contagion_rounds': contagion_rounds,
            'contagion_occurred': len(failed_protocols) > 1,
            'severity': 'Critical' if len(failed_protocols) > 5 else ('High' if len(failed_protocols) > 3 else 'Moderate')
        }


    def _interpret_interconnectedness(self, score: float) -> str:
        """Interpret interconnectedness score"""
        if score < 20:
            return "Low interconnectedness - protocols are relatively isolated"
        elif score < 40:
            return "Moderate interconnectedness - some dependencies exist"
        elif score < 60:
            return "High interconnectedness - significant cross-protocol dependencies"
        elif score < 80:
            return "Very high interconnectedness - systemic risk is elevated"
        else:
            return "Extreme interconnectedness - one failure could cascade widely"


# ====================================================================================
# EXAMPLE USAGE FOR MSc RESEARCH
# ====================================================================================

if __name__ == "__main__":
    """
    Example usage demonstrating all risk assessment capabilities
    """
    print("=" * 80)
    print("DeFi RISK ASSESSMENT - EXAMPLE USAGE")
    print("=" * 80)

    # Initialize analyzers
    sc_analyzer = SmartContractRiskAnalyzer()
    liq_analyzer = LiquidationRiskAnalyzer()
    sys_analyzer = SystemicRiskAnalyzer()

    # ========================================
    # Example 1: Smart Contract Risk
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Smart Contract Risk Assessment")
    print("=" * 80)

    # Assess a few protocols
    protocols_to_assess = [
        {
            'name': 'Established Protocol (Aave)',
            'address': '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9',
            'auditors': ['Trail of Bits', 'OpenZeppelin', 'ConsenSys Diligence'],
            'code_lines': 15000,
            'days_deployed': 900,
            'tvl': 5_000_000_000,
            'upgrade': 'Timelock + Multisig',
            'bug_bounty': True,
            'admin_control': 'Low'
        },
        {
            'name': 'New Protocol (Risky)',
            'address': '0x1234567890abcdef',
            'auditors': [],
            'code_lines': 8000,
            'days_deployed': 15,
            'tvl': 2_000_000,
            'upgrade': 'Single Admin',
            'bug_bounty': False,
            'admin_control': 'Very High'
        }
    ]

    print("\nSmart Contract Risk Assessments:\n")
    for protocol in protocols_to_assess:
        risk = sc_analyzer.assess_smart_contract_risk(
            protocol_name=protocol['name'],
            contract_address=protocol['address'],
            auditors=protocol['auditors'],
            code_lines=protocol['code_lines'],
            days_deployed=protocol['days_deployed'],
            tvl_usd=protocol['tvl'],
            upgrade_mechanism=protocol['upgrade'],
            has_bug_bounty=protocol['bug_bounty'],
            admin_control_level=protocol['admin_control']
        )

        print(f"{risk.protocol_name}:")
        print(f"  Overall Risk Score: {risk.overall_risk_score}/100 ({risk.risk_level.value})")
        print(f"  Audit Score: {risk.audit_score}/100")
        print(f"  Code Complexity: {risk.code_complexity}/100")
        print(f"  Days Deployed: {risk.time_deployed_days}")
        print(f"  TVL at Risk: ${risk.total_value_at_risk:,.0f}")
        print(f"  Number of Audits: {risk.number_of_audits}")
        print(f"  Admin Risk: {risk.admin_key_risk}/100")
        print()

    # ========================================
    # Example 2: Liquidation Risk
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Liquidation Risk Assessment")
    print("=" * 80)

    # Assess a lending position
    position_risk = liq_analyzer.assess_liquidation_risk(
        protocol_name='Aave',
        asset='ETH',
        collateral_value_usd=100000,  # $100k ETH collateral
        debt_value_usd=60000         # $60k USDC debt
    )

    print(f"\nLending Position Risk:")
    print(f"  Protocol: {position_risk.protocol_name}")
    print(f"  Collateral: ${position_risk.collateral_value:,.0f} {position_risk.asset}")
    print(f"  Debt: ${position_risk.debt_value:,.0f}")
    print(f"  Health Factor: {position_risk.health_factor}")
    print(f"  Current LTV: {position_risk.current_ltv * 100:.2f}%")
    print(f"  Max LTV: {position_risk.max_ltv * 100:.2f}%")
    print(f"  Distance to Liquidation: {position_risk.distance_to_liquidation_percent:.2f}%")
    print(f"  Liquidation Penalty: {position_risk.liquidation_penalty * 100:.1f}%")
    print(f"  Risk Level: {position_risk.risk_level.value}")

    # Simulate price drop scenarios
    print("\n\nPrice Drop Scenarios:")
    scenarios = liq_analyzer.simulate_price_drop_scenarios(
        initial_collateral_usd=100000,
        debt_usd=60000,
        liquidation_threshold=0.86,
        price_drops=[0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    )
    print(scenarios.to_string(index=False))

    # ========================================
    # Example 3: Liquidation Cascade
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Liquidation Cascade Simulation")
    print("=" * 80)

    # Simulate multiple positions
    positions = [
        {'collateral_usd': 1000000, 'debt_usd': 700000, 'liq_threshold': 0.86, 'collateral_amount': 500},
        {'collateral_usd': 500000, 'debt_usd': 350000, 'liq_threshold': 0.86, 'collateral_amount': 250},
        {'collateral_usd': 2000000, 'debt_usd': 1500000, 'liq_threshold': 0.86, 'collateral_amount': 1000},
        {'collateral_usd': 750000, 'debt_usd': 500000, 'liq_threshold': 0.86, 'collateral_amount': 375},
        {'collateral_usd': 300000, 'debt_usd': 200000, 'liq_threshold': 0.86, 'collateral_amount': 150},
    ]

    cascade = liq_analyzer.calculate_cascade_probability(
        positions=positions,
        price_shock=0.15  # 15% initial drop
    )

    print(f"\nLiquidation Cascade Analysis:")
    print(f"  Initial Price Shock: {cascade['initial_price_shock']:.1f}%")
    print(f"  Final Price Drop: {cascade['final_price_drop']:.1f}%")
    print(f"  Cascade Occurred: {cascade['cascade_occurred']}")
    print(f"  Total Positions: {cascade['total_positions']}")
    print(f"  Positions Liquidated: {cascade['positions_liquidated']}")
    print(f"  Liquidation Rate: {cascade['liquidation_rate']:.1f}%")
    print(f"  Total Value Liquidated: ${cascade['total_value_liquidated']:,.0f}")
    print(f"  Amplification Factor: {cascade['amplification_factor']:.2f}x")

    if cascade['cascade_rounds']:
        print("\n  Cascade Rounds:")
        for round_data in cascade['cascade_rounds']:
            print(f"    Round {round_data['round']}: {round_data['positions_liquidated']} positions, "
                  f"${round_data['value_liquidated']:,.0f} liquidated, "
                  f"{round_data['cumulative_price_drop']:.2f}% cumulative drop")

    # ========================================
    # Example 4: Systemic Risk
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Systemic Risk & Interconnectedness")
    print("=" * 80)

    # Define protocol connections
    connections = [
        {'from_protocol': 'Yearn', 'to_protocol': 'Curve', 'connection_type': 'Liquidity', 'value_at_risk': 50000000},
        {'from_protocol': 'Yearn', 'to_protocol': 'Aave', 'connection_type': 'Lending', 'value_at_risk': 30000000},
        {'from_protocol': 'Curve', 'to_protocol': 'Aave', 'connection_type': 'Lending', 'value_at_risk': 40000000},
        {'from_protocol': 'Curve', 'to_protocol': 'Chainlink', 'connection_type': 'Oracle', 'value_at_risk': 100000000},
        {'from_protocol': 'Aave', 'to_protocol': 'Chainlink', 'connection_type': 'Oracle', 'value_at_risk': 5000000000},
        {'from_protocol': 'Compound', 'to_protocol': 'Chainlink', 'connection_type': 'Oracle', 'value_at_risk': 3000000000},
        {'from_protocol': 'MakerDAO', 'to_protocol': 'Chainlink', 'connection_type': 'Oracle', 'value_at_risk': 8000000000},
        {'from_protocol': 'Synthetix', 'to_protocol': 'Chainlink', 'connection_type': 'Oracle', 'value_at_risk': 500000000},
    ]

    interconnectedness = sys_analyzer.assess_protocol_interconnectedness(connections)

    print(f"\nProtocol Interconnectedness Analysis:")
    print(f"  Number of Protocols: {interconnectedness['num_protocols']}")
    print(f"  Total Connections: {interconnectedness['total_connections']}")
    print(f"  Interconnectedness Score: {interconnectedness['interconnectedness_score']}/100")
    print(f"  Risk Level: {interconnectedness['risk_level']}")
    print(f"  Interpretation: {interconnectedness['interpretation']}")

    print("\n  Most Critical Protocols:")
    for protocol, data in interconnectedness['most_critical_protocols']:
        print(f"    {protocol}: {data['num_dependents']} dependents, "
              f"{data['num_dependencies']} dependencies, "
              f"criticality score: {data['criticality_score']}")

    # ========================================
    # Example 5: Contagion Simulation
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Contagion Simulation")
    print("=" * 80)

    # Simulate Chainlink failure (oracles are critical!)
    contagion = sys_analyzer.simulate_contagion(
        initial_failure='Chainlink',
        protocol_connections=connections,
        failure_threshold=0.30
    )

    print(f"\nContagion Simulation (Initial Failure: {contagion['initial_failure']}):")
    print(f"  Total Failures: {contagion['total_failures']}")
    print(f"  Contagion Occurred: {contagion['contagion_occurred']}")
    print(f"  Severity: {contagion['severity']}")
    print(f"  Failed Protocols: {', '.join(contagion['failure_list'])}")

    if contagion['contagion_rounds']:
        print("\n  Contagion Progression:")
        for round_data in contagion['contagion_rounds']:
            print(f"    Round {round_data['round']}: "
                  f"Newly Failed: {', '.join(round_data['newly_failed']) if round_data['newly_failed'] else 'None'}")

    print("\n" + "=" * 80)
    print("Risk assessment complete! Use these tools for your MSc research.")
    print("=" * 80)
