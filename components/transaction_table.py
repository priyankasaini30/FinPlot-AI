"""
Filterable, searchable transactions table and action management component for FinPlot AI.
Features:
- Full-text search and multi-facet filtering (type, category, date range, demo data)
- Formatted tabular data display with badge indicators
- In-place row editing trigger
- Two-step confirmation modal/box before deletion
"""

from datetime import date
from typing import Any, Dict, List, Optional
import streamlit as st

from services.transaction_service import TransactionService
from components.transaction_form import render_transaction_form
from components.cards import format_currency


def render_transaction_table(
    service: TransactionService,
    transactions: List[Dict[str, Any]],
) -> None:
    """
    Renders the interactive transactions explorer:
    Filter bar, transactions table with badges, and Edit / Delete actions with confirmation.
    """
    if "editing_transaction_id" not in st.session_state:
        st.session_state["editing_transaction_id"] = None

    if "confirm_delete_id" not in st.session_state:
        st.session_state["confirm_delete_id"] = None

    # Handle Active Edit State
    if st.session_state["editing_transaction_id"]:
        tx_to_edit = service.get_transaction(st.session_state["editing_transaction_id"])
        if tx_to_edit:
            st.markdown("### ✏️ Editing Transaction")
            col_cancel, _ = st.columns([1, 5])
            with col_cancel:
                if st.button("← Cancel Edit", key="btn_cancel_edit"):
                    st.session_state["editing_transaction_id"] = None
                    st.rerun()

            def finish_edit():
                st.session_state["editing_transaction_id"] = None

            render_transaction_form(
                service,
                initial_data=tx_to_edit,
                on_success=finish_edit,
            )
            st.markdown("---")

    # Handle Active Delete Confirmation
    if st.session_state["confirm_delete_id"]:
        del_id = st.session_state["confirm_delete_id"]
        tx_to_del = service.get_transaction(del_id)
        if tx_to_del:
            st.warning(
                f"⚠️ **Confirm Deletion**: Are you sure you want to permanently delete "
                f"**{tx_to_del.get('description')}** ({format_currency(tx_to_del.get('amount', 0.0))})? "
                "This action cannot be undone."
            )
            c1, c2, _ = st.columns([1, 1, 4])
            with c1:
                if st.button("🗑️ Yes, Delete", type="primary", key="btn_confirm_delete"):
                    success, err = service.delete_transaction(del_id)
                    st.session_state["confirm_delete_id"] = None
                    if success:
                        st.success("Transaction successfully deleted.")
                        st.rerun()
                    else:
                        st.error(f"Failed to delete: {err}")
            with c2:
                if st.button("Cancel", key="btn_cancel_delete"):
                    st.session_state["confirm_delete_id"] = None
                    st.rerun()
            st.markdown("---")

    # Empty State Handling
    if not transactions:
        st.markdown(
            """
            <div class="empty-state-box">
                <div class="empty-state-icon">💳</div>
                <div class="empty-state-title">No Transactions Found</div>
                <div class="empty-state-desc">
                    Your ledger is currently empty for the selected filters.
                    Add a manual transaction above, import a CSV statement,
                    or load demo transactions from the sidebar.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Transactions Table Display Header
    st.markdown(
        f"<div style='margin-bottom: 0.6rem; color: #94a3b8; font-size: 0.85rem; font-weight: 500;'>"
        f"Showing <b>{len(transactions)}</b> transaction{'s' if len(transactions) != 1 else ''}"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Render Transaction Rows
    header_cols = st.columns([1.5, 3.2, 1.8, 1.4, 2.0, 1.2, 1.5])
    with header_cols[0]:
        st.caption("**DATE**")
    with header_cols[1]:
        st.caption("**DESCRIPTION**")
    with header_cols[2]:
        st.caption("**CATEGORY**")
    with header_cols[3]:
        st.caption("**TYPE**")
    with header_cols[4]:
        st.caption("**AMOUNT**")
    with header_cols[5]:
        st.caption("**TAG**")
    with header_cols[6]:
        st.caption("**ACTIONS**")

    st.divider()

    for tx in transactions:
        tx_id = str(tx.get("id"))
        t_date = str(tx.get("transaction_date", ""))
        desc = str(tx.get("description", ""))
        category = str(tx.get("category", ""))
        t_type = str(tx.get("transaction_type", "expense")).lower()
        amount = float(tx.get("amount", 0.0))
        is_demo = bool(tx.get("is_demo", False))
        pm = tx.get("payment_method") or "N/A"

        row_cols = st.columns([1.5, 3.2, 1.8, 1.4, 2.0, 1.2, 1.5])

        with row_cols[0]:
            st.write(t_date)

        with row_cols[1]:
            st.write(f"**{desc}**")
            if tx.get("notes"):
                st.caption(f"📝 {tx['notes']}")

        with row_cols[2]:
            st.write(category)

        with row_cols[3]:
            if t_type == "income":
                st.markdown(
                    "<span class='badge-income'>Income</span>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<span class='badge-expense'>Expense</span>",
                    unsafe_allow_html=True,
                )

        with row_cols[4]:
            amt_formatted = format_currency(amount)
            if t_type == "income":
                st.markdown(
                    f"<span style='color: #10b981; font-weight: 700;'>+{amt_formatted}</span>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<span style='color: #f43f5e; font-weight: 700;'>-{amt_formatted}</span>",
                    unsafe_allow_html=True,
                )

        with row_cols[5]:
            if is_demo:
                st.markdown(
                    "<span class='badge-demo'>Demo</span>",
                    unsafe_allow_html=True,
                )
            else:
                st.caption("Live")

        with row_cols[6]:
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("✏️", key=f"edit_btn_{tx_id}", help="Edit transaction"):
                    st.session_state["editing_transaction_id"] = tx_id
                    st.rerun()
            with act_col2:
                if st.button("🗑️", key=f"del_btn_{tx_id}", help="Delete transaction"):
                    st.session_state["confirm_delete_id"] = tx_id
                    st.rerun()

        st.divider()
