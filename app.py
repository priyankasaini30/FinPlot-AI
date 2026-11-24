"""
FinPlot AI — AI-Powered Bookkeeping, Transaction Management, and Financial Reconciliation System.
Phase 1: Working Dashboard & Transaction Management.

Architecture:
- Frontend: Streamlit
- Database: Supabase PostgreSQL (Cloud) with fallback to local SQLite for offline/demo development
- Analytics: Deterministic financial calculations via Pandas
- Visualizations: Interactive Plotly charts
"""
from textwrap import dedent
from html import escape
from datetime import date, timedelta
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="FinPlot AI — Financial Management System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.styles import apply_custom_css
from components.cards import render_metric_cards, format_currency
from components.charts import (
    render_monthly_chart,
    render_category_donut,
    render_cashflow_trend,
)
from components.transaction_form import render_transaction_form
from components.transaction_table import render_transaction_table

from database.repository import get_repository
from services.transaction_service import TransactionService
from services.analytics_service import (
    calculate_metrics,
    get_monthly_summary,
    get_category_summary,
    get_cumulative_cashflow,
)
from services.import_service import (
    parse_and_validate_file,
    get_csv_template,
)
from utils.validators import (
    DEFAULT_EXPENSE_CATEGORIES,
    DEFAULT_INCOME_CATEGORIES,
)


def initialize_app_services():
    """Initializes and caches database repository and transaction service."""
    repo, status = get_repository()
    service = TransactionService(repo)
    return service, status


