"""
=============================================================================
LIQUIDITY ANALYZER FOR DeFi PROTOCOLS
=============================================================================

PURPOSE:
This module analyzes liquidity in Decentralized Finance (DeFi) protocols.
Think of it as your trading desk analyst that tells you:
- How much slippage you'll face when trading
- Where the best liquidity is
- If there are arbitrage opportunities
- How concentrated liquidity is distributed

FOR MSc RESEARCH:
- Study liquidity provision strategies
- Analyze market microstructure in DeFi
- Research price impact and market efficiency
- Compare different AMM (Automated Market Maker) designs

AUTHOR: Built for Economics & Finance MSc students
DATE: 2024
=============================================================================
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import math
from web3 import Web3


# ====================================================================================
# DATA STRUCTURES
# ====================================================================================

@dataclass
class LiquidityMetrics:
    """
    Container for liquidity metrics

    WHAT IT STORES:
    - Pool size (Total Value Locked)
    - Trading volume
    - Liquidity depth at different price levels
    - Slippage estimates
    """
    pool_address: str
    token0: str
    token1: str
    tvl_usd: float
    volume_24h: float
    fee_tier: float  # e.g., 0.003 for 0.3%
    price_current: float
    reserve0: float
    reserve1: float
    liquidity_score: float  # 0-100 rating
    timestamp: datetime


@dataclass
class SlippageResult:
    """
    Results from slippage calculation

    WHY SLIPPAGE MATTERS:
    Large trades move the price against you. This tells you by how much.

    Example: Buying $100k of ETH might cost you 0.5% more than the quoted price
    """
    trade_size_usd: float
    expected_price: float
    execution_price: float
    slippage_percent: float
    price_impact: float
    output_amount: float


@dataclass
class ArbitrageOpportunity:
    """
    Detected arbitrage opportunity between pools

    WHAT IS ARBITRAGE:
    When the same token has different prices on different exchanges,
    you can buy low and sell high for risk-free profit.

    Example: ETH is $2000 on Uniswap but $2010 on SushiSwap → $10 profit per ETH
    """
    token_pair: str
    pool1_name: str
    pool1_address: str
    pool1_price: float
    pool2_name: str
    pool2_address: str
    pool2_price: float
    price_difference_percent: float
    potential_profit_usd: float
    gas_cost_estimate: float
    net_profit: float
    timestamp: datetime


# ====================================================================================
# MAIN LIQUIDITY ANALYZER CLASS
# ====================================================================================

class LiquidityAnalyzer:
    """
    Analyze liquidity in DeFi protocols

    WHAT IT DOES:
    1. Calculate slippage for trades of any size
    2. Analyze liquidity depth (how much you can trade without big price impact)
    3. Score pools based on liquidity quality
    4. Find arbitrage opportunities between pools
    5. Analyze Uniswap V3 concentrated liquidity

    WHY FOR MSc STUDENTS:
    - Research market microstructure in DeFi
    - Study liquidity provision strategies
    - Analyze AMM efficiency vs. traditional order books
    - Model price impact and slippage

    COMMON USE CASES:
    - Before large trades: "How much slippage will I face?"
    - Pool comparison: "Which pool has better liquidity?"
    - Research: "How does liquidity affect price efficiency?"
    """

    def __init__(self, web3_provider: Optional[str] = None):
        """
        Initialize the liquidity analyzer

        Args:
            web3_provider: Ethereum RPC URL (Infura, Alchemy, etc.)
        """
        self.web3 = None
        if web3_provider:
            self.web3 = Web3(Web3.HTTPProvider(web3_provider))

        # Standard fee tiers in basis points (1 bp = 0.01%)
        self.UNISWAP_V3_FEES = {
            100: 0.0001,    # 0.01% - stable pairs
            500: 0.0005,    # 0.05% - common pairs
            3000: 0.003,    # 0.3% - standard
            10000: 0.01     # 1% - exotic pairs
        }


    # ====================================================================================
    # SLIPPAGE CALCULATION
    # ====================================================================================

    def calculate_slippage_constant_product(
        self,
        reserve_in: float,
        reserve_out: float,
        amount_in: float,
        fee: float = 0.003
    ) -> SlippageResult:
        """
        Calculate slippage for Constant Product Market Maker (x * y = k)

        WHAT IS CPMM:
        Uniswap V2, SushiSwap, PancakeSwap use this formula: x * y = k
        - x = reserve of token A
        - y = reserve of token B
        - k = constant

        FORMULA EXPLAINED:
        When you trade, you add tokens to one reserve and remove from the other,
        but x * y must stay constant. This creates a price curve.

        WHY SLIPPAGE HAPPENS:
        Larger trades have bigger impact because they move the reserves more.

        Example:
            ETH/USDC pool: 100 ETH, 200,000 USDC
            Price: 2000 USDC per ETH
            If you buy 10 ETH (10% of pool), price will rise significantly

        Args:
            reserve_in: Reserve of token you're selling (e.g., 200,000 USDC)
            reserve_out: Reserve of token you're buying (e.g., 100 ETH)
            amount_in: Amount you're selling (e.g., 20,000 USDC)
            fee: Pool fee (default 0.3% = 0.003)

        Returns:
            SlippageResult with execution price and slippage %
        """
        # Current price (before trade)
        price_before = reserve_in / reserve_out

        # Apply fee: only (1 - fee) of your input goes to the trade
        amount_in_with_fee = amount_in * (1 - fee)

        # Constant product formula: (x + Δx) * (y - Δy) = x * y
        # Solving for Δy (amount you receive):
        # Δy = (y * Δx) / (x + Δx)
        amount_out = (reserve_out * amount_in_with_fee) / (reserve_in + amount_in_with_fee)

        # Execution price (actual price you paid)
        execution_price = amount_in / amount_out if amount_out > 0 else 0

        # Price after trade
        new_reserve_in = reserve_in + amount_in
        new_reserve_out = reserve_out - amount_out
        price_after = new_reserve_in / new_reserve_out if new_reserve_out > 0 else 0

        # Slippage calculation
        slippage_percent = ((execution_price - price_before) / price_before * 100) if price_before > 0 else 0

        # Price impact (how much the price moved)
        price_impact = ((price_after - price_before) / price_before * 100) if price_before > 0 else 0

        return SlippageResult(
            trade_size_usd=amount_in,
            expected_price=price_before,
            execution_price=execution_price,
            slippage_percent=slippage_percent,
            price_impact=price_impact,
            output_amount=amount_out
        )


    def calculate_slippage_for_multiple_sizes(
        self,
        reserve_in: float,
        reserve_out: float,
        trade_sizes: List[float],
        fee: float = 0.003
    ) -> pd.DataFrame:
        """
        Calculate slippage for multiple trade sizes

        WHY THIS IS USEFUL:
        - Before trading: "What if I trade $10k vs $100k vs $1M?"
        - Research: Study relationship between trade size and price impact
        - Risk management: Know your maximum tradeable size

        Example Output:
        | Trade Size | Slippage % | Price Impact % | Output Amount |
        |------------|------------|----------------|---------------|
        | $1,000     | 0.05%      | 0.05%          | 0.499 ETH     |
        | $10,000    | 0.50%      | 0.52%          | 4.95 ETH      |
        | $100,000   | 5.26%      | 5.88%          | 47.6 ETH      |

        Args:
            reserve_in: Reserve of input token
            reserve_out: Reserve of output token
            trade_sizes: List of trade sizes to test (e.g., [1000, 10000, 100000])
            fee: Pool fee

        Returns:
            DataFrame with slippage analysis for each size
        """
        results = []

        for size in trade_sizes:
            result = self.calculate_slippage_constant_product(
                reserve_in, reserve_out, size, fee
            )

            results.append({
                'trade_size': size,
                'expected_price': result.expected_price,
                'execution_price': result.execution_price,
                'slippage_percent': result.slippage_percent,
                'price_impact_percent': result.price_impact,
                'output_amount': result.output_amount,
                'total_cost': size,
                'cost_per_unit': result.execution_price
            })

        df = pd.DataFrame(results)

        # Add human-readable interpretations
        df['slippage_rating'] = df['slippage_percent'].apply(self._rate_slippage)

        return df


    def _rate_slippage(self, slippage: float) -> str:
        """
        Rate slippage quality

        INDUSTRY STANDARDS:
        - < 0.1%: Excellent (institutional quality)
        - 0.1-0.5%: Good (retail acceptable)
        - 0.5-1%: Moderate (consider splitting trade)
        - 1-3%: High (only if urgent)
        - > 3%: Very High (danger zone, likely to be front-run)
        """
        if slippage < 0.1:
            return "Excellent"
        elif slippage < 0.5:
            return "Good"
        elif slippage < 1.0:
            return "Moderate"
        elif slippage < 3.0:
            return "High"
        else:
            return "Very High"


    # ====================================================================================
    # LIQUIDITY DEPTH ANALYSIS
    # ====================================================================================

    def calculate_liquidity_depth(
        self,
        reserve_in: float,
        reserve_out: float,
        price_levels: List[float],
        fee: float = 0.003
    ) -> pd.DataFrame:
        """
        Calculate liquidity depth at different price levels

        WHAT IS LIQUIDITY DEPTH:
        In traditional markets, the "order book" shows how many orders exist
        at each price level. In AMMs, we calculate the equivalent: how much
        you can trade before reaching a certain price level.

        WHY IT MATTERS:
        - Deep liquidity = can trade large amounts with low slippage
        - Shallow liquidity = even small trades move the price

        Example:
        ETH at $2000, liquidity depth analysis:
        | Price Level | Max Trade Size | Cumulative Depth |
        |-------------|----------------|------------------|
        | $2010       | $50,000        | $50,000          |
        | $2020       | $48,000        | $98,000          |
        | $2050       | $45,000        | $143,000         |

        Args:
            reserve_in: Reserve of input token
            reserve_out: Reserve of output token
            price_levels: List of price increases (e.g., [0.01, 0.02, 0.05] for +1%, +2%, +5%)
            fee: Pool fee

        Returns:
            DataFrame with depth at each price level
        """
        current_price = reserve_in / reserve_out
        results = []
        cumulative_volume = 0

        for price_change in price_levels:
            target_price = current_price * (1 + price_change)

            # Calculate how much needs to be traded to reach this price
            # Using CPMM formula: x * y = k
            k = reserve_in * reserve_out

            # At target price: (x + Δx) / (y - Δy) = target_price
            # And: (x + Δx) * (y - Δy) = k
            # Solving for Δx:
            new_reserve_out = math.sqrt(k / target_price)
            amount_out = reserve_out - new_reserve_out

            # Calculate required input
            new_reserve_in = k / new_reserve_out
            amount_in = new_reserve_in - reserve_in

            # Adjust for fees
            amount_in_with_fee = amount_in / (1 - fee)

            cumulative_volume += amount_in_with_fee

            results.append({
                'price_level': target_price,
                'price_change_percent': price_change * 100,
                'trade_size_required': amount_in_with_fee,
                'cumulative_depth': cumulative_volume,
                'tokens_out': amount_out
            })

        df = pd.DataFrame(results)
        df['depth_quality'] = df['trade_size_required'].apply(
            lambda x: 'Deep' if x > 100000 else ('Moderate' if x > 50000 else 'Shallow')
        )

        return df


    # ====================================================================================
    # POOL QUALITY SCORING
    # ====================================================================================

    def calculate_pool_quality_score(
        self,
        tvl: float,
        volume_24h: float,
        fee_tier: float,
        reserve_ratio: float = 1.0
    ) -> Dict[str, float]:
        """
        Score pool quality from 0-100

        WHAT MAKES A GOOD POOL:
        1. High TVL (Total Value Locked) - more liquidity
        2. High volume relative to TVL - active trading
        3. Balanced reserves - not skewed to one token
        4. Appropriate fee tier - matches volatility

        SCORING COMPONENTS:
        - TVL Score (40%): Higher is better
        - Volume/TVL ratio (30%): Higher means more fee income per $ locked
        - Reserve Balance (20%): Close to 50/50 is ideal
        - Fee Appropriateness (10%): Matches pair characteristics

        Example:
        ETH/USDC pool:
        - TVL: $100M → TVL score: 95/100
        - Daily volume: $80M → Volume ratio: 0.8 → Volume score: 90/100
        - Reserves: 49% ETH, 51% USDC → Balance score: 98/100
        - Fee: 0.05% → Appropriate for stable majors → Fee score: 95/100
        Overall: 93.5/100 (Excellent pool)

        Args:
            tvl: Total Value Locked in USD
            volume_24h: 24-hour trading volume in USD
            fee_tier: Fee percentage (e.g., 0.003 for 0.3%)
            reserve_ratio: Ratio of reserve values (closer to 1.0 is better)

        Returns:
            Dictionary with component scores and overall score
        """
        # Component 1: TVL Score (40% weight)
        # Using logarithmic scale: $1M = 50, $10M = 70, $100M = 90, $1B = 100
        if tvl <= 0:
            tvl_score = 0
        else:
            tvl_score = min(100, 50 + (math.log10(tvl) - 6) * 20)
        tvl_score = max(0, tvl_score)

        # Component 2: Volume/TVL Ratio Score (30% weight)
        # Good pools: 0.3-1.0 (means TVL turns over every 1-3 days)
        # Excellent pools: >1.0 (daily turnover)
        volume_ratio = volume_24h / tvl if tvl > 0 else 0
        if volume_ratio < 0.1:
            volume_score = volume_ratio * 500  # 0-50
        elif volume_ratio < 0.5:
            volume_score = 50 + (volume_ratio - 0.1) * 125  # 50-100
        else:
            volume_score = min(100, 100 + (volume_ratio - 0.5) * 20)  # 100+

        # Component 3: Reserve Balance Score (20% weight)
        # Ideal is 50/50 (ratio = 1.0)
        # Score drops as it deviates from 1.0
        balance_deviation = abs(1.0 - reserve_ratio)
        balance_score = max(0, 100 - (balance_deviation * 200))

        # Component 4: Fee Tier Appropriateness (10% weight)
        # Lower fees for stable/major pairs, higher for exotic
        if fee_tier == 0.0001:  # 0.01% - for stablecoins
            fee_score = 100 if tvl > 10000000 else 80
        elif fee_tier == 0.0005:  # 0.05% - for major pairs
            fee_score = 100
        elif fee_tier == 0.003:  # 0.3% - standard
            fee_score = 90
        elif fee_tier == 0.01:  # 1% - exotic pairs
            fee_score = 70 if tvl < 1000000 else 60
        else:
            fee_score = 50

        # Calculate weighted overall score
        overall_score = (
            tvl_score * 0.4 +
            volume_score * 0.3 +
            balance_score * 0.2 +
            fee_score * 0.1
        )

        return {
            'overall_score': round(overall_score, 2),
            'tvl_score': round(tvl_score, 2),
            'volume_score': round(volume_score, 2),
            'balance_score': round(balance_score, 2),
            'fee_score': round(fee_score, 2),
            'volume_to_tvl_ratio': round(volume_ratio, 4),
            'rating': self._score_to_rating(overall_score)
        }


    def _score_to_rating(self, score: float) -> str:
        """Convert numerical score to letter rating"""
        if score >= 90:
            return "A+ (Excellent)"
        elif score >= 80:
            return "A (Very Good)"
        elif score >= 70:
            return "B (Good)"
        elif score >= 60:
            return "C (Fair)"
        elif score >= 50:
            return "D (Poor)"
        else:
            return "F (Very Poor)"


    # ====================================================================================
    # ARBITRAGE DETECTION
    # ====================================================================================

    def detect_arbitrage_opportunities(
        self,
        pools_data: List[Dict],
        min_profit_percent: float = 0.3,
        gas_cost_estimate: float = 50.0
    ) -> List[ArbitrageOpportunity]:
        """
        Detect arbitrage opportunities between pools

        WHAT IS ARBITRAGE:
        When the same token pair has different prices on different exchanges/pools,
        you can:
        1. Buy on the cheaper exchange
        2. Sell on the more expensive exchange
        3. Profit from the price difference

        WHY IT EXISTS:
        - Temporary price inefficiencies
        - Different pools have different supply/demand
        - High gas costs prevent small arbitrages

        REAL EXAMPLE:
        Block #15000000:
        - Uniswap: ETH = 1,580 USDC
        - SushiSwap: ETH = 1,585 USDC
        - Difference: $5 per ETH (0.316%)
        - Trade 100 ETH → Gross profit: $500
        - Gas cost: $50
        - Net profit: $450

        WHY IMPORTANT FOR RESEARCH:
        - Study market efficiency in DeFi
        - Analyze how quickly arbitrage is corrected
        - Research MEV (Miner Extractable Value)
        - Compare to traditional markets

        Args:
            pools_data: List of pool dictionaries with structure:
                {
                    'name': 'Uniswap V3',
                    'address': '0x...',
                    'token_pair': 'ETH/USDC',
                    'price': 1580.5,
                    'tvl': 50000000
                }
            min_profit_percent: Minimum profit % to report (default 0.3%)
            gas_cost_estimate: Estimated gas cost in USD (default $50)

        Returns:
            List of ArbitrageOpportunity objects sorted by profitability
        """
        opportunities = []

        # Group pools by token pair
        pools_by_pair = {}
        for pool in pools_data:
            pair = pool.get('token_pair', '')
            if pair not in pools_by_pair:
                pools_by_pair[pair] = []
            pools_by_pair[pair].append(pool)

        # Compare prices within each pair
        for pair, pools in pools_by_pair.items():
            if len(pools) < 2:
                continue

            # Sort by price
            pools_sorted = sorted(pools, key=lambda x: x.get('price', 0))

            # Compare lowest price pool with all higher price pools
            for i in range(len(pools_sorted) - 1):
                pool_low = pools_sorted[i]

                for j in range(i + 1, len(pools_sorted)):
                    pool_high = pools_sorted[j]

                    price_low = pool_low.get('price', 0)
                    price_high = pool_high.get('price', 0)

                    if price_low <= 0 or price_high <= 0:
                        continue

                    # Calculate price difference
                    price_diff_percent = ((price_high - price_low) / price_low) * 100

                    # Only consider if above minimum threshold
                    if price_diff_percent < min_profit_percent:
                        continue

                    # Estimate potential profit
                    # Conservative: assume we can trade $10,000 without much slippage
                    trade_size = 10000
                    gross_profit = trade_size * (price_diff_percent / 100)
                    net_profit = gross_profit - gas_cost_estimate

                    if net_profit > 0:
                        opportunity = ArbitrageOpportunity(
                            token_pair=pair,
                            pool1_name=pool_low.get('name', 'Unknown'),
                            pool1_address=pool_low.get('address', ''),
                            pool1_price=price_low,
                            pool2_name=pool_high.get('name', 'Unknown'),
                            pool2_address=pool_high.get('address', ''),
                            pool2_price=price_high,
                            price_difference_percent=price_diff_percent,
                            potential_profit_usd=gross_profit,
                            gas_cost_estimate=gas_cost_estimate,
                            net_profit=net_profit,
                            timestamp=datetime.now()
                        )
                        opportunities.append(opportunity)

        # Sort by net profit (highest first)
        opportunities.sort(key=lambda x: x.net_profit, reverse=True)

        return opportunities


    # ====================================================================================
    # UNISWAP V3 CONCENTRATED LIQUIDITY ANALYSIS
    # ====================================================================================

    def analyze_concentrated_liquidity(
        self,
        current_price: float,
        tick_spacing: int,
        liquidity_positions: List[Dict]
    ) -> Dict:
        """
        Analyze Uniswap V3 concentrated liquidity distribution

        WHAT IS CONCENTRATED LIQUIDITY:
        Uniswap V3 lets liquidity providers (LPs) choose price ranges.
        Instead of providing liquidity across all prices (0 to ∞),
        they can concentrate in a specific range (e.g., ETH $1,800-$2,200).

        WHY IT MATTERS:
        - More capital efficient (up to 4000x compared to V2)
        - LPs earn more fees per dollar
        - But: liquidity can be sparse outside popular ranges

        EXAMPLE:
        ETH/USDC at $2,000:
        - 60% of liquidity is in range $1,900-$2,100
        - 30% in range $1,800-$2,200
        - 10% spread across other prices

        If price moves to $2,150, most liquidity is left behind!

        FOR RESEARCH:
        - Study LP strategies and behavior
        - Analyze efficiency vs. V2
        - Research impact on slippage

        Args:
            current_price: Current market price
            tick_spacing: Tick spacing for the pool (determines granularity)
            liquidity_positions: List of LP positions:
                {
                    'lower_price': 1900,
                    'upper_price': 2100,
                    'liquidity': 1000000
                }

        Returns:
            Dictionary with concentration analysis
        """
        if not liquidity_positions:
            return {
                'total_liquidity': 0,
                'active_liquidity': 0,
                'concentration_ratio': 0,
                'liquidity_at_current_price': 0
            }

        # Calculate total and active liquidity
        total_liquidity = sum(pos.get('liquidity', 0) for pos in liquidity_positions)

        # Active liquidity = liquidity in range at current price
        active_liquidity = sum(
            pos.get('liquidity', 0)
            for pos in liquidity_positions
            if pos.get('lower_price', 0) <= current_price <= pos.get('upper_price', float('inf'))
        )

        # Liquidity distribution by price range
        price_ranges = []
        for pos in liquidity_positions:
            lower = pos.get('lower_price', 0)
            upper = pos.get('upper_price', 0)
            liquidity = pos.get('liquidity', 0)

            # Calculate range width as % of current price
            range_width_percent = ((upper - lower) / current_price) * 100

            price_ranges.append({
                'lower_price': lower,
                'upper_price': upper,
                'liquidity': liquidity,
                'range_width_percent': range_width_percent,
                'is_active': lower <= current_price <= upper
            })

        # Sort by liquidity
        price_ranges.sort(key=lambda x: x['liquidity'], reverse=True)

        # Calculate concentration metrics
        concentration_ratio = (active_liquidity / total_liquidity * 100) if total_liquidity > 0 else 0

        # Find where most liquidity is concentrated
        top_3_ranges = price_ranges[:3]
        top_3_liquidity = sum(r['liquidity'] for r in top_3_ranges)
        top_3_concentration = (top_3_liquidity / total_liquidity * 100) if total_liquidity > 0 else 0

        return {
            'current_price': current_price,
            'total_liquidity': total_liquidity,
            'active_liquidity': active_liquidity,
            'inactive_liquidity': total_liquidity - active_liquidity,
            'concentration_ratio': round(concentration_ratio, 2),
            'top_3_concentration': round(top_3_concentration, 2),
            'num_positions': len(liquidity_positions),
            'active_positions': sum(1 for r in price_ranges if r['is_active']),
            'top_ranges': top_3_ranges,
            'interpretation': self._interpret_concentration(concentration_ratio, top_3_concentration)
        }


    def _interpret_concentration(self, concentration: float, top_3: float) -> str:
        """Interpret concentration metrics"""
        if concentration > 80 and top_3 > 70:
            return "Highly concentrated - excellent liquidity at current price, but risky if price moves"
        elif concentration > 60 and top_3 > 50:
            return "Well concentrated - good liquidity with reasonable range coverage"
        elif concentration > 40:
            return "Moderately concentrated - decent liquidity but somewhat spread out"
        elif concentration > 20:
            return "Low concentration - liquidity is fragmented across many ranges"
        else:
            return "Very low concentration - most liquidity is out of range (warning!)"


# ====================================================================================
# EXAMPLE USAGE FOR MSc STUDENTS
# ====================================================================================

if __name__ == "__main__":
    """
    Example usage demonstrating all major features
    """
    print("=" * 80)
    print("DEFI LIQUIDITY ANALYZER - EXAMPLE USAGE")
    print("=" * 80)

    # Initialize analyzer
    analyzer = LiquidityAnalyzer()

    # ========================================
    # Example 1: Calculate Slippage
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Slippage Analysis for ETH/USDC Pool")
    print("=" * 80)

    # Pool state: 1,000 ETH and 2,000,000 USDC (price = $2,000 per ETH)
    eth_reserve = 1000
    usdc_reserve = 2000000

    # Test different trade sizes
    trade_sizes = [1000, 5000, 10000, 50000, 100000, 500000]

    slippage_df = analyzer.calculate_slippage_for_multiple_sizes(
        reserve_in=usdc_reserve,
        reserve_out=eth_reserve,
        trade_sizes=trade_sizes,
        fee=0.003  # 0.3%
    )

    print("\nSlippage for different trade sizes:")
    print(slippage_df.to_string(index=False))

    # ========================================
    # Example 2: Liquidity Depth
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Liquidity Depth Analysis")
    print("=" * 80)

    # How much can we trade before price moves by 1%, 2%, 5%, 10%?
    price_levels = [0.01, 0.02, 0.05, 0.10, 0.20]

    depth_df = analyzer.calculate_liquidity_depth(
        reserve_in=usdc_reserve,
        reserve_out=eth_reserve,
        price_levels=price_levels,
        fee=0.003
    )

    print("\nLiquidity depth at different price impacts:")
    print(depth_df.to_string(index=False))

    # ========================================
    # Example 3: Pool Quality Score
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Pool Quality Scoring")
    print("=" * 80)

    # Evaluate three different pools
    pools_to_score = [
        {
            'name': 'Major ETH/USDC Pool',
            'tvl': 100000000,      # $100M
            'volume_24h': 80000000,  # $80M
            'fee': 0.0005,          # 0.05%
            'reserve_ratio': 0.98   # Well balanced
        },
        {
            'name': 'Small ETH/USDC Pool',
            'tvl': 5000000,        # $5M
            'volume_24h': 2000000,  # $2M
            'fee': 0.003,           # 0.3%
            'reserve_ratio': 1.05   # Slightly imbalanced
        },
        {
            'name': 'Exotic Token Pool',
            'tvl': 500000,         # $500k
            'volume_24h': 100000,   # $100k
            'fee': 0.01,            # 1%
            'reserve_ratio': 0.75   # Imbalanced
        }
    ]

    print("\nPool Quality Scores:")
    for pool in pools_to_score:
        score = analyzer.calculate_pool_quality_score(
            tvl=pool['tvl'],
            volume_24h=pool['volume_24h'],
            fee_tier=pool['fee'],
            reserve_ratio=pool['reserve_ratio']
        )
        print(f"\n{pool['name']}:")
        print(f"  Overall Score: {score['overall_score']}/100 - {score['rating']}")
        print(f"  TVL Score: {score['tvl_score']}/100")
        print(f"  Volume Score: {score['volume_score']}/100")
        print(f"  Balance Score: {score['balance_score']}/100")
        print(f"  Volume/TVL Ratio: {score['volume_to_tvl_ratio']}")

    # ========================================
    # Example 4: Arbitrage Detection
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Arbitrage Opportunity Detection")
    print("=" * 80)

    # Simulate price data from different pools
    pools_data = [
        {'name': 'Uniswap V3', 'address': '0xabc...', 'token_pair': 'ETH/USDC', 'price': 1998.50, 'tvl': 100000000},
        {'name': 'SushiSwap', 'address': '0xdef...', 'token_pair': 'ETH/USDC', 'price': 2005.25, 'tvl': 50000000},
        {'name': 'Curve', 'address': '0xghi...', 'token_pair': 'ETH/USDC', 'price': 2001.75, 'tvl': 80000000},
        {'name': 'Uniswap V2', 'address': '0xjkl...', 'token_pair': 'WBTC/USDC', 'price': 42150.00, 'tvl': 30000000},
        {'name': 'SushiSwap', 'address': '0xmno...', 'token_pair': 'WBTC/USDC', 'price': 42280.00, 'tvl': 20000000},
    ]

    opportunities = analyzer.detect_arbitrage_opportunities(
        pools_data=pools_data,
        min_profit_percent=0.2,  # 0.2% minimum
        gas_cost_estimate=50.0
    )

    print(f"\nFound {len(opportunities)} arbitrage opportunities:")
    for i, opp in enumerate(opportunities, 1):
        print(f"\n#{i}: {opp.token_pair}")
        print(f"  Buy from: {opp.pool1_name} @ ${opp.pool1_price:,.2f}")
        print(f"  Sell on: {opp.pool2_name} @ ${opp.pool2_price:,.2f}")
        print(f"  Price difference: {opp.price_difference_percent:.3f}%")
        print(f"  Gross profit: ${opp.potential_profit_usd:.2f}")
        print(f"  Gas cost: ${opp.gas_cost_estimate:.2f}")
        print(f"  Net profit: ${opp.net_profit:.2f}")

    # ========================================
    # Example 5: Concentrated Liquidity (V3)
    # ========================================
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Uniswap V3 Concentrated Liquidity Analysis")
    print("=" * 80)

    # Simulate LP positions
    liquidity_positions = [
        {'lower_price': 1900, 'upper_price': 2100, 'liquidity': 5000000},  # Tight range
        {'lower_price': 1850, 'upper_price': 2150, 'liquidity': 3000000},  # Medium range
        {'lower_price': 1800, 'upper_price': 2200, 'liquidity': 2000000},  # Wide range
        {'lower_price': 1950, 'upper_price': 2050, 'liquidity': 4000000},  # Very tight
        {'lower_price': 1700, 'upper_price': 2300, 'liquidity': 1000000},  # Very wide
    ]

    current_price = 2000

    analysis = analyzer.analyze_concentrated_liquidity(
        current_price=current_price,
        tick_spacing=10,
        liquidity_positions=liquidity_positions
    )

    print(f"\nConcentrated Liquidity Analysis at price ${current_price:,.2f}:")
    print(f"  Total Liquidity: ${analysis['total_liquidity']:,.0f}")
    print(f"  Active Liquidity (in range): ${analysis['active_liquidity']:,.0f}")
    print(f"  Inactive Liquidity: ${analysis['inactive_liquidity']:,.0f}")
    print(f"  Concentration Ratio: {analysis['concentration_ratio']}%")
    print(f"  Top 3 Ranges Concentration: {analysis['top_3_concentration']}%")
    print(f"  Number of Positions: {analysis['num_positions']}")
    print(f"  Active Positions: {analysis['active_positions']}")
    print(f"\n  Interpretation: {analysis['interpretation']}")

    print("\n" + "=" * 80)
    print("Analysis complete! Use these techniques for your MSc research.")
    print("=" * 80)
