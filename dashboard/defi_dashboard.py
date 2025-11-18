"""
=============================================================================
DeFi ANALYTICS PLATFORM - STREAMLIT DASHBOARD
=============================================================================

PURPOSE:
Interactive web dashboard for DeFi analytics featuring:
- Portfolio builder and monitor
- Yield opportunity explorer
- Risk assessment tools
- Liquidity analysis
- Real-time metrics

FOR MSc RESEARCH:
- Visualize DeFi data
- Test portfolio strategies
- Analyze risk-return tradeoffs
- Compare protocols

AUTHOR: Built for Economics & Finance MSc students
DATE: 2024

USAGE:
    streamlit run defi_dashboard.py
=============================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# ====================================================================================
# PAGE CONFIGURATION
# ====================================================================================

st.set_page_config(
    page_title="DeFi Analytics Platform",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ====================================================================================
# HELPER FUNCTIONS
# ====================================================================================

def create_portfolio_pie_chart(allocations):
    """Create portfolio allocation pie chart"""
    labels = [f"{a['protocol']}\n{a['pool']}" for a in allocations]
    values = [a['percent'] for a in allocations]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        textinfo='label+percent',
        textposition='auto'
    )])

    fig.update_layout(
        title="Portfolio Allocation",
        height=400,
        showlegend=True
    )

    return fig


def create_apy_comparison_chart(opportunities):
    """Create APY comparison bar chart"""
    df = pd.DataFrame(opportunities)

    fig = px.bar(
        df,
        x='protocol',
        y='apy',
        color='risk_rating',
        title='APY by Protocol',
        labels={'apy': 'APY (%)', 'protocol': 'Protocol'},
        color_discrete_map={
            'Very Low': '#28a745',
            'Low': '#5cb85c',
            'Moderate': '#ffc107',
            'High': '#fd7e14',
            'Very High': '#dc3545'
        }
    )

    fig.update_layout(height=400)

    return fig


def create_risk_return_scatter(opportunities):
    """Create risk-return scatter plot"""
    df = pd.DataFrame(opportunities)

    fig = px.scatter(
        df,
        x='risk_level',
        y='apy',
        size='tvl_millions',
        color='protocol',
        hover_data=['pool', 'asset'],
        title='Risk-Return Profile',
        labels={'apy': 'APY (%)', 'risk_level': 'Risk Level (1-5)'}
    )

    fig.update_layout(height=400)

    return fig


def format_currency(amount):
    """Format number as currency"""
    return f"${amount:,.2f}"


def format_percent(value):
    """Format number as percentage"""
    return f"{value:.2f}%"


# ====================================================================================
# SIDEBAR
# ====================================================================================

with st.sidebar:
    st.image("https://via.placeholder.com/200x80/1f77b4/ffffff?text=DeFi+Analytics", use_column_width=True)

    st.markdown("### 📊 Navigation")

    page = st.radio(
        "Select Page",
        ["🏠 Overview", "💼 Portfolio Builder", "📈 Yield Explorer", "⚠️ Risk Assessment", "💧 Liquidity Analysis"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### ⚙️ Settings")

    show_demo_data = st.checkbox("Use Demo Data", value=True)

    st.markdown("---")
    st.markdown("""
    ### 📚 Resources
    - [Documentation](#)
    - [API Reference](#)
    - [GitHub](#)

    ### 💡 For MSc Students
    Built for Economics & Finance research
    """)


# ====================================================================================
# PAGE: OVERVIEW
# ====================================================================================

if "Overview" in page:
    st.markdown('<div class="main-header">💰 DeFi Analytics Platform</div>', unsafe_allow_html=True)

    st.markdown("""
    ### Welcome to DeFi Analytics Platform

    A comprehensive platform for DeFi portfolio management, yield optimization, and risk assessment.

    **Key Features:**
    - 📊 **Portfolio Builder**: Construct optimal DeFi portfolios
    - 💰 **Yield Optimizer**: Find best yields across protocols
    - ⚠️ **Risk Assessment**: Analyze smart contract and liquidation risks
    - 💧 **Liquidity Analysis**: Calculate slippage and pool quality
    """)

    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Protocols", "15+", "+3")

    with col2:
        st.metric("Avg APY", "12.5%", "+2.3%")

    with col3:
        st.metric("Total TVL", "$50B", "+5%")

    with col4:
        st.metric("Active Users", "10k+", "+15%")

    st.markdown("---")

    # Market Overview
    st.markdown("### 📊 Market Overview")

    col1, col2 = st.columns(2)

    with col1:
        # Top protocols by TVL
        protocols_data = pd.DataFrame({
            'Protocol': ['Aave', 'Uniswap', 'Curve', 'MakerDAO', 'Compound'],
            'TVL_Billions': [12.5, 8.3, 6.2, 5.8, 4.1],
            'APY': [3.5, 18.2, 8.0, 2.8, 3.2]
        })

        fig = px.bar(
            protocols_data,
            x='Protocol',
            y='TVL_Billions',
            title='Top Protocols by TVL',
            labels={'TVL_Billions': 'TVL ($ Billions)'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Yield opportunities
        yield_data = pd.DataFrame({
            'Category': ['Lending', 'LP (Stable)', 'LP (Volatile)', 'Staking', 'Farming'],
            'Avg_APY': [3.5, 7.5, 22.0, 4.5, 35.0],
            'Risk': [1, 2, 3, 2, 4]
        })

        fig = px.scatter(
            yield_data,
            x='Risk',
            y='Avg_APY',
            size='Avg_APY',
            color='Category',
            title='Yield Opportunities by Risk',
            labels={'Avg_APY': 'Average APY (%)', 'Risk': 'Risk Level (1-5)'}
        )
        st.plotly_chart(fig, use_container_width=True)


# ====================================================================================
# PAGE: PORTFOLIO BUILDER
# ====================================================================================

elif "Portfolio Builder" in page:
    st.markdown('<div class="main-header">💼 Portfolio Builder</div>', unsafe_allow_html=True)

    st.markdown("### Build Your Optimal DeFi Portfolio")

    # Input Parameters
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("#### Investment Parameters")

        capital = st.number_input(
            "Capital to Invest ($)",
            min_value=1000,
            max_value=10000000,
            value=100000,
            step=1000
        )

        strategy = st.selectbox(
            "Investment Strategy",
            ["Conservative", "Balanced", "Aggressive"]
        )

        if strategy == "Conservative":
            st.info("**Conservative**: Stablecoins only, blue-chip protocols, 2-8% APY, minimal risk")
        elif strategy == "Balanced":
            st.info("**Balanced**: Mix of stable and volatile, 10-20% APY, moderate risk")
        else:
            st.warning("**Aggressive**: High yield focus, 30-50% APY, high risk ⚠️")

        if st.button("🚀 Build Portfolio", type="primary"):
            st.session_state.portfolio_built = True

    with col2:
        if st.session_state.get('portfolio_built', False):
            # Generate portfolio based on strategy
            if strategy == "Conservative":
                allocations = [
                    {"protocol": "Aave", "pool": "USDC", "percent": 40, "apy": 3.5, "risk": 15},
                    {"protocol": "Compound", "pool": "USDC", "percent": 25, "apy": 3.2, "risk": 18},
                    {"protocol": "Curve", "pool": "3pool", "percent": 25, "apy": 5.0, "risk": 20},
                    {"protocol": "Yearn", "pool": "USDC Vault", "percent": 10, "apy": 6.0, "risk": 25}
                ]
                expected_apy = 4.1
                risk_score = 18.5

            elif strategy == "Balanced":
                allocations = [
                    {"protocol": "Aave", "pool": "USDC", "percent": 30, "apy": 3.5, "risk": 15},
                    {"protocol": "Curve", "pool": "3pool", "percent": 25, "apy": 8.0, "risk": 20},
                    {"protocol": "Uniswap V3", "pool": "ETH/USDC", "percent": 25, "apy": 18.0, "risk": 35},
                    {"protocol": "Lido", "pool": "ETH Staking", "percent": 15, "apy": 4.5, "risk": 25},
                    {"protocol": "Yearn", "pool": "USDC Vault", "percent": 5, "apy": 12.0, "risk": 28}
                ]
                expected_apy = 9.5
                risk_score = 28.5

            else:  # Aggressive
                allocations = [
                    {"protocol": "Curve", "pool": "3pool", "percent": 15, "apy": 8.0, "risk": 20},
                    {"protocol": "Uniswap V3", "pool": "ETH/USDC", "percent": 30, "apy": 35.0, "risk": 45},
                    {"protocol": "GMX", "pool": "GLP", "percent": 25, "apy": 42.0, "risk": 55},
                    {"protocol": "Convex", "pool": "cvxCRV", "percent": 20, "apy": 50.0, "risk": 60},
                    {"protocol": "Stargate", "pool": "USDC", "percent": 10, "apy": 25.0, "risk": 50}
                ]
                expected_apy = 35.7
                risk_score = 48.5

            # Add amounts
            for alloc in allocations:
                alloc['amount'] = capital * alloc['percent'] / 100

            # Display Results
            st.markdown("#### Portfolio Summary")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Expected APY", f"{expected_apy}%")
            with col2:
                st.metric("Risk Score", f"{risk_score}/100")
            with col3:
                st.metric("Positions", len(allocations))

            # Pie chart
            st.plotly_chart(create_portfolio_pie_chart(allocations), use_container_width=True)

            # Detailed allocation table
            st.markdown("#### Detailed Allocations")

            df = pd.DataFrame(allocations)
            df['Amount'] = df['amount'].apply(format_currency)
            df['APY'] = df['apy'].apply(lambda x: f"{x}%")
            df['Allocation'] = df['percent'].apply(lambda x: f"{x}%")

            st.dataframe(
                df[['protocol', 'pool', 'Allocation', 'Amount', 'APY', 'risk']].rename(columns={
                    'protocol': 'Protocol',
                    'pool': 'Pool',
                    'risk': 'Risk Score'
                }),
                use_container_width=True,
                hide_index=True
            )

            # Expected returns
            st.markdown("#### Expected Returns")

            time_periods = [30, 90, 180, 365]
            returns = []

            for days in time_periods:
                expected_return = capital * (expected_apy / 100) * (days / 365)
                returns.append({
                    'Period': f"{days} days",
                    'Expected_Return': expected_return,
                    'Total_Value': capital + expected_return,
                    'APY': expected_apy
                })

            returns_df = pd.DataFrame(returns)
            returns_df['Expected Return'] = returns_df['Expected_Return'].apply(format_currency)
            returns_df['Total Value'] = returns_df['Total_Value'].apply(format_currency)

            st.dataframe(returns_df[['Period', 'Expected Return', 'Total Value']], use_container_width=True, hide_index=True)


# ====================================================================================
# PAGE: YIELD EXPLORER
# ====================================================================================

elif "Yield Explorer" in page:
    st.markdown('<div class="main-header">📈 Yield Explorer</div>', unsafe_allow_html=True)

    st.markdown("### Discover Best Yield Opportunities")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        min_apy = st.slider("Minimum APY (%)", 0.0, 100.0, 5.0, 1.0)

    with col2:
        max_risk = st.select_slider("Max Risk Level", options=[1, 2, 3, 4, 5], value=3)

    with col3:
        min_tvl = st.selectbox("Min TVL", ["$1M", "$10M", "$100M", "$1B"], index=1)

    # Sample opportunities
    opportunities = [
        {"protocol": "Aave", "pool": "USDC Lending", "asset": "USDC", "apy": 3.5, "tvl_millions": 2000, "risk_level": 1, "risk_rating": "Very Low", "yield_type": "Lending"},
        {"protocol": "Compound", "pool": "USDC Lending", "asset": "USDC", "apy": 3.2, "tvl_millions": 1800, "risk_level": 1, "risk_rating": "Very Low", "yield_type": "Lending"},
        {"protocol": "Curve", "pool": "3pool", "asset": "Stablecoins", "apy": 8.0, "tvl_millions": 1500, "risk_level": 2, "risk_rating": "Low", "yield_type": "LP"},
        {"protocol": "Uniswap V3", "pool": "ETH/USDC", "asset": "ETH/USDC", "apy": 25.0, "tvl_millions": 800, "risk_level": 3, "risk_rating": "Moderate", "yield_type": "LP"},
        {"protocol": "Lido", "pool": "ETH Staking", "asset": "ETH", "apy": 4.5, "tvl_millions": 3000, "risk_level": 2, "risk_rating": "Low", "yield_type": "Staking"},
        {"protocol": "GMX", "pool": "GLP", "asset": "Multi-asset", "apy": 42.0, "tvl_millions": 500, "risk_level": 4, "risk_rating": "High", "yield_type": "Derivatives"},
        {"protocol": "Convex", "pool": "cvxCRV", "asset": "CRV", "apy": 50.0, "tvl_millions": 400, "risk_level": 4, "risk_rating": "High", "yield_type": "Farming"},
    ]

    # Filter opportunities
    tvl_min_map = {"$1M": 1, "$10M": 10, "$100M": 100, "$1B": 1000}
    tvl_threshold = tvl_min_map[min_tvl]

    filtered = [
        opp for opp in opportunities
        if opp['apy'] >= min_apy
        and opp['risk_level'] <= max_risk
        and opp['tvl_millions'] >= tvl_threshold
    ]

    st.markdown(f"### Found {len(filtered)} Opportunities")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        if filtered:
            st.plotly_chart(create_apy_comparison_chart(filtered), use_container_width=True)

    with col2:
        if filtered:
            st.plotly_chart(create_risk_return_scatter(filtered), use_container_width=True)

    # Table
    st.markdown("### Detailed Opportunities")

    if filtered:
        df = pd.DataFrame(filtered)
        df['APY'] = df['apy'].apply(lambda x: f"{x}%")
        df['TVL'] = df['tvl_millions'].apply(lambda x: f"${x}M")

        st.dataframe(
            df[['protocol', 'pool', 'asset', 'APY', 'TVL', 'risk_rating', 'yield_type']].rename(columns={
                'protocol': 'Protocol',
                'pool': 'Pool',
                'asset': 'Asset',
                'risk_rating': 'Risk',
                'yield_type': 'Type'
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No opportunities match your filters. Try adjusting the criteria.")


# ====================================================================================
# PAGE: RISK ASSESSMENT
# ====================================================================================

elif "Risk Assessment" in page:
    st.markdown('<div class="main-header">⚠️ Risk Assessment</div>', unsafe_allow_html=True)

    st.markdown("### Assess DeFi Risks")

    tab1, tab2, tab3 = st.tabs(["Smart Contract Risk", "Liquidation Risk", "Portfolio Risk"])

    # Tab 1: Smart Contract Risk
    with tab1:
        st.markdown("#### Smart Contract Risk Assessment")

        col1, col2 = st.columns([1, 1])

        with col1:
            protocol_name = st.text_input("Protocol Name", "Example Protocol")
            audits = st.multiselect("Auditors", ["Trail of Bits", "OpenZeppelin", "ConsenSys", "CertiK", "Quantstamp"])
            code_lines = st.number_input("Lines of Code", min_value=100, max_value=100000, value=5000)
            days_deployed = st.number_input("Days Deployed", min_value=1, max_value=3650, value=180)
            has_bug_bounty = st.checkbox("Has Bug Bounty Program")

        with col2:
            if st.button("Assess Risk"):
                # Calculate risk score
                audit_score = min(100, 30 + len(audits) * 25)
                if has_bug_bounty:
                    audit_score += 10

                complexity_score = min(100, code_lines / 100)
                time_score = min(100, 10 + days_deployed / 10)

                overall_risk = (
                    (100 - audit_score) * 0.30 +
                    complexity_score * 0.20 +
                    (100 - time_score) * 0.20 +
                    40 * 0.30
                )

                risk_level = "Very Low" if overall_risk < 20 else ("Low" if overall_risk < 40 else "Moderate")

                st.markdown("#### Risk Assessment Results")
                st.metric("Overall Risk Score", f"{overall_risk:.1f}/100", delta=None)
                st.metric("Risk Level", risk_level)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Audit Score", f"{audit_score}/100")
                with col2:
                    st.metric("Complexity", f"{complexity_score}/100")
                with col3:
                    st.metric("Time Score", f"{time_score}/100")

                if overall_risk < 40:
                    st.success("✅ Safe to use - Low risk profile")
                else:
                    st.warning("⚠️ Use with caution - Elevated risk")

    # Tab 2: Liquidation Risk
    with tab2:
        st.markdown("#### Liquidation Risk Calculator")

        col1, col2 = st.columns([1, 1])

        with col1:
            collateral = st.number_input("Collateral Value ($)", min_value=1000, max_value=10000000, value=100000)
            debt = st.number_input("Debt Value ($)", min_value=100, max_value=10000000, value=60000)
            liq_threshold = st.slider("Liquidation Threshold (%)", 50, 95, 86) / 100

        with col2:
            # Calculate health factor
            health_factor = (collateral * liq_threshold) / debt if debt > 0 else float('inf')
            current_ltv = debt / collateral if collateral > 0 else 0
            distance = ((health_factor - 1.0) / health_factor) * 100 if health_factor != float('inf') else 100

            st.markdown("#### Health Factor Analysis")
            st.metric("Health Factor", f"{health_factor:.3f}")

            if health_factor >= 1.5:
                st.success("✅ SAFE - Position is healthy")
            elif health_factor >= 1.2:
                st.warning("⚠️ MODERATE RISK - Monitor closely")
            elif health_factor >= 1.0:
                st.error("🚨 HIGH RISK - Add collateral soon!")
            else:
                st.error("💀 CRITICAL - Position is liquidatable!")

            st.metric("Current LTV", f"{current_ltv*100:.2f}%")
            st.metric("Distance to Liquidation", f"{distance:.2f}%")

            # Price drop scenarios
            st.markdown("#### Price Drop Scenarios")
            scenarios = []
            for drop in [0.05, 0.10, 0.15, 0.20, 0.30]:
                new_coll = collateral * (1 - drop)
                new_hf = (new_coll * liq_threshold) / debt
                scenarios.append({
                    'Price Drop': f"{drop*100:.0f}%",
                    'New HF': f"{new_hf:.3f}",
                    'Status': '✅' if new_hf >= 1.2 else ('⚠️' if new_hf >= 1.0 else '💀')
                })

            st.dataframe(pd.DataFrame(scenarios), use_container_width=True, hide_index=True)

    # Tab 3: Portfolio Risk
    with tab3:
        st.markdown("#### Portfolio Risk Dashboard")

        # Sample portfolio risk metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Portfolio Risk", "28.5/100", delta="-2.1", delta_color="inverse")

        with col2:
            st.metric("Max Drawdown", "7.5%", delta="OK", delta_color="normal")

        with col3:
            st.metric("Sharpe Ratio", "1.8", delta="+0.3")

        with col4:
            st.metric("Diversification", "78/100", delta="+5")

        # Risk breakdown
        st.markdown("#### Risk Breakdown by Position")

        risk_data = pd.DataFrame({
            'Protocol': ['Aave', 'Curve', 'Uniswap V3', 'Lido', 'Yearn'],
            'Allocation': [30, 25, 25, 15, 5],
            'Risk_Score': [15, 20, 35, 25, 28],
            'Contribution': [4.5, 5.0, 8.75, 3.75, 1.4]
        })

        fig = px.bar(
            risk_data,
            x='Protocol',
            y='Contribution',
            color='Risk_Score',
            title='Risk Contribution by Protocol',
            labels={'Contribution': 'Risk Contribution'},
            color_continuous_scale='RdYlGn_r'
        )

        st.plotly_chart(fig, use_container_width=True)


# ====================================================================================
# PAGE: LIQUIDITY ANALYSIS
# ====================================================================================

elif "Liquidity Analysis" in page:
    st.markdown('<div class="main-header">💧 Liquidity Analysis</div>', unsafe_allow_html=True)

    st.markdown("### Analyze Pool Liquidity and Slippage")

    tab1, tab2 = st.tabs(["Slippage Calculator", "Pool Quality Score"])

    # Tab 1: Slippage
    with tab1:
        st.markdown("#### Slippage Calculator")
        st.markdown("Calculate expected slippage for your trade using the Constant Product Market Maker (CPMM) formula")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("##### Pool Reserves")
            reserve_in = st.number_input("Reserve IN (e.g., USDC)", min_value=1000, value=2000000, step=1000)
            reserve_out = st.number_input("Reserve OUT (e.g., ETH)", min_value=1, value=1000, step=10)
            fee = st.slider("Pool Fee (%)", 0.01, 1.0, 0.3, 0.01) / 100

            st.markdown("##### Trade Details")
            amount_in = st.number_input("Amount to Trade (IN)", min_value=100, value=10000, step=100)

        with col2:
            # Calculate slippage
            price_before = reserve_in / reserve_out
            amount_in_with_fee = amount_in * (1 - fee)
            amount_out = (reserve_out * amount_in_with_fee) / (reserve_in + amount_in_with_fee)
            execution_price = amount_in / amount_out if amount_out > 0 else 0
            slippage_percent = ((execution_price - price_before) / price_before * 100) if price_before > 0 else 0

            st.markdown("#### Results")

            st.metric("Expected Price", f"${price_before:,.2f}")
            st.metric("Execution Price", f"${execution_price:,.2f}")
            st.metric("Slippage", f"{slippage_percent:.3f}%")
            st.metric("Output Amount", f"{amount_out:.4f}")

            # Rating
            if slippage_percent < 0.1:
                st.success("✅ EXCELLENT - Minimal slippage")
            elif slippage_percent < 0.5:
                st.success("✅ GOOD - Acceptable slippage")
            elif slippage_percent < 1.0:
                st.warning("⚠️ MODERATE - Consider splitting trade")
            else:
                st.error("🚨 HIGH - High slippage, reconsider trade size")

    # Tab 2: Pool Quality
    with tab2:
        st.markdown("#### Pool Quality Scorer")

        col1, col2 = st.columns([1, 1])

        with col1:
            tvl = st.number_input("Total Value Locked ($)", min_value=100000, value=100000000, step=1000000)
            volume_24h = st.number_input("24h Volume ($)", min_value=10000, value=80000000, step=1000000)
            fee_tier = st.selectbox("Fee Tier", ["0.01%", "0.05%", "0.3%", "1.0%"])
            reserve_ratio = st.slider("Reserve Balance Ratio", 0.5, 1.5, 1.0, 0.01)

        with col2:
            # Calculate scores
            import math

            fee_map = {"0.01%": 0.0001, "0.05%": 0.0005, "0.3%": 0.003, "1.0%": 0.01}
            fee_value = fee_map[fee_tier]

            tvl_score = min(100, 50 + (math.log10(tvl) - 6) * 20) if tvl > 0 else 0
            volume_ratio = volume_24h / tvl if tvl > 0 else 0
            volume_score = min(100, 100 if volume_ratio > 0.5 else volume_ratio * 200)
            balance_score = max(0, 100 - abs(1.0 - reserve_ratio) * 200)
            fee_score = 100 if fee_value == 0.0005 else 90

            overall = (tvl_score * 0.4 + volume_score * 0.3 + balance_score * 0.2 + fee_score * 0.1)
            rating = "A+" if overall >= 90 else ("A" if overall >= 80 else ("B" if overall >= 70 else "C"))

            st.markdown("#### Pool Quality Score")

            st.metric("Overall Score", f"{overall:.1f}/100")
            st.metric("Rating", rating)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("TVL Score", f"{tvl_score:.1f}/100")
                st.metric("Volume Score", f"{volume_score:.1f}/100")

            with col2:
                st.metric("Balance Score", f"{balance_score:.1f}/100")
                st.metric("Fee Score", f"{fee_score:.1f}/100")

            st.metric("Volume/TVL Ratio", f"{volume_ratio:.4f}")

            if overall >= 80:
                st.success("✅ EXCELLENT POOL - High quality liquidity")
            elif overall >= 60:
                st.info("ℹ️ GOOD POOL - Acceptable quality")
            else:
                st.warning("⚠️ MODERATE POOL - Use with caution")


# ====================================================================================
# FOOTER
# ====================================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>DeFi Analytics Platform v1.0 | Built for Economics & Finance MSc Students</p>
    <p>⚠️ Demo version with simulated data | For research and educational purposes only</p>
</div>
""", unsafe_allow_html=True)
