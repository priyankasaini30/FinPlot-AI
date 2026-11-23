"""
Unit tests for deterministic financial calculations and analytics services.
Validates:
- Total Income calculation
- Total Expenses calculation
- Net Cash Flow (Income - Expenses)
- Profit margin and averages
- Monthly aggregations and category distribution
"""

import pytest
from services.analytics_service import (
    calculate_metrics,
    get_monthly_summary,
    get_category_summary,
    get_cumulative_cashflow,
)


def test_calculate_metrics_empty():
    """Verify that an empty list returns clean zeroed metrics without ZeroDivisionError."""
    res = calculate_metrics([])
    assert res["total_income"] == 0.0
    assert res["total_expenses"] == 0.0
    assert res["net_cash_flow"] == 0.0
    assert res["net_margin"] == 0.0
    assert res["transaction_count"] == 0
    assert res["income_count"] == 0
    assert res["expense_count"] == 0


def test_calculate_metrics_surplus():
    """Verify positive net cash flow calculation."""
    txs = [
        {"amount": 5000.00, "transaction_type": "income"},
        {"amount": 2500.00, "transaction_type": "income"},
        {"amount": 1500.00, "transaction_type": "expense"},
        {"amount": 500.00, "transaction_type": "expense"},
    ]
    res = calculate_metrics(txs)
    assert res["total_income"] == 7500.00
    assert res["total_expenses"] == 2000.00
    assert res["net_cash_flow"] == 5500.00
    # Margin: 5500 / 7500 * 100 = 73.33%
    assert res["net_margin"] == 73.33
    assert res["transaction_count"] == 4
    assert res["income_count"] == 2
    assert res["expense_count"] == 2
    assert res["avg_income"] == 3750.00
    assert res["avg_expense"] == 1000.00


def test_calculate_metrics_deficit():
    """Verify negative net cash flow (deficit) calculation."""
    txs = [
        {"amount": 1000.00, "transaction_type": "income"},
        {"amount": 3500.00, "transaction_type": "expense"},
    ]
    res = calculate_metrics(txs)
    assert res["total_income"] == 1000.00
    assert res["total_expenses"] == 3500.00
    assert res["net_cash_flow"] == -2500.00
    assert res["net_margin"] == -250.00


def test_monthly_summary_aggregation():
    """Verify grouping and net calculation by calendar month."""
    txs = [
        {"transaction_date": "2026-01-10", "amount": 1000.00, "transaction_type": "income"},
        {"transaction_date": "2026-01-20", "amount": 400.00, "transaction_type": "expense"},
        {"transaction_date": "2026-02-05", "amount": 2000.00, "transaction_type": "income"},
        {"transaction_date": "2026-02-15", "amount": 800.00, "transaction_type": "expense"},
    ]
    df = get_monthly_summary(txs)
    assert len(df) == 2
    jan = df[df["month_year"] == "2026-01"].iloc[0]
    assert jan["income"] == 1000.00
    assert jan["expense"] == 400.00
    assert jan["net_flow"] == 600.00

    feb = df[df["month_year"] == "2026-02"].iloc[0]
    assert feb["income"] == 2000.00
    assert feb["expense"] == 800.00
    assert feb["net_flow"] == 1200.00


def test_category_summary():
    """Verify category breakdown sums, counts, percentages, and sorting."""
    txs = [
        {"category": "Cloud & Infrastructure", "amount": 300.00, "transaction_type": "expense"},
        {"category": "Cloud & Infrastructure", "amount": 700.00, "transaction_type": "expense"},
        {"category": "Software & SaaS", "amount": 500.00, "transaction_type": "expense"},
        {"category": "Sales Revenue", "amount": 9000.00, "transaction_type": "income"},
    ]
    df = get_category_summary(txs, transaction_type="expense")
    assert len(df) == 2
    # First row should be highest amount (Cloud: 1000)
    assert df.iloc[0]["category"] == "Cloud & Infrastructure"
    assert df.iloc[0]["amount"] == 1000.00
    assert df.iloc[0]["percentage"] == 66.7
    assert df.iloc[0]["count"] == 2

    assert df.iloc[1]["category"] == "Software & SaaS"
    assert df.iloc[1]["amount"] == 500.00
    assert df.iloc[1]["percentage"] == 33.3


def test_cumulative_cashflow_trend():
    """Verify running cumulative balance computation over time."""
    txs = [
        {"transaction_date": "2026-03-01", "amount": 500.00, "transaction_type": "income"},
        {"transaction_date": "2026-03-02", "amount": 200.00, "transaction_type": "expense"},
        {"transaction_date": "2026-03-03", "amount": 100.00, "transaction_type": "expense"},
    ]
    df = get_cumulative_cashflow(txs)
    assert len(df) == 3
    assert df.iloc[0]["cumulative_balance"] == 500.00
    assert df.iloc[1]["cumulative_balance"] == 300.00
    assert df.iloc[2]["cumulative_balance"] == 200.00
