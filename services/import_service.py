"""
CSV and Excel import service for FinPlot AI.
Handles header mapping, row validation, preview generation,
duplicate transaction detection, and invalid row isolation.
"""

from datetime import date
import io
from typing import Any, Dict, List, Optional, Set, Tuple
import pandas as pd

from utils.validators import (
    parse_amount,
    parse_date,
    validate_transaction_payload,
)

# Standard template column headers
TEMPLATE_COLUMNS = [
    "transaction_date",
    "description",
    "amount",
    "transaction_type",
    "category",
    "payment_method",
    "notes",
]

# Canonical column mapping aliases
COLUMN_ALIASES: Dict[str, List[str]] = {
    "transaction_date": ["date", "transaction_date", "txn_date", "posted_date", "timestamp"],
    "description": ["description", "desc", "memo", "payee", "narration", "details", "title"],
    "amount": ["amount", "value", "amt", "total", "net_amount"],
    "transaction_type": ["transaction_type", "type", "txn_type", "direction", "kind"],
    "category": ["category", "cat", "classification", "expense_category", "tag"],
    "payment_method": ["payment_method", "method", "mode", "payment_mode", "account"],
    "notes": ["notes", "note", "comment", "remarks", "memo_2"],
}


def get_csv_template() -> str:
    """Returns standard sample CSV content for download."""
    return (
        "transaction_date,description,amount,transaction_type,category,payment_method,notes\n"
        "2026-03-15,Acme Client Retainer,4500.00,income,Consulting,Bank Transfer,Quarterly retainer\n"
        "2026-03-16,GitHub Team License,84.00,expense,Software & SaaS,Credit Card,Developer tooling\n"
        "2026-03-18,AWS Cloud Hosting,320.50,expense,Cloud & Infrastructure,Credit Card,EC2 and S3 billing\n"
    )


def map_columns(df_columns: List[str]) -> Tuple[Dict[str, str], List[str]]:
    """
    Maps incoming DataFrame column names to standard canonical field names.
    Returns:
        (canonical_to_source_mapping, missing_required_fields)
    """
    norm_to_original = {str(col).strip().lower(): col for col in df_columns}
    mapping: Dict[str, str] = {}

    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias.lower() in norm_to_original:
                mapping[canonical] = norm_to_original[alias.lower()]
                break

    # Required fields for any valid transaction
    required = ["transaction_date", "description", "amount", "transaction_type", "category"]
    missing = [req for req in required if req not in mapping]

    return mapping, missing


def build_duplicate_signature(t_date: str, desc: str, amount: float, t_type: str) -> str:
    """Creates a deterministic signature string to detect identical transactions."""
    return f"{t_date}|{desc.strip().lower()}|{round(amount, 2)}|{t_type.strip().lower()}"


def parse_and_validate_file(
    file_bytes: bytes,
    file_name: str,
    existing_transactions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Parses a CSV or Excel file, normalizes columns, validates rows,
    identifies duplicates against existing records, and returns preview structures.
    """
    # 1. Read into Pandas DataFrame
    try:
        if file_name.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
        else:
            df = pd.read_csv(io.BytesIO(file_bytes))
    except Exception as exc:
        return {
            "success": False,
            "error": f"Failed to parse file: {str(exc)}",
            "valid_records": [],
            "invalid_records": [],
            "duplicate_records": [],
            "total_rows": 0,
        }

    if df.empty:
        return {
            "success": False,
            "error": "The uploaded file is empty.",
            "valid_records": [],
            "invalid_records": [],
            "duplicate_records": [],
            "total_rows": 0,
        }

    # 2. Check and map column names
    col_mapping, missing_req = map_columns(list(df.columns))
    if missing_req:
        return {
            "success": False,
            "error": (
                f"Missing required columns in file: {', '.join(missing_req)}. "
                f"Found columns: {list(df.columns)}. "
                "Download the sample CSV template for the expected layout."
            ),
            "valid_records": [],
            "invalid_records": [],
            "duplicate_records": [],
            "total_rows": len(df),
        }

    # 3. Build existing duplicate signatures set
    existing_sigs: Set[str] = set()
    if existing_transactions:
        for ex in existing_transactions:
            dt_str = str(ex.get("transaction_date", ""))
            desc = str(ex.get("description", ""))
            amt = float(ex.get("amount", 0.0))
            typ = str(ex.get("transaction_type", ""))
            existing_sigs.add(build_duplicate_signature(dt_str, desc, amt, typ))

    valid_records: List[Dict[str, Any]] = []
    invalid_records: List[Dict[str, Any]] = []
    duplicate_records: List[Dict[str, Any]] = []
    seen_in_batch: Set[str] = set()

    # 4. Iterate over rows and validate
    for row_idx, row in df.iterrows():
        display_idx = int(row_idx) + 2  # 1-based, accounts for CSV header row

        # Extract values using mapped column names
        raw_date = row.get(col_mapping.get("transaction_date"))
        raw_desc = row.get(col_mapping.get("description"))
        raw_amt = row.get(col_mapping.get("amount"))
        raw_type = row.get(col_mapping.get("transaction_type"))
        raw_cat = row.get(col_mapping.get("category"))
        raw_pm = row.get(col_mapping.get("payment_method")) if "payment_method" in col_mapping else None
        raw_notes = row.get(col_mapping.get("notes")) if "notes" in col_mapping else None

        # Clean/parse values
        parsed_dt = parse_date(raw_date)
        parsed_amt = parse_amount(raw_amt)
        clean_desc = str(raw_desc).strip() if pd.notna(raw_desc) else ""
        clean_type = str(raw_type).strip().lower() if pd.notna(raw_type) else ""
        clean_cat = str(raw_cat).strip() if pd.notna(raw_cat) else ""
        clean_pm = str(raw_pm).strip() if pd.notna(raw_pm) else None
        clean_notes = str(raw_notes).strip() if pd.notna(raw_notes) else None

        # Build test payload for validation
        payload: Dict[str, Any] = {
            "transaction_date": parsed_dt.isoformat() if parsed_dt else str(raw_date),
            "description": clean_desc,
            "amount": parsed_amt if parsed_amt is not None else raw_amt,
            "transaction_type": clean_type,
            "category": clean_cat,
            "payment_method": clean_pm,
            "notes": clean_notes,
            "is_demo": False,
        }

        is_valid, validation_errors = validate_transaction_payload(payload)

        if not is_valid:
            invalid_records.append({
                "row_number": display_idx,
                "raw_data": {
                    "date": str(raw_date),
                    "description": clean_desc,
                    "amount": str(raw_amt),
                    "type": clean_type,
                    "category": clean_cat,
                },
                "errors": validation_errors,
            })
            continue

        # Check for duplicates (both against database and within this import batch)
        sig = build_duplicate_signature(
            payload["transaction_date"],
            payload["description"],
            float(payload["amount"]),
            payload["transaction_type"],
        )

        if sig in existing_sigs or sig in seen_in_batch:
            duplicate_records.append({
                "row_number": display_idx,
                "record": payload,
                "reason": "Exact match (date, description, amount, type) found in database or file.",
            })
            seen_in_batch.add(sig)
            continue

        seen_in_batch.add(sig)
        valid_records.append(payload)

    return {
        "success": True,
        "error": None,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "duplicate_records": duplicate_records,
        "total_rows": len(df),
    }
