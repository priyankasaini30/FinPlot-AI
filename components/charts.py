"""
Interactive financial visualization charts for FinPlot AI using Plotly.
Includes:
- Monthly Income vs Expense comparison (Grouped Bar Chart)
- Category-wise Expense distribution (Interactive Donut Chart)
- Cumulative Cash Flow trajectory (Area Chart)
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

CHART_THEME = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "Inter, sans-serif", "color": "#94a3b8"},
    "margin": dict(l=20, r=20, t=40, b=20),
}

CATEGORY_COLORS = [
    "#38bdf8",  # Sky
    "#818cf8",  # Indigo
    "#f43f5e",  # Rose
    "#34d399",  # Emerald
    "#fbbf24",  # Amber
    "#c084fc",  # Purple
    "#fb923c",  # Orange
    "#2dd4bf",  # Teal
    "#a3e635",  # Lime
    "#f472b6",  # Pink
]


def render_monthly_chart(monthly_df: pd.DataFrame) -> None:
    """Renders grouped bar chart of Income vs Expense by month."""
    if monthly_df.empty:
        st.info("No monthly data available to plot yet.")
        return

    fig = go.Figure()

    # Income Bars
    fig.add_trace(
        go.Bar(
            name="Income",
            x=monthly_df["period_label"],
            y=monthly_df["income"],
            marker_color="#10b981",
            hovertemplate="<b>%{x}</b><br>Income: $%{y:,.2f}<extra></extra>",
            marker_line_width=0,
            opacity=0.9,
        )
    )

    # Expense Bars
    fig.add_trace(
        go.Bar(
            name="Expense",
            x=monthly_df["period_label"],
            y=monthly_df["expense"],
            marker_color="#f43f5e",
            hovertemplate="<b>%{x}</b><br>Expense: $%{y:,.2f}<extra></extra>",
            marker_line_width=0,
            opacity=0.9,
        )
    )

    # Net Cash Flow Line Overlay
    fig.add_trace(
        go.Scatter(
            name="Net Flow",
            x=monthly_df["period_label"],
            y=monthly_df["net_flow"],
            mode="lines+markers",
            line=dict(color="#38bdf8", width=3, dash="dot"),
            marker=dict(size=7, color="#38bdf8"),
            hovertemplate="<b>%{x}</b><br>Net Flow: $%{y:,.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        **CHART_THEME,
        barmode="group",
        bargap=0.25,
        bargroupgap=0.1,
        title=dict(
            text="Monthly Revenue & Expenditure",
            font=dict(size=15, color="#f1f5f9", family="Inter"),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12, color="#94a3b8"),
        ),
        xaxis=dict(
            showgrid=False,
            color="#64748b",
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.06)",
            color="#64748b",
            tickprefix="$",
            tickformat=",.0f",
            tickfont=dict(size=11),
        ),
        height=360,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_category_donut(
    cat_df: pd.DataFrame, transaction_type: str = "expense"
) -> None:
    """Renders interactive donut breakdown chart by category."""
    title_label = "Expenses by Category" if transaction_type == "expense" else "Income by Category"

    if cat_df.empty:
        st.info(f"No {transaction_type} transactions found for category breakdown.")
        return

    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels=cat_df["category"],
            values=cat_df["amount"],
            hole=0.55,
            marker=dict(colors=CATEGORY_COLORS[: len(cat_df)]),
            textinfo="percent+label",
            textposition="outside",
            insidetextorientation="horizontal",
            hovertemplate="<b>%{label}</b><br>Amount: $%{value:,.2f}<br>Share: %{percent}<extra></extra>",
            showlegend=False,
        )
    )

    fig.update_layout(
        **CHART_THEME,
        title=dict(
            text=title_label,
            font=dict(size=15, color="#f1f5f9", family="Inter"),
        ),
        annotations=[
            dict(
                text=f"Total<br><b>${cat_df['amount'].sum():,.0f}</b>",
                x=0.5,
                y=0.5,
                font=dict(size=13, color="#f8fafc", family="Inter"),
                showarrow=False,
            )
        ],
        height=360,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_cashflow_trend(trend_df: pd.DataFrame) -> None:
    """Renders cumulative net cash flow trajectory area chart over time."""
    if trend_df.empty:
        return

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=trend_df["date"],
            y=trend_df["cumulative_balance"],
            mode="lines",
            line=dict(color="#6366f1", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(99, 102, 241, 0.12)",
            hovertemplate="<b>%{x}</b><br>Cumulative Cash: $%{y:,.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        **CHART_THEME,
        title=dict(
            text="Cumulative Cash Balance Trajectory",
            font=dict(size=15, color="#f1f5f9", family="Inter"),
        ),
        xaxis=dict(
            showgrid=False,
            color="#64748b",
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.06)",
            color="#64748b",
            tickprefix="$",
            tickformat=",.0f",
            tickfont=dict(size=11),
        ),
        height=320,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