def render_sidebar(service: TransactionService, status: dict):
    """Render the FinPlot AI sidebar."""

    with st.sidebar:

        # ---------------- BRANDING ----------------
        st.markdown(
            """
            <div class="sidebar-brand-box">
                <div class="brand-logo">FP</div>
                <div class="brand-title">FinPlot AI</div>
                <div class="brand-tagline">
                    FINANCIAL INTELLIGENCE PLATFORM
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---------------- STORAGE STATUS ----------------
        is_cloud = (
            status.get("mode") == "supabase"
            and status.get("is_connected", False)
        )

        if is_cloud:
            status_label = "Supabase Cloud Active"
            status_class = "status-badge-cloud"
            status_icon = "●"
        else:
            status_label = "Local SQLite Demo Mode"
            status_class = "status-badge-local"
            status_icon = "●"

        st.markdown(
            f"""
            <div class="sidebar-status">
                <span class="{status_class}">
                    <span class="status-dot">{status_icon}</span>
                    {status_label}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---------------- STORAGE DETAILS ----------------
        with st.expander("Storage Details", expanded=False):
            st.caption(
                f"**Storage Engine:** "
                f"{'Supabase PostgreSQL' if is_cloud else 'Local SQLite (Persistent)'}"
            )
            st.caption(
                f"**Endpoint:** {status.get('url', 'finplot_local.db')}"
            )
            st.caption(status.get("message", ""))

            if not is_cloud:
                st.info(
                    "To connect to Supabase Cloud, add your "
                    "SUPABASE_URL and SUPABASE_KEY to the .env file "
                    "and run the SQL migration."
                )

        st.markdown('<div class="sidebar-divider"></div>',
                    unsafe_allow_html=True)

        # ---------------- NAVIGATION ----------------
        st.markdown(
            '<div class="sidebar-section-title">WORKSPACE</div>',
            unsafe_allow_html=True,
        )

        nav_choice = st.radio(
            "Go to",
            options=[
                "📊 Dashboard",
                "💳 Transactions",
                "📈 Reports (Phase 5)",
                "⚙️ Settings",
            ],
            label_visibility="collapsed",
        )

        st.markdown('<div class="sidebar-divider"></div>',
                    unsafe_allow_html=True)

        # ---------------- DEMO DATASET ----------------
        st.markdown(
            '<div class="sidebar-section-title">DATA MANAGEMENT</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="sidebar-description">
                Manage sample business transactions to explore
                financial insights and dashboard features.
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_load, col_clear = st.columns(2)

        with col_load:
            if st.button(
                "Load Demo",
                use_container_width=True,
                type="primary",
                help="Load sample business transactions",
            ):
                with st.spinner("Loading demo transactions..."):
                    count, errs = service.load_demo_dataset()

                    if count > 0:
                        st.success(f"Loaded {count} demo transactions!")
                        st.rerun()
                    else:
                        st.error("Failed to load demo data.")

        with col_clear:
            if st.button(
                "Clear Demo",
                use_container_width=True,
                type="secondary",
                help="Remove only demo transactions",
            ):
                with st.spinner("Removing demo transactions..."):
                    deleted_count = service.remove_demo_dataset()
                    st.info(f"Cleared {deleted_count} demo records.")
                    st.rerun()

        # ---------------- DATABASE STATISTICS ----------------
        # ---------------- DATABASE STATISTICS ----------------
                # ---------------- DATABASE STATISTICS ----------------
        stats = service.get_stats()

        stats_html = dedent(f"""
        <div class="sidebar-stats">
            <div class="sidebar-stats-heading">
                DATABASE OVERVIEW
            </div>

            <div class="sidebar-stat-row">
                <span>Total Records</span>
                <strong>{escape(str(stats['total']))}</strong>
            </div>

            <div class="sidebar-stat-row">
                <span>Live Records</span>
                <strong class="live-count">{escape(str(stats['real']))}</strong>
            </div>

            <div class="sidebar-stat-row">
                <span>Demo Records</span>
                <strong class="demo-count">{escape(str(stats['demo']))}</strong>
            </div>
        </div>
        """).strip()

        st.html(stats_html)

        # ---------------- FOOTER ----------------
        st.markdown(
            """
            <div class="sidebar-footer">
                <span>FinPlot AI</span>
                <span>VERSION 1.0</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        return nav_choice

def render_dashboard_page(service: TransactionService):
    """Renders the executive summary dashboard with KPIs, charts, and activity."""
    st.markdown(
        """
        <div class="section-header-box">
            <h1 class="section-title">📊 Executive Financial Dashboard</h1>
            <div class="section-subtitle">Real-time revenue, expense breakdown, and operating cash flow metrics.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Date range quick filter for dashboard
    col_filter1, col_filter2, col_filter3 = st.columns([1.5, 1.5, 1])
    with col_filter1:
        default_start = date.today() - timedelta(days=90)
        d_start = st.date_input("Start Date", value=default_start, key="dash_start_date")
    with col_filter2:
        d_end = st.date_input("End Date", value=date.today(), key="dash_end_date")
    with col_filter3:
        include_demo = st.checkbox("Include Demo Data", value=True, key="dash_inc_demo")

    # Fetch transactions matching date range
    transactions = service.list_transactions(
        start_date=d_start,
        end_date=d_end,
        include_demo=include_demo,
    )

    # Calculate deterministic metrics
    metrics = calculate_metrics(transactions)

    # 1. KPI Cards
    render_metric_cards(metrics)

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # 2. Charts Section
    chart_col1, chart_col2 = st.columns([1.6, 1.4])

    monthly_df = get_monthly_summary(transactions)
    category_df = get_category_summary(transactions, transaction_type="expense")

    with chart_col1:
        render_monthly_chart(monthly_df)

    with chart_col2:
        render_category_donut(category_df, transaction_type="expense")

    # 3. Cash Flow Trajectory
    trend_df = get_cumulative_cashflow(transactions)
    if not trend_df.empty:
        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
        render_cashflow_trend(trend_df)

    # 4. Recent Transactions Preview
    st.markdown("### 🕒 Recent Ledger Activity")
    recent = transactions[:8] if transactions else []
    if recent:
        render_transaction_table(service, recent)
    else:
        st.info("No recent transactions recorded in this date range. Click 'Load Demo' in the sidebar or add a transaction to begin.")


def render_transactions_page(service: TransactionService):
    """Renders the transactions management page with table search, CRUD forms, and CSV import."""
    st.markdown(
        """
        <div class="section-header-box">
            <h1 class="section-title">💳 Transactions Ledger</h1>
            <div class="section-subtitle">Manage, search, validate, and import business financial transactions.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_manage, tab_import = st.tabs(["📋 Ledger & Actions", "📥 Import Statements (CSV/Excel)"])

    # ---------------- TAB 1: Ledger & Actions ----------------
    with tab_manage:
        # Add Transaction Form Expander
        render_transaction_form(service)

        st.markdown("#### 🔍 Filter & Search Ledger")
        col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns([2, 1.2, 1.5, 1.2, 1])

        with col_s1:
            search_query = st.text_input(
                "Search",
                placeholder="Search description, payee, notes...",
                label_visibility="collapsed",
            )
        with col_s2:
            t_type = st.selectbox(
                "Type",
                options=["All Types", "Income", "Expense"],
                label_visibility="collapsed",
            )
        with col_s3:
            all_categories = ["All Categories"] + sorted(list(set(DEFAULT_INCOME_CATEGORIES + DEFAULT_EXPENSE_CATEGORIES)))
            cat_choice = st.selectbox(
                "Category",
                options=all_categories,
                label_visibility="collapsed",
            )
        with col_s4:
            days_range = st.selectbox(
                "Date Range",
                options=["Last 30 Days", "Last 90 Days", "Last 180 Days", "All Time"],
                index=1,
                label_visibility="collapsed",
            )
        with col_s5:
            show_demo = st.checkbox("Show Demo", value=True)

        # Compute date range
        start_date = None
        if days_range == "Last 30 Days":
            start_date = date.today() - timedelta(days=30)
        elif days_range == "Last 90 Days":
            start_date = date.today() - timedelta(days=90)
        elif days_range == "Last 180 Days":
            start_date = date.today() - timedelta(days=180)

        type_param = None
        if t_type == "Income":
            type_param = "income"
        elif t_type == "Expense":
            type_param = "expense"

        cat_param = None if cat_choice == "All Categories" else cat_choice

        filtered_transactions = service.list_transactions(
            search_query=search_query,
            transaction_type=type_param,
            category=cat_param,
            start_date=start_date,
            end_date=None,
            include_demo=show_demo,
        )

        # Render Transaction Table with Edit/Delete Actions
        render_transaction_table(service, filtered_transactions)

    # ---------------- TAB 2: Import Statements ----------------
    with tab_import:
        st.markdown("### 📥 Import Bank Statements or Accounting CSV")
        st.caption(
            "Upload `.csv` or `.xlsx` files. The system validates column mappings, checks each row for valid types and positive amounts, "
            "identifies duplicates against the database, and presents a full preview before persisting."
        )

        # Template Download
        template_csv = get_csv_template()
        st.download_button(
            label="📥 Download Sample CSV Template",
            data=template_csv,
            file_name="finplot_sample_transactions.csv",
            mime="text/csv",
            help="Download a formatted template with sample headers",
        )

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose a statement file",
            type=["csv", "xlsx", "xls"],
            help="Supported file types: CSV, Excel (.xlsx, .xls)",
        )

        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            # Fetch existing records to check for duplicates
            existing_all = service.list_transactions(include_demo=True)

            with st.spinner("Analyzing statement and validating transactions..."):
                parse_result = parse_and_validate_file(
                    file_bytes=file_bytes,
                    file_name=uploaded_file.name,
                    existing_transactions=existing_all,
                )

            if not parse_result.get("success", False):
                st.error(f"❌ {parse_result.get('error')}")
            else:
                valid_recs = parse_result["valid_records"]
                invalid_recs = parse_result["invalid_records"]
                dup_recs = parse_result["duplicate_records"]
                total_rows = parse_result["total_rows"]

                # Summary Statistics Cards
                st.markdown("#### 📊 Import Validation Summary")
                s1, s2, s3, s4 = st.columns(4)
                s1.metric("Total Rows in File", total_rows)
                s2.metric("Valid Rows", len(valid_recs))
                s3.metric("Duplicate Rows", len(dup_recs))
                s4.metric("Invalid Rows", len(invalid_recs))

                # If there are duplicates, give the user the option to include or skip
                skip_duplicates = st.checkbox(
                    f"Skip {len(dup_recs)} duplicate record{'s' if len(dup_recs) != 1 else ''} (prevent redundant entries)",
                    value=True,
                )

                records_to_import = list(valid_recs)
                if not skip_duplicates and dup_recs:
                    records_to_import.extend([d["record"] for d in dup_recs])

                # 1. Valid Records Preview
                if records_to_import:
                    st.markdown("##### ✅ Valid Records Ready for Import")
                    preview_data = [
                        {
                            "Date": r["transaction_date"],
                            "Description": r["description"],
                            "Amount": f"${r['amount']:,.2f}",
                            "Type": r["transaction_type"].capitalize(),
                            "Category": r["category"],
                            "Payment Method": r.get("payment_method") or "N/A",
                        }
                        for r in records_to_import[:15]
                    ]
                    st.dataframe(preview_data, use_container_width=True)
                    if len(records_to_import) > 15:
                        st.caption(f"... and {len(records_to_import) - 15} more rows.")

                # 2. Duplicate Records Reporting
                if dup_recs:
                    with st.expander(f"⚠️ View {len(dup_recs)} Detected Duplicates", expanded=False):
                        dup_preview = [
                            {
                                "Row #": d["row_number"],
                                "Date": d["record"]["transaction_date"],
                                "Description": d["record"]["description"],
                                "Amount": f"${d['record']['amount']:,.2f}",
                                "Reason": d["reason"],
                            }
                            for d in dup_recs
                        ]
                        st.dataframe(dup_preview, use_container_width=True)

                # 3. Invalid Records Reporting
                if invalid_recs:
                    with st.expander(f"❌ View {len(invalid_recs)} Invalid Rows with Errors", expanded=True):
                        st.error("The following rows contained validation errors and will NOT be imported:")
                        invalid_preview = [
                            {
                                "Row #": inv["row_number"],
                                "Values": str(inv["raw_data"]),
                                "Validation Errors": "; ".join(inv["errors"]),
                            }
                            for inv in invalid_recs
                        ]
                        st.dataframe(invalid_preview, use_container_width=True)

                # Commit Import Button
                st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                if records_to_import:
                    if st.button(
                        f"🚀 Confirm & Import {len(records_to_import)} Valid Record{'s' if len(records_to_import) != 1 else ''}",
                        type="primary",
                        key="btn_confirm_import",
                    ):
                        with st.spinner("Persisting records to database..."):
                            count, errs = service.bulk_import_records(records_to_import)
                            if count > 0:
                                st.success(f"🎉 Successfully imported {count} transactions!")
                                if errs:
                                    st.warning(f"Encountered issues on {len(errs)} rows: {errs[:3]}")
                                st.rerun()
                            else:
                                st.error("No records were saved. Please check the logs.")
                else:
                    st.warning("No valid transactions available to import from this file.")


def render_reports_page():
    """Placeholder for Phase 5 reporting module."""
    st.markdown(
        """
        <div class="section-header-box">
            <h1 class="section-title">📈 Financial Reports (Phase 5)</h1>
            <div class="section-subtitle">Financial statement exports, cash runway projections, and tax schedules.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="empty-state-box">
            <div class="empty-state-icon">📊</div>
            <div class="empty-state-title">Reporting Module Scheduled for Phase 5</div>
            <div class="empty-state-desc">
                Per the project implementation roadmap, comprehensive P&L statements,
                balance sheet estimation, and downloadable PDF reports will be activated in Phase 5.
                Currently active: <b>Phase 1 — Working Dashboard and Transaction Management</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_settings_page(status: dict):
    """Placeholder and configuration inspection page."""
    st.markdown(
        """
        <div class="section-header-box">
            <h1 class="section-title">⚙️ System Configuration & Database Setup</h1>
            <div class="section-subtitle">Diagnostics, environment parameters, and Supabase database connection details.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🔌 Database Connection Status")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Storage Engine:** `{status.get('mode')}`")
        st.write(f"**Connection Active:** `{status.get('is_connected')}`")
        st.write(f"**Target URL:** `{status.get('url')}`")
    with col2:
        st.write(f"**Status Message:** {status.get('message')}")
        if status.get("missing"):
            st.warning(f"Missing environment variables: {', '.join(status['missing'])}")

    st.markdown("---")
    st.markdown("### 🗄️ Supabase Cloud Migration Instructions")
    st.markdown(
        """
        To configure Supabase PostgreSQL as your persistent cloud database:
        
        1. **Create a Free Supabase Project**: Go to [supabase.com](https://supabase.com) and create an organization and project.
        2. **Run the SQL Migration**:
           - Open the Supabase dashboard -> **SQL Editor**.
           - Paste and execute the contents of `supabase/migrations/20260101_init_schema.sql`.
           - This creates the `transactions` table, performance indexes, and Row-Level Security (RLS) policies.
        3. **Copy Your API Keys**:
           - Go to **Project Settings** -> **API**.
           - Copy the `Project URL` and `anon public` key.
        4. **Update `.env`**:
           ```env
           SUPABASE_URL=https://your-project-ref.supabase.co
           SUPABASE_KEY=your-actual-anon-key-here
           ```
        5. **Restart Streamlit**:
           Restart the app; it will automatically connect to Supabase Cloud!
        """
    )


def main():
    """Main application controller."""
    apply_custom_css()
    service, status = initialize_app_services()

    # Render Sidebar and retrieve navigation route
    nav_choice = render_sidebar(service, status)

    # Route Page
    if nav_choice == "📊 Dashboard":
        render_dashboard_page(service)
    elif nav_choice == "💳 Transactions":
        render_transactions_page(service)
    elif nav_choice == "📈 Reports (Phase 5)":
        render_reports_page()
    elif nav_choice == "⚙️ Settings":
        render_settings_page(status)


if __name__ == "__main__":
    main()
