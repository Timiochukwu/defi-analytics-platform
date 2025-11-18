"""
Tests for liquidity analyzer module
"""
import pytest
from analytics.liquidity_analyzer import LiquidityAnalyzer


class TestLiquidityAnalyzer:
    """Test cases for LiquidityAnalyzer"""

    def test_calculate_slippage_constant_product(self, sample_pool_data):
        """Test slippage calculation for constant product AMM"""
        analyzer = LiquidityAnalyzer()

        result = analyzer.calculate_slippage_constant_product(
            reserve_in=sample_pool_data["reserve_in"],
            reserve_out=sample_pool_data["reserve_out"],
            amount_in=10_000,
            fee=0.003
        )

        assert result is not None
        assert "slippage_percent" in result.__dict__
        assert result.slippage_percent >= 0
        assert result.amount_out > 0

    def test_calculate_pool_quality_score(self, sample_pool_data):
        """Test pool quality scoring"""
        analyzer = LiquidityAnalyzer()

        score = analyzer.calculate_pool_quality_score(
            tvl=sample_pool_data["tvl"],
            volume_24h=sample_pool_data["volume_24h"],
            fee_tier=sample_pool_data["fee_tier"],
            reserve_ratio=0.98
        )

        assert score is not None
        assert "overall_score" in score
        assert 0 <= score["overall_score"] <= 100
        assert "rating" in score

    def test_calculate_impermanent_loss(self):
        """Test impermanent loss calculation"""
        analyzer = LiquidityAnalyzer()

        result = analyzer.calculate_impermanent_loss(
            price_start=1000,
            price_end=2000
        )

        assert result is not None
        assert "il_percent" in result
        assert result["il_percent"] < 0  # IL is always negative
