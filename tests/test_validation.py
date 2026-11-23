"""
Unit tests for transaction input validation and parsing utilities.
Validates:
- Amount parsing and strictly positive constraints
- Date parsing across formats
- Transaction payload integrity and error reporting
"""

from datetime import date
import pytest
from utils.validators import (
    parse_amount,
    parse_date,
    validate_transaction_payload,
)


def test_parse_amount_valid():
    """Verify numeric, string, currency-symbol, and delimited amount parsing."""
    assert parse_amount(150.50) == 150.50
    assert parse_amount(200) == 200.0
    assert parse_amount("$1,250.75") == 1250.75
    assert parse_amount(" 500 ") == 500.0
    assert parse_amount("€3,400.00") == 3400.0


def test_parse_amount_invalid():
    """Verify non-numeric or malformed values return None."""
    assert parse_amount(None) is None
    assert parse_amount("") is None
    assert parse_amount("abc") is None
    assert parse_amount("$NaN") is None


def test_parse_date_formats():
    """Verify parsing ISO, US, and EU formatted date strings."""
    assert parse_date("2026-03-15") == date(2026, 3, 15)
    assert parse_date("03/15/2026") == date(2026, 3, 15)
    assert parse_date("15-03-2026") == date(2026, 3, 15)
    assert parse_date(date(2026, 3, 15)) == date(2026, 3, 15)


def test_parse_date_invalid():
    """Verify malformed dates return None."""
    assert parse_date(None) is None
    assert parse_date("not-a-date") is None
    assert parse_date("2026-99-99") is None


def test_validate_transaction_payload_valid():
    """Verify that a compliant payload passes with no error messages."""
    payload = {
        "transaction_date": "2026-03-15",
        "description": "AWS Cloud Hosting",
        "amount": 250.00,
        "transaction_type": "expense",
        "category": "Cloud & Infrastructure",
        "payment_method": "Credit Card",
        "notes": "Monthly billing",
    }
    is_valid, errors = validate_transaction_payload(payload)
    assert is_valid is True
    assert len(errors) == 0


def test_validate_transaction_payload_negative_amount():
    """Verify that negative amounts or zero are rejected."""
    payload = {
        "transaction_date": "2026-03-15",
        "description": "Office Supplies",
        "amount": -50.00,
        "transaction_type": "expense",
        "category": "Office Supplies & Equipment",
    }
    is_valid, errors = validate_transaction_payload(payload)
    assert is_valid is False
    assert any("strictly greater than zero" in e for e in errors)


def test_validate_transaction_payload_missing_required():
    """Verify missing description, category, and invalid type are caught."""
    payload = {
        "transaction_date": "2026-03-15",
        "description": "   ",
        "amount": 100.00,
        "transaction_type": "invalid_type",
        "category": "",
    }
    is_valid, errors = validate_transaction_payload(payload)
    assert is_valid is False
    assert any("Description is required" in e for e in errors)
    assert any("Transaction type must be one of" in e for e in errors)
    assert any("Category is required" in e for e in errors)
