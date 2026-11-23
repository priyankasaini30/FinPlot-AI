"""
Input validation and parsing utilities for FinPlot AI.
Ensures financial integrity, valid types, positive amounts, and clean input data.
"""

from datetime import date, datetime
import re
import math
from typing import Any, Dict, List, Optional, Tuple

VALID_TRANSACTION_TYPES = ("income", "expense")

DEFAULT_INCOME_CATEGORIES = [
    "Sales Revenue",
    "Client Invoicing",
    "Consulting",
    "Investment Return",
    "Affiliate / Commission",
    "Grants & Funding",
    "Other Income",
]

DEFAULT_EXPENSE_CATEGORIES = [
    "Software & SaaS",
    "Cloud & Infrastructure",
    "Salaries & Contractor",
    "Marketing & Advertising",
    "Office Supplies & Equipment",
    "Legal & Accounting",
    "Travel & Entertainment",
    "Rent & Real Estate",
    "Utilities & Internet",
    "Banking & Payment Fees",
    "Taxes & Licenses",
    "Miscellaneous Expense",
]

VALID_PAYMENT_METHODS = [
    "Bank Transfer",
    "Credit Card",
    "Debit Card",
    "Stripe",
    "PayPal",
    "Cash",
    "Wire",
    "Other",
]


def parse_amount(val: Any) -> Optional[float]:
    """
    Safely parse monetary amount into a positive float.
    Strips currency signs, commas, and whitespace.
    Returns None if parsing fails, is NaN/Inf, or amount is non-numeric.
    """
    if val is None:
        return None
    if isinstance(val, (int, float)):
        f_val = float(val)
        if math.isnan(f_val) or math.isinf(f_val):
            return None
        return f_val

    s = str(val).strip()
    # Remove currency symbols and common delimiters
    s = re.sub(r"[$\s,€£₹]", "", s)
    try:
        parsed = float(s)
        if math.isnan(parsed) or math.isinf(parsed):
            return None
        return parsed
    except (ValueError, TypeError):
        return None


def parse_date(val: Any) -> Optional[date]:
    """
    Safely parses various date inputs into a python datetime.date.
    Supported: date, datetime, ISO string (YYYY-MM-DD), MM/DD/YYYY, DD-MM-YYYY.
    """
    if val is None:
        return None
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, date):
        return val

    s = str(val).strip()
    if not s:
        return None

    # Common date formats
    date_formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%b %d, %Y",
        "%d %b %Y",
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue

    return None


def validate_transaction_payload(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate transaction fields strictly.
    Returns (is_valid, list_of_error_messages).
    """
    errors: List[str] = []

    # 1. Description
    desc = payload.get("description")
    if not desc or not str(desc).strip():
        errors.append("Description is required and cannot be empty.")
    elif len(str(desc).strip()) > 255:
        errors.append("Description must not exceed 255 characters.")

    # 2. Amount
    raw_amount = payload.get("amount")
    parsed_amount = parse_amount(raw_amount)
    if parsed_amount is None:
        errors.append(f"Amount '{raw_amount}' is not a valid number.")
    elif parsed_amount <= 0:
        errors.append("Amount must be strictly greater than zero (> $0.00).")
    elif parsed_amount > 1_000_000_000:
        errors.append("Amount exceeds supported threshold ($1,000,000,000).")

    # 3. Transaction Type
    t_type = str(payload.get("transaction_type", "")).strip().lower()
    if t_type not in VALID_TRANSACTION_TYPES:
        errors.append(
            f"Transaction type must be one of {VALID_TRANSACTION_TYPES}. Received: '{t_type}'."
        )

    # 4. Category
    category = payload.get("category")
    if not category or not str(category).strip():
        errors.append("Category is required.")

    # 5. Transaction Date
    raw_date = payload.get("transaction_date")
    parsed_dt = parse_date(raw_date)
    if parsed_dt is None:
        errors.append(f"Invalid transaction date: '{raw_date}'.")

    # 6. Payment method (optional, max 50 chars)
    pm = payload.get("payment_method")
    if pm and len(str(pm).strip()) > 50:
        errors.append("Payment method cannot exceed 50 characters.")

    # 7. Notes (optional, max 1000 chars)
    notes = payload.get("notes")
    if notes and len(str(notes).strip()) > 1000:
        errors.append("Notes cannot exceed 1000 characters.")

    return len(errors) == 0, errors
