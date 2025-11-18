"""
Tests for DeFi risk models
"""
import pytest
from risk.defi_risk_models import SmartContractRiskAnalyzer, LiquidationRiskAnalyzer


class TestSmartContractRiskAnalyzer:
    """Test cases for SmartContractRiskAnalyzer"""

    def test_assess_smart_contract_risk(self, sample_protocol_data):
        """Test smart contract risk assessment"""
        analyzer = SmartContractRiskAnalyzer()

        risk = analyzer.assess_smart_contract_risk(
            protocol_name=sample_protocol_data["protocol_name"],
            contract_address=sample_protocol_data["contract_address"],
            auditors=sample_protocol_data["auditors"],
            code_lines=sample_protocol_data["code_lines"],
            days_deployed=sample_protocol_data["days_deployed"],
            tvl_usd=sample_protocol_data["tvl_usd"],
            upgrade_mechanism="Timelock + Multisig",
            has_bug_bounty=True,
            admin_control_level="Low"
        )

        assert risk is not None
        assert 0 <= risk.overall_risk_score <= 100
        assert risk.risk_level is not None


class TestLiquidationRiskAnalyzer:
    """Test cases for LiquidationRiskAnalyzer"""

    def test_assess_liquidation_risk(self):
        """Test liquidation risk assessment"""
        analyzer = LiquidationRiskAnalyzer()

        risk = analyzer.assess_liquidation_risk(
            protocol_name="Aave",
            asset="ETH",
            collateral_value_usd=100_000,
            debt_value_usd=60_000
        )

        assert risk is not None
        assert risk.health_factor > 0
        assert risk.distance_to_liquidation_percent >= 0
