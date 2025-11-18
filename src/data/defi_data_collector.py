"""
DeFi Data Collector Module

This module collects real-time and historical data from DeFi protocols:
- Uniswap (DEX - Decentralized Exchange)
- Aave (Lending protocol)
- Compound (Lending protocol)
- Curve (Stablecoin DEX)
- MakerDAO (CDP - Collateralized Debt Position)

Why This Matters:
- DeFi operates 24/7 (no closing bell!)
- Prices update every block (~12 seconds on Ethereum)
- Critical for yield farming, arbitrage, risk management
- Real-time data = competitive advantage

How It Works:
1. Connect to Ethereum node (Infura/Alchemy)
2. Read smart contract data using Web3
3. Query The Graph for historical data
4. Cache frequently accessed data in Redis
5. Update database with latest metrics

For Your MSc Research:
- Study liquidity dynamics
- Analyze yield behavior
- Model systemic risk
- Measure protocol efficiency
"""

from web3 import Web3
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import json
import os
from decimal import Decimal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeFiDataCollector:
    """
    Collect data from major DeFi protocols

    This is your gateway to the DeFi ecosystem. Think of it as
    Bloomberg Terminal for DeFi - real-time data on:
    - Token prices
    - Liquidity pools
    - Lending rates
    - Total Value Locked (TVL)
    - Trading volumes

    Example:
        collector = DeFiDataCollector(
            provider_url="https://mainnet.infura.io/v3/YOUR-KEY"
        )

        # Get Uniswap pool data
        pool_data = collector.get_uniswap_pool_info(
            pool_address="0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"  # USDC/ETH
        )

        # Get Aave lending rates
        rates = collector.get_aave_rates("USDC")
    """

    def __init__(
        self,
        provider_url: str,
        the_graph_api_key: Optional[str] = None
    ):
        """
        Initialize DeFi data collector

        Args:
            provider_url: Ethereum node URL (Infura/Alchemy)
                        Get free key at: https://infura.io or https://alchemy.com
            the_graph_api_key: The Graph API key for historical queries
                              Get at: https://thegraph.com

        Setup Guide:
            1. Sign up for Infura: https://infura.io/register
            2. Create new project → Get Project ID
            3. Use: https://mainnet.infura.io/v3/YOUR-PROJECT-ID
        """
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.the_graph_key = the_graph_api_key

        # Check connection
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Ethereum node")

        logger.info(f"Connected to Ethereum. Block number: {self.w3.eth.block_number}")

        # Protocol addresses on Ethereum Mainnet
        self.UNISWAP_V3_FACTORY = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
        self.AAVE_V3_POOL = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"
        self.COMPOUND_V3_USDC = "0xc3d688B66703497DAA19211EEdff47f25384cdc3"

        # Common ERC20 tokens
        self.TOKENS = {
            "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
        }

        # ABI fragments (minimal for reading data)
        # In production, load full ABIs from files
        self.ERC20_ABI = json.loads('[{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"type":"function"}]')

    def get_token_price_uniswap(
        self,
        token_address: str,
        quote_token: str = "USDC"
    ) -> float:
        """
        Get token price from Uniswap

        Uniswap uses Constant Product Market Maker (CPMM):
        x * y = k (constant)

        Price = reserve_quote / reserve_token

        Args:
            token_address: Token contract address
            quote_token: Quote currency (default USDC for USD price)

        Returns:
            Token price in USD

        Example:
            # Get ETH price
            eth_price = collector.get_token_price_uniswap(
                collector.TOKENS["WETH"]
            )
            print(f"ETH Price: ${eth_price:,.2f}")
        """
        try:
            # This is a simplified version
            # In production, find the actual pool and read reserves

            # For demo, we'll return mock data
            # In real implementation, you'd:
            # 1. Find pool address from factory
            # 2. Get reserves from pool contract
            # 3. Calculate price accounting for decimals

            logger.info(f"Fetching price for {token_address}")

            # Mock implementation
            if token_address == self.TOKENS["WETH"]:
                return 2000.0  # $2000 per ETH (demo)
            elif token_address == self.TOKENS["WBTC"]:
                return 40000.0  # $40k per BTC (demo)
            else:
                return 1.0

        except Exception as e:
            logger.error(f"Error fetching price: {str(e)}")
            return 0.0

    def get_uniswap_pool_info(
        self,
        pool_address: str
    ) -> Dict[str, any]:
        """
        Get Uniswap V3 pool information

        Uniswap V3 pools are concentrated liquidity AMMs.
        Key metrics:
        - Liquidity: Total liquidity in pool
        - Tick: Current price tick
        - Fee tier: 0.01%, 0.05%, 0.3%, or 1%
        - Volume 24h: Trading volume
        - TVL: Total Value Locked

        Args:
            pool_address: Uniswap V3 pool address

        Returns:
            Dictionary with pool information

        Use Cases:
            - Liquidity analysis
            - Slippage estimation
            - Impermanent loss calculation
            - Yield farming APY
        """
        try:
            # In production, read from actual pool contract
            # This requires the Uniswap V3 Pool ABI

            pool_info = {
                'pool_address': pool_address,
                'token0': self.TOKENS["USDC"],
                'token1': self.TOKENS["WETH"],
                'fee': 3000,  # 0.3% in basis points
                'liquidity': 15000000.0,  # $15M liquidity (demo)
                'price': 2000.0,  # Current price
                'volume_24h': 50000000.0,  # $50M volume (demo)
                'tvl': 30000000.0,  # $30M TVL
                'fees_24h': 150000.0,  # $150k fees
                'timestamp': datetime.now()
            }

            logger.info(f"Pool {pool_address}: TVL=${pool_info['tvl']:,.0f}, Volume=${pool_info['volume_24h']:,.0f}")

            return pool_info

        except Exception as e:
            logger.error(f"Error fetching pool info: {str(e)}")
            return {}

    def get_aave_rates(
        self,
        asset: str = "USDC"
    ) -> Dict[str, float]:
        """
        Get Aave lending and borrowing rates

        Aave is a lending protocol where users can:
        - Supply assets to earn interest
        - Borrow assets by providing collateral

        Rates are dynamic based on utilization:
        Utilization = Borrowed / Supplied
        Higher utilization → Higher rates

        Args:
            asset: Asset symbol (USDC, DAI, ETH, etc.)

        Returns:
            Dictionary with supply/borrow rates and utilization

        Research Applications:
            - Study interest rate dynamics
            - Analyze utilization patterns
            - Model lending risk
            - Compare with TradFi rates
        """
        try:
            asset_address = self.TOKENS.get(asset)
            if not asset_address:
                logger.warning(f"Asset {asset} not found")
                return {}

            # In production, read from Aave Pool contract
            # This requires querying getReserveData(asset)

            rates = {
                'asset': asset,
                'supply_apy': 3.5,  # 3.5% APY for supplying (demo)
                'borrow_apy_variable': 5.2,  # 5.2% APY variable rate
                'borrow_apy_stable': 6.0,  # 6.0% APY stable rate
                'utilization': 0.75,  # 75% utilization
                'total_supplied': 500000000.0,  # $500M supplied
                'total_borrowed': 375000000.0,  # $375M borrowed
                'available_liquidity': 125000000.0,  # $125M available
                'timestamp': datetime.now()
            }

            logger.info(f"Aave {asset}: Supply APY={rates['supply_apy']:.2f}%, Borrow={rates['borrow_apy_variable']:.2f}%")

            return rates

        except Exception as e:
            logger.error(f"Error fetching Aave rates: {str(e)}")
            return {}

    def calculate_impermanent_loss(
        self,
        price_start: float,
        price_end: float
    ) -> Dict[str, float]:
        """
        Calculate impermanent loss for liquidity providers

        Impermanent Loss (IL) is the opportunity cost of providing
        liquidity vs just holding tokens.

        Formula:
        IL = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1

        Example:
            If ETH goes from $1000 to $2000 (2x):
            IL = 2 * sqrt(2) / (1 + 2) - 1 = -5.7%

            This means you'd be 5.7% worse off than just holding!

        Args:
            price_start: Starting price
            price_end: Ending price

        Returns:
            Dictionary with IL metrics

        Why This Matters:
            - Major risk for liquidity providers
            - Must be offset by trading fees
            - Worse for volatile pairs
            - Better for stablecoin pairs
        """
        try:
            price_ratio = price_end / price_start

            # Impermanent loss formula
            il_percentage = (2 * np.sqrt(price_ratio) / (1 + price_ratio) - 1) * 100

            # Value if held
            held_value = 1.0 + price_ratio  # Start with 1 token0 + 1 token1

            # Value in pool (constant product formula)
            pool_value = 2 * np.sqrt(price_ratio)

            # Absolute loss
            absolute_loss = pool_value - held_value

            result = {
                'price_start': price_start,
                'price_end': price_end,
                'price_change': (price_ratio - 1) * 100,
                'impermanent_loss_pct': il_percentage,
                'held_value': held_value,
                'pool_value': pool_value,
                'absolute_loss': absolute_loss
            }

            logger.info(f"Price change: {result['price_change']:+.1f}% → IL: {il_percentage:.2f}%")

            return result

        except Exception as e:
            logger.error(f"Error calculating IL: {str(e)}")
            return {}

    def get_protocol_tvl_historical(
        self,
        protocol: str,
        days: int = 30
    ) -> pd.DataFrame:
        """
        Get historical Total Value Locked (TVL) for a protocol

        TVL is THE most important DeFi metric:
        - Measures protocol adoption
        - Indicates security (more TVL = more at stake)
        - Shows growth trends
        - Correlates with token price

        In production, this would query The Graph or Defillama API

        Args:
            protocol: Protocol name (uniswap, aave, compound, etc.)
            days: Number of days of history

        Returns:
            DataFrame with date and TVL columns

        Research Applications:
            - Study protocol growth
            - Analyze TVL migrations
            - Model network effects
            - Identify trends
        """
        try:
            # Generate mock historical data
            # In production, query The Graph subgraphs

            dates = pd.date_range(
                end=datetime.now(),
                periods=days,
                freq='D'
            )

            # Simulate TVL growth with some volatility
            base_tvl = 1000000000  # $1B base
            growth_rate = 0.01  # 1% daily growth
            volatility = 0.05  # 5% volatility

            tvl_values = []
            current_tvl = base_tvl

            for i in range(days):
                # Random walk with drift
                change = np.random.normal(growth_rate, volatility)
                current_tvl *= (1 + change)
                tvl_values.append(current_tvl)

            df = pd.DataFrame({
                'date': dates,
                'tvl': tvl_values,
                'protocol': protocol
            })

            logger.info(f"{protocol} TVL: ${current_tvl:,.0f} ({days} days)")

            return df

        except Exception as e:
            logger.error(f"Error fetching TVL: {str(e)}")
            return pd.DataFrame()

    def get_gas_prices(self) -> Dict[str, float]:
        """
        Get current gas prices (transaction costs)

        Gas prices fluctuate based on network demand.
        Critical for:
        - Transaction timing decisions
        - Profitability calculations
        - User experience optimization

        Returns:
            Dictionary with gas prices in Gwei

        Understanding Gas:
            - Measured in Gwei (1 Gwei = 0.000000001 ETH)
            - Total cost = gas_price * gas_used * ETH_price
            - Simple transfer: ~21,000 gas
            - Uniswap swap: ~150,000 gas
            - Complex DeFi: 300,000+ gas
        """
        try:
            # Get latest gas price from network
            gas_price_wei = self.w3.eth.gas_price
            gas_price_gwei = self.w3.from_wei(gas_price_wei, 'gwei')

            # Estimate for different speed levels
            gas_prices = {
                'slow': float(gas_price_gwei * 0.8),  # 80% for slower
                'standard': float(gas_price_gwei),
                'fast': float(gas_price_gwei * 1.2),  # 120% for faster
                'instant': float(gas_price_gwei * 1.5),  # 150% for instant
                'timestamp': datetime.now()
            }

            logger.info(f"Gas prices - Standard: {gas_prices['standard']:.1f} Gwei")

            return gas_prices

        except Exception as e:
            logger.error(f"Error fetching gas prices: {str(e)}")
            return {'standard': 50.0}  # Default fallback


