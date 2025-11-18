"""
Mathematical utility functions
"""
from typing import Optional
import math


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values

    Args:
        old_value: Original value
        new_value: New value

    Returns:
        Percentage change
    """
    if old_value == 0:
        return 0.0 if new_value == 0 else float('inf')

    return ((new_value - old_value) / old_value) * 100


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero

    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if denominator is zero

    Returns:
        Result of division or default
    """
    if denominator == 0:
        return default
    return numerator / denominator


def calculate_compound_interest(
    principal: float,
    rate: float,
    time: float,
    n: int = 365
) -> float:
    """
    Calculate compound interest

    Args:
        principal: Initial principal
        rate: Annual interest rate (as decimal, e.g., 0.08 for 8%)
        time: Time in years
        n: Number of compounding periods per year

    Returns:
        Final amount
    """
    return principal * math.pow((1 + rate / n), n * time)


def calculate_apy_from_apr(apr: float, compounds_per_year: int = 365) -> float:
    """
    Convert APR to APY (accounting for compounding)

    Args:
        apr: Annual Percentage Rate (as decimal)
        compounds_per_year: Number of compounds per year

    Returns:
        Annual Percentage Yield (as decimal)
    """
    return math.pow(1 + apr / compounds_per_year, compounds_per_year) - 1


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp a value between min and max

    Args:
        value: Value to clamp
        min_value: Minimum value
        max_value: Maximum value

    Returns:
        Clamped value
    """
    return max(min_value, min(max_value, value))
