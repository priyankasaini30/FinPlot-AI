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
    background: linear-gradient(145deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.25rem 1.4rem;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.25);
    transition: transform 0.2s ease, border-color 0.2s ease;
    height: 100%;
}
.fin-metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4);
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
</style>
"""


def apply_custom_css():
    """Injects custom CSS styles into the active Streamlit app."""
    import streamlit as st

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