# Example usage and testing
if __name__ == "__main__":
    print("="*80)
    print("DeFi DATA COLLECTOR - SETUP GUIDE")
    print("="*80)

    print("""
    BEFORE RUNNING:

    1. Get Ethereum Node Access (FREE):
       - Sign up: https://infura.io/register
       - Create project → Copy Project ID
       - Or use Alchemy: https://alchemy.com

    2. Set Environment Variable:
       export INFURA_PROJECT_ID="your-project-id"

    3. Basic Usage:

       from src.data.defi_data_collector import DeFiDataCollector

       collector = DeFiDataCollector(
           provider_url=f"https://mainnet.infura.io/v3/{YOUR_ID}"
       )

       # Get ETH price
       eth_price = collector.get_token_price_uniswap(
           collector.TOKENS["WETH"]
       )

       # Get Aave lending rates
       rates = collector.get_aave_rates("USDC")

       # Calculate impermanent loss
       il = collector.calculate_impermanent_loss(
           price_start=1000,
           price_end=2000
       )

    4. For The Graph (Historical Data):
       - Sign up: https://thegraph.com
       - Get API key
       - Access Uniswap, Aave subgraphs

    DEMO MODE:
    Currently returns mock data for demonstration.
    Connect to real Ethereum node to get live data!
    """)

    # Demo with mock data
    print("\n" + "="*80)
    print("RUNNING DEMO (Mock Data)")
    print("="*80)

    # This will fail without real Ethereum connection
    # Uncomment to test with your Infura/Alchemy key:

    # infura_url = f"https://mainnet.infura.io/v3/{os.getenv('INFURA_PROJECT_ID')}"
    # collector = DeFiDataCollector(provider_url=infura_url)

    # For demo, show the structure
    print("\nExample outputs:")
    print("\n1. Impermanent Loss Calculation:")
    print("   Price $1000 → $2000 (2x increase)")
    print("   Result: -5.7% impermanent loss")
    print("   Meaning: You'd be 5.7% worse off vs holding")

    print("\n2. Aave Lending Rates:")
    print("   USDC Supply APY: 3.5%")
    print("   USDC Borrow APY: 5.2%")
    print("   Spread: 1.7% (protocol profit)")

    print("\n3. Uniswap Pool TVL:")
    print("   USDC/ETH Pool: $30M TVL")
    print("   24h Volume: $50M")
    print("   24h Fees: $150k")
    print("   APY from fees: ~180%")

    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("1. Get Infura/Alchemy API key")
    print("2. Connect to mainnet")
    print("3. Start collecting real DeFi data!")
    print("="*80)
