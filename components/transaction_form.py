"""
Transaction creation and editing form component for FinPlot AI.
Provides clean inputs, dynamic category selection based on type,
real-time input validation, and feedback messages.
"""

from datetime import date
from typing import Any, Callable, Dict, Optional
import streamlit as st

from services.transaction_service import TransactionService
from utils.validators import (
    DEFAULT_INCOME_CATEGORIES,
    DEFAULT_EXPENSE_CATEGORIES,
    VALID_PAYMENT_METHODS,
    parse_date,
)


def render_transaction_form(
    service: TransactionService,
    initial_data: Optional[Dict[str, Any]] = None,
    on_success: Optional[Callable[[], None]] = None,
) -> None:
    """
    Renders an Add / Edit transaction form.
    If initial_data is provided, operates in Edit mode; otherwise in Create mode.
    """
    is_edit = initial_data is not None
    form_title = "✏️ Edit Transaction" if is_edit else "➕ Add New Transaction"

    with st.expander(form_title, expanded=is_edit):
        form_key = f"tx_form_{'edit_' + str(initial_data.get('id')) if is_edit else 'create'}"

        with st.form(key=form_key, clear_on_submit=not is_edit):
            # Row 1: Type & Date
            col1, col2 = st.columns([1, 1])

            existing_type = (
                str(initial_data.get("transaction_type", "expense")).lower()
                if is_edit
                else "expense"
            )
            type_options = ["expense", "income"]
            type_index = (
                type_options.index(existing_type)
                if existing_type in type_options
                else 0
            )

            with col1:
                selected_type = st.radio(
                    "Transaction Type *",
                    options=type_options,
                    index=type_index,
                    format_func=lambda x: "🔴 Expense" if x == "expense" else "🟢 Income",
                    horizontal=True,
                )

            with col2:
                default_date = date.today()
                if is_edit and initial_data.get("transaction_date"):
                    parsed_d = parse_date(initial_data["transaction_date"])
                    if parsed_d:
                        default_date = parsed_d

                selected_date = st.date_input(
                    "Transaction Date *",
                    value=default_date,
                    help="Calendar date when transaction occurred",
                )

            # Row 2: Description & Amount
            col3, col4 = st.columns([2, 1])

            with col3:
                desc_val = str(initial_data.get("description", "")) if is_edit else ""
                description = st.text_input(
                    "Description / Payee *",
                    value=desc_val,
                    placeholder="e.g. Acme Corp Retainer or AWS Cloud Billing",
                )

            with col4:
                amt_val = float(initial_data.get("amount", 100.00)) if is_edit else 100.00
                amount = st.number_input(
                    "Amount ($) *",
                    min_value=0.01,
                    max_value=1_000_000_000.00,
                    value=amt_val,
                    step=10.00,
                    format="%.2f",
                    help="Amount must be positive; transaction type dictates direction",
                )

            # Row 3: Category & Payment Method
            col5, col6 = st.columns([1, 1])

            category_list = (
                DEFAULT_EXPENSE_CATEGORIES
                if selected_type == "expense"
                else DEFAULT_INCOME_CATEGORIES
            )

            existing_cat = (
                str(initial_data.get("category", category_list[0]))
                if is_edit
                else category_list[0]
            )
            cat_options = list(category_list)
            if existing_cat not in cat_options:
                cat_options.append(existing_cat)
            cat_options.append("Other (Custom...)")

            cat_index = (
                cat_options.index(existing_cat)
                if existing_cat in cat_options
                else 0
            )

            with col5:
                selected_cat = st.selectbox(
                    "Category *",
                    options=cat_options,
                    index=cat_index,
                )
                custom_cat = ""
                if selected_cat == "Other (Custom...)":
                    custom_cat = st.text_input(
                        "Specify Custom Category *",
                        placeholder="e.g. Conference Ticket",
                    )

            with col6:
                existing_pm = (
                    str(initial_data.get("payment_method", "Bank Transfer"))
                    if is_edit
                    else "Bank Transfer"
                )
                pm_options = list(VALID_PAYMENT_METHODS)
                pm_index = (
                    pm_options.index(existing_pm)
                    if existing_pm in pm_options
                    else 0
                )
                payment_method = st.selectbox(
                    "Payment Method (Optional)",
                    options=pm_options,
                    index=pm_index,
                )

            # Row 4: Notes
            notes_val = str(initial_data.get("notes") or "") if is_edit else ""
            notes = st.text_area(
                "Notes & Reconciliation Memo (Optional)",
                value=notes_val,
                placeholder="Additional details, invoice references, tax codes...",
                height=70,
            )

            # Action Buttons
            submit_label = "💾 Save Changes" if is_edit else "➕ Add Transaction"
            submitted = st.form_submit_button(
                label=submit_label,
                use_container_width=True,
                type="primary",
            )

            if submitted:
                final_category = (
                    custom_cat.strip()
                    if selected_cat == "Other (Custom...)"
                    else selected_cat
                )

                payload: Dict[str, Any] = {
                    "transaction_date": selected_date.isoformat(),
                    "description": description.strip(),
                    "amount": float(amount),
                    "transaction_type": selected_type,
                    "category": final_category,
                    "payment_method": payment_method,
                    "notes": notes.strip() if notes.strip() else None,
                    "is_demo": False,
                }

                if is_edit:
                    tx_id = str(initial_data["id"])
                    success, updated_rec, errors = service.update_transaction(
                        tx_id, payload
                    )
                    if success:
                        st.success(
                            f"✅ Successfully updated transaction '{description}'!"
                        )
                        if on_success:
                            on_success()
                        st.rerun()
                    else:
                        for err in errors:
                            st.error(f"❌ {err}")
                else:
                    success, created_rec, errors = service.create_transaction(payload)
                    if success:
                        st.success(
                            f"✅ Successfully added transaction '{description}' for ${amount:,.2f}!"
                        )
                        if on_success:
                            on_success()
                        st.rerun()
                    else:
                        for err in errors:
                            st.error(f"❌ {err}")
