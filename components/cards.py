
"""
Summary KPI card components for FinPlot AI.
Displays financial metrics using reusable card components.
"""

from typing import Any, Dict
from html import escape
from textwrap import dedent

import streamlit as st


def format_currency(val: float) -> str:
    """Format currency values."""
    if val < 0:
        return f"-${abs(val):,.2f}"
    return f"${val:,.2f}"


from html import escape
from textwrap import dedent
import streamlit as st


def render_single_card(
    title: str,
    value: str,
    subtitle: str,
    icon: str,
    card_type: str
) -> None:

    allowed_types = {
        "income", "expense", "positive", "negative", "ledger"
    }

    if card_type not in allowed_types:
        card_type = "ledger"

    card_html = dedent(f"""
    <div class="fin-metric-card">
        <div class="fin-metric-label">
            <span>{escape(str(title))}</span>
            <span class="fin-card-icon {card_type}">
                {escape(str(icon))}
            </span>
        </div>

        <div class="fin-metric-value {card_type}">
            {escape(str(value))}
        </div>

        <div class="fin-metric-subtext">
            {escape(str(subtitle))}
        </div>
    </div>
    """).strip()
    st.html(card_html)
    

def render_metric_cards(metrics: Dict[str, Any]) -> None:
    """Render four financial KPI cards."""

    total_income = metrics.get("total_income", 0.0)
    total_expenses = metrics.get("total_expenses", 0.0)
    net_cash_flow = metrics.get("net_cash_flow", 0.0)
    net_margin = metrics.get("net_margin", 0.0)

    tx_count = metrics.get("transaction_count", 0)
    income_count = metrics.get("income_count", 0)
    expense_count = metrics.get("expense_count", 0)

    flow_class = (
        "positive" if net_cash_flow >= 0 else "negative"
    )

    flow_status = (
        "Cash Surplus" if net_cash_flow >= 0
        else "Cash Deficit"
    )

    columns = st.columns(4, gap="medium")

    with columns[0]:
        render_single_card(
            "Total Income",
            format_currency(total_income),
            f"{income_count} recorded income streams",
            "↗",
            "income",
        )

    with columns[1]:
        render_single_card(
            "Total Expenses",
            format_currency(total_expenses),
            f"{expense_count} recorded expense items",
            "↘",
            "expense",
        )

    with columns[2]:
        render_single_card(
            "Net Cash Flow",
            format_currency(net_cash_flow),
            f"{flow_status} ({net_margin:+.1f}% margin)",
            "●",
            flow_class,
        )

    with columns[3]:
        render_single_card(
            "Ledger Activity",
            str(tx_count),
            "Total reconciled transactions",
            "▦",
            "ledger",
        )
