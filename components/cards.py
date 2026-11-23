"""
Summary KPI card components for FinPlot AI.
Renders Total Income, Total Expenses, Net Cash Flow, and operational metrics.
"""

from typing import Any, Dict
import streamlit as st


def format_currency(val: float) -> str:
    """Format floating point numbers into standard currency string ($X,XXX.XX)."""
    if val < 0:
        return f"-${abs(val):,.2f}"
    return f"${val:,.2f}"


def render_metric_cards(metrics: Dict[str, Any]) -> None:
    """
    Renders the three core financial KPI cards plus a ledger activity card
    in a responsive 4-column layout.
    """
    total_income = metrics.get("total_income", 0.0)
    total_expenses = metrics.get("total_expenses", 0.0)
    net_cash_flow = metrics.get("net_cash_flow", 0.0)
    net_margin = metrics.get("net_margin", 0.0)
    tx_count = metrics.get("transaction_count", 0)
    income_count = metrics.get("income_count", 0)
    expense_count = metrics.get("expense_count", 0)

    col1, col2, col3, col4 = st.columns(4)

    # 1. Total Income Card
    with col1:
        st.markdown(
            f"""
            <div class="fin-metric-card">
                <div class="fin-metric-label">
                    <span>Total Income</span>
                    <span style="color: #34d399; font-size: 1rem;">↗</span>
                </div>
                <div class="fin-metric-value income">{format_currency(total_income)}</div>
                <div class="fin-metric-subtext">
                    <span>{income_count} recorded income stream{'s' if income_count != 1 else ''}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 2. Total Expenses Card
    with col2:
        st.markdown(
            f"""
            <div class="fin-metric-card">
                <div class="fin-metric-label">
                    <span>Total Expenses</span>
                    <span style="color: #fb7185; font-size: 1rem;">↘</span>
                </div>
                <div class="fin-metric-value expense">{format_currency(total_expenses)}</div>
                <div class="fin-metric-subtext">
                    <span>{expense_count} recorded expense item{'s' if expense_count != 1 else ''}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 3. Net Cash Flow Card
    with col3:
        flow_class = "positive" if net_cash_flow >= 0 else "negative"
        indicator_icon = "🟢" if net_cash_flow >= 0 else "🔴"
        flow_status = "Cash Surplus" if net_cash_flow >= 0 else "Cash Deficit"

        st.markdown(
            f"""
            <div class="fin-metric-card">
                <div class="fin-metric-label">
                    <span>Net Cash Flow</span>
                    <span>{indicator_icon}</span>
                </div>
                <div class="fin-metric-value {flow_class}">{format_currency(net_cash_flow)}</div>
                <div class="fin-metric-subtext">
                    <span>{flow_status} ({net_margin:+.1f}% margin)</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 4. Active Ledger Overview
    with col4:
        st.markdown(
            f"""
            <div class="fin-metric-card">
                <div class="fin-metric-label">
                    <span>Ledger Activity</span>
                    <span style="color: #818cf8; font-size: 1rem;">📊</span>
                </div>
                <div class="fin-metric-value" style="color: #e2e8f0;">{tx_count}</div>
                <div class="fin-metric-subtext">
                    <span>Total reconciled transactions</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
