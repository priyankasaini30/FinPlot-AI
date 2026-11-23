"""
Deterministic financial calculations and analytics service for FinPlot AI.
Implements core accounting formulas:
- Total Income = Sum(amount WHERE transaction_type == 'income')
- Total Expenses = Sum(amount WHERE transaction_type == 'expense')
- Net Cash Flow = Total Income - Total Expenses
- Monthly aggregations and category distribution analysis
"""

from typing import Any, Dict, List, Optional
import pandas as pd


def calculate_metrics(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes top-level financial metrics from a list of transaction records.
    All calculations are deterministic and testable.
    """
    if not transactions:
        return {
            "total_income": 0.0,
            "total_expenses": 0.0,
            "net_cash_flow": 0.0,
            "net_margin": 0.0,
            "transaction_count": 0,
            "income_count": 0,
            "expense_count": 0,
            "avg_income": 0.0,
            "avg_expense": 0.0,
        }

    total_income = 0.0
    total_expenses = 0.0
    income_count = 0
    expense_count = 0

    for tx in transactions:
        amount = float(tx.get("amount", 0.0))
        t_type = str(tx.get("transaction_type", "")).strip().lower()

        if t_type == "income":
            total_income += amount
            income_count += 1
        elif t_type == "expense":
            total_expenses += amount
            expense_count += 1

    net_cash_flow = total_income - total_expenses
    net_margin = (
        (net_cash_flow / total_income * 100.0) if total_income > 0 else 0.0
    )

    avg_income = (total_income / income_count) if income_count > 0 else 0.0
    avg_expense = (total_expenses / expense_count) if expense_count > 0 else 0.0

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_cash_flow": round(net_cash_flow, 2),
        "net_margin": round(net_margin, 2),
        "transaction_count": len(transactions),
        "income_count": income_count,
        "expense_count": expense_count,
        "avg_income": round(avg_income, 2),
        "avg_expense": round(avg_expense, 2),
    }


def get_monthly_summary(transactions: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Groups transactions by calendar month (YYYY-MM).
    Returns DataFrame with columns: ['month_year', 'period_label', 'income', 'expense', 'net_flow'].
    Sorted chronologically.
    """
    if not transactions:
        return pd.DataFrame(
            columns=["month_year", "period_label", "income", "expense", "net_flow"]
        )

    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df = df.dropna(subset=["date"])

    if df.empty:
        return pd.DataFrame(
            columns=["month_year", "period_label", "income", "expense", "net_flow"]
        )

    df["month_year"] = df["date"].dt.strftime("%Y-%m")
    df["period_label"] = df["date"].dt.strftime("%b %Y")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)

    # Pivot income and expense
    pivoted = (
        df.groupby(["month_year", "period_label", "transaction_type"])["amount"]
        .sum()
        .unstack(fill_value=0.0)
        .reset_index()
    )

    if "income" not in pivoted.columns:
        pivoted["income"] = 0.0
    if "expense" not in pivoted.columns:
        pivoted["expense"] = 0.0

    pivoted["net_flow"] = pivoted["income"] - pivoted["expense"]
    pivoted = pivoted.sort_values("month_year").reset_index(drop=True)

    return pivoted[["month_year", "period_label", "income", "expense", "net_flow"]]


def get_category_summary(
    transactions: List[Dict[str, Any]],
    transaction_type: str = "expense",
) -> pd.DataFrame:
    """
    Aggregates transactions by category for a specific type (expense or income).
    Returns DataFrame: ['category', 'amount', 'percentage', 'count'] sorted descending by amount.
    """
    if not transactions:
        return pd.DataFrame(columns=["category", "amount", "percentage", "count"])

    filtered = [
        tx
        for tx in transactions
        if str(tx.get("transaction_type", "")).strip().lower()
        == transaction_type.lower()
    ]

    if not filtered:
        return pd.DataFrame(columns=["category", "amount", "percentage", "count"])

    df = pd.DataFrame(filtered)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)

    summary = (
        df.groupby("category")
        .agg(amount=("amount", "sum"), count=("amount", "count"))
        .reset_index()
    )

    total_amount = summary["amount"].sum()
    if total_amount > 0:
        summary["percentage"] = (summary["amount"] / total_amount * 100.0).round(1)
    else:
        summary["percentage"] = 0.0

    summary = summary.sort_values(by="amount", ascending=False).reset_index(drop=True)
    summary["amount"] = summary["amount"].round(2)
    return summary


def get_cumulative_cashflow(transactions: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Computes chronological cumulative running cash flow over time.
    Returns DataFrame: ['date', 'daily_net', 'cumulative_balance']
    """
    if not transactions:
        return pd.DataFrame(columns=["date", "daily_net", "cumulative_balance"])

    df = pd.DataFrame(transactions)
    df["date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df = df.dropna(subset=["date"])
    if df.empty:
        return pd.DataFrame(columns=["date", "daily_net", "cumulative_balance"])

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["signed_amount"] = df.apply(
        lambda r: r["amount"] if r["transaction_type"] == "income" else -r["amount"],
        axis=1,
    )

    daily = (
        df.groupby(df["date"].dt.date)["signed_amount"]
        .sum()
        .reset_index()
        .rename(columns={"signed_amount": "daily_net"})
    )
    daily = daily.sort_values("date").reset_index(drop=True)
    daily["cumulative_balance"] = daily["daily_net"].cumsum().round(2)
    return daily
