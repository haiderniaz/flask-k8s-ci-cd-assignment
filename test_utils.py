import pytest
from utils import add_numbers


def test_add_numbers_positive():
    """Test adding two positive numbers."""
    assert add_numbers(5, 3) == 8


def test_add_numbers_negative():
    """Test adding two negative numbers."""
    assert add_numbers(-5, -3) == -8


def test_add_numbers_mixed():
    """Test adding positive and negative numbers."""
    assert add_numbers(10, -5) == 5


def test_add_numbers_zero():
    """Test adding with zero."""
    assert add_numbers(0, 5) == 5
    assert add_numbers(5, 0) == 5

