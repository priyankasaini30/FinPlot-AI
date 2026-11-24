"""
Design system and CSS stylesheets for FinPlot AI.
Implements a modern, responsive, high-aesthetic dark/modern corporate interface
inspired by contemporary AI-native fintech tools (e.g., Rillet).
"""

CUSTOM_CSS = """
<style>
/* Import Inter font from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Base App Layout Padding */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3.5rem;
    max-width: 1400px;
}

/* Sidebar Branding Header */
.sidebar-brand-box {
    padding: 1.2rem 1rem;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    margin-bottom: 1.5rem;
    text-align: center;
}
.brand-title {
    font-size: 1.4rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
}
.brand-tagline {
    font-size: 0.75rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}

/* Storage Status Banner Badge */
.status-badge-cloud {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.75rem;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 9999px;
    color: #34d399;
    font-size: 0.78rem;
    font-weight: 600;
}
.status-badge-local {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.75rem;
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 9999px;
    color: #fbbf24;
    font-size: 0.78rem;
    font-weight: 600;
}

/* Metric Cards */
.fin-metric-card {
    min-height: 135px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: linear-gradient(145deg, #172536, #111827);
    border: 1px solid #26364a;
    border-radius: 14px;
    padding: 1.35rem;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.16);
    transition: all 0.25s ease;
}
.fin-metric-card:hover {
    transform: translateY(-4px);
    border-color: #6366f1;
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.12);
}
.fin-metric-label {
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    margin-bottom: 0.4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.fin-metric-value {
    font-size: 1.95rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #f8fafc;
    line-height: 1.2;
    margin-bottom: 0.35rem;
    font-family: 'Inter', sans-serif;
}
.fin-metric-value.income {
    color: #10b981;
}
.fin-metric-value.expense {
    color: #f43f5e;
}
.fin-metric-value.positive {
    color: #06b6d4;
}
.fin-metric-value.negative {
    color: #f43f5e;
}
.fin-metric-subtext {
    font-size: 0.78rem;
    color: #64748b;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* Badges for Transactions */
.badge-income {
    background-color: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.75rem;
    display: inline-block;
}
.badge-expense {
    background-color: rgba(244, 63, 94, 0.15);
    color: #fb7185;
    border: 1px solid rgba(244, 63, 94, 0.3);
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.75rem;
    display: inline-block;
}
.badge-demo {
    background-color: rgba(139, 92, 246, 0.15);
    color: #c084fc;
    border: 1px solid rgba(139, 92, 246, 0.3);
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.7rem;
    display: inline-block;
}

/* Section Header Container */
.section-header-box {
    margin-top: 1rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #f1f5f9;
    margin: 0;
}
.section-subtitle {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 0.2rem;
}

/* Empty State Box */
.empty-state-box {
    text-align: center;
    padding: 3rem 1.5rem;
    background: rgba(30, 41, 59, 0.4);
    border: 1px dashed rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    margin: 1.5rem 0;
}
.empty-state-icon {
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
}
.empty-state-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.3rem;
}
.empty-state-desc {
    font-size: 0.85rem;
    color: #94a3b8;
    max-width: 480px;
    margin: 0 auto;
    }

/* =====================================
   STREAMLIT WIDGETS - GLOBAL STYLING
===================================== */

/* Primary Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: #ffffff;
    border: none;
    border-radius: 9px;
    padding: 0.55rem 1.2rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #4f46e5, #4338ca);
    border-color: transparent;
    transform: translateY(-1px);
}

/* Input Fields */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTextArea textarea {
    background-color: #172536;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
}
.stTextInput input:focus,
.stNumberInput input:focus,
.stDateInput input:focus,
.stTextArea textarea:focus {
    border-color: #818cf8;
    box-shadow: 0 0 0 1px #818cf8;
}

/* Select Boxes */
.stSelectbox [data-baseweb="select"] > div {
    background-color: #172536;
    border-color: #334155;
    border-radius: 8px;
}

/* Dataframes and Tables */
.stDataFrame {
    border: 1px solid #334155;
    border-radius: 10px;
    overflow: hidden;
}

/* Dividers */
hr {
    border-color: rgba(148, 163, 184, 0.15);
}

/* KPI Card Improvements */

.fin-card-icon {
    font-size: 1.1rem;
    font-weight: 700;
}

.fin-card-icon.income {
    color: #34d399;
}

.fin-card-icon.expense {
    color: #fb7185;
}

.fin-card-icon.positive {
    color: #22d3ee;
}

.fin-card-icon.negative {
    color: #fb7185;
}

.fin-card-icon.ledger {
    color: #818cf8;
}

.fin-metric-value.ledger {
    color: #e2e8f0;
}

.fin-metric-value.positive {
    color: #22d3ee;
}

.fin-metric-value.negative {
    color: #fb7185;
}


@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem;
    }

    .fin-metric-card {
        padding: 1rem;
        min-height: 120px;
    }

    .fin-metric-value {
        font-size: 1.5rem;
    }

    .section-title {
        font-size: 1.15rem;
    }
}

/* =====================================
   SIDEBAR REDESIGN
===================================== */

/* Sidebar background */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #263449;
}

/* Sidebar content spacing */
section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

/* Branding */
.sidebar-brand-box {
    text-align: center;
    padding: 1.3rem 0.8rem;
    margin-bottom: 1.2rem;
    background: linear-gradient(145deg, #1e293b, #151e2e);
    border: 1px solid #334155;
    border-radius: 14px;
}

.brand-logo {
    width: 42px;
    height: 42px;
    margin: 0 auto 0.7rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-size: 1rem;
    font-weight: 800;
}

.brand-title {
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-tagline {
    margin-top: 0.4rem;
    color: #94a3b8;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 1.1px;
}

/* Storage status */
.sidebar-status {
    display: flex;
    justify-content: center;
    margin: 0.8rem 0 1.2rem;
}

.status-badge-cloud,
.status-badge-local {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 0.75rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
}

.status-dot {
    font-size: 0.65rem;
}

/* Section headings */
.sidebar-section-title {
    color: #8192aa;
    font-size: 0.69rem;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin: 0.5rem 0 0.8rem;
}

/* Navigation items */
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
    gap: 0.4rem;
}

section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 9px;
    padding: 0.55rem 0.7rem;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] .stRadio
[role="radiogroup"] label:hover {
    background: #1e293b;
    border-color: #334155;
}

/* Highlight selected navigation item */
section[data-testid="stSidebar"] .stRadio
[role="radiogroup"] label:has(input:checked) {
    background: rgba(99, 102, 241, 0.16);
    border: 1px solid rgba(129, 140, 248, 0.4);
}

/* Sidebar dividers */
.sidebar-divider {
    height: 1px;
    background: #293548;
    margin: 1.3rem 0;
}

/* Description */
.sidebar-description {
    color: #94a3b8;
    font-size: 0.78rem;
    line-height: 1.6;
    margin-bottom: 0.9rem;
}

/* Demo buttons */
section[data-testid="stSidebar"] .stButton button {
    min-height: 38px;
    font-size: 0.76rem;
    border-radius: 8px;
}

/* Database statistics */
.sidebar-stats {
    margin-top: 1.1rem;
    padding: 0.9rem;
    background: #172536;
    border: 1px solid #2b3b50;
    border-radius: 10px;
}

.sidebar-stats-heading {
    color: #8192aa;
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 0.8rem;
}

.sidebar-stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #cbd5e1;
    font-size: 0.78rem;
    padding: 0.35rem 0;
}

.sidebar-stat-row strong {
    color: #f8fafc;
}

.sidebar-stat-row .live-count {
    color: #34d399;
}

.sidebar-stat-row .demo-count {
    color: #c084fc;
}

/* Footer */
.sidebar-footer {
    display: flex;
    justify-content: space-between;
    margin-top: 1.5rem;
    padding-top: 0.9rem;
    border-top: 1px solid #293548;
    color: #64748b;
    font-size: 0.68rem;
    font-weight: 600;
}


</style>
"""


def apply_custom_css():
    """Injects custom CSS styles into the active Streamlit app."""
    import streamlit as st

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
