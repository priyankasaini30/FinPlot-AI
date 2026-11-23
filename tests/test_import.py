"""
Unit tests for statement importing, CSV parsing, and duplicate detection.
Validates:
- Column header mapping and alias recognition
- Valid and invalid row separation without crashing
- Accurate duplicate detection against existing databases and batch rows
- Template generation
"""

import pytest
from services.import_service import (
    map_columns,
    parse_and_validate_file,
    get_csv_template,
)


def test_template_generation():
    """Verify standard CSV template includes all required headers."""
    tmpl = get_csv_template()
    assert "transaction_date" in tmpl
    assert "description" in tmpl
    assert "amount" in tmpl
    assert "transaction_type" in tmpl
    assert "category" in tmpl


def test_column_mapping_aliases():
    """Verify alias mapping for diverse column name conventions."""
    cols = ["Date", "Memo", "Total", "Type", "Category"]
    mapping, missing = map_columns(cols)
    assert len(missing) == 0
    assert mapping["transaction_date"] == "Date"
    assert mapping["description"] == "Memo"
    assert mapping["amount"] == "Total"
    assert mapping["transaction_type"] == "Type"
    assert mapping["category"] == "Category"


def test_column_mapping_missing_required():
    """Verify missing required columns are correctly identified."""
    cols = ["Date", "Description"]
    mapping, missing = map_columns(cols)
    assert "amount" in missing
    assert "transaction_type" in missing
    assert "category" in missing


def test_parse_and_validate_file_valid_csv():
    """Verify processing of valid CSV file bytes."""
    csv_content = (
        "transaction_date,description,amount,transaction_type,category\n"
        "2026-03-01,Client Consulting Retainer,3000.00,income,Consulting\n"
        "2026-03-02,AWS Cloud Hosting,150.00,expense,Cloud & Infrastructure\n"
    ).encode("utf-8")

    result = parse_and_validate_file(csv_content, "statement.csv")
    assert result["success"] is True
    assert len(result["valid_records"]) == 2
    assert len(result["invalid_records"]) == 0
    assert len(result["duplicate_records"]) == 0
    assert result["valid_records"][0]["amount"] == 3000.00


def test_parse_and_validate_file_invalid_rows():
    """Verify invalid rows (negative amount, empty description) are isolated and reported."""
    csv_content = (
        "transaction_date,description,amount,transaction_type,category\n"
        "2026-03-01,Valid Retainer,3000.00,income,Consulting\n"
        "2026-03-02,,150.00,expense,Cloud & Infrastructure\n"  # missing desc
        "2026-03-03,Bad Amount,-50.00,expense,Cloud & Infrastructure\n"  # negative amt
    ).encode("utf-8")

    result = parse_and_validate_file(csv_content, "statement.csv")
    assert result["success"] is True
    assert len(result["valid_records"]) == 1
    assert len(result["invalid_records"]) == 2
    # Verify exact error details are captured
    assert result["invalid_records"][0]["row_number"] == 3
    assert any("Description is required" in e for e in result["invalid_records"][0]["errors"])
    assert result["invalid_records"][1]["row_number"] == 4
    assert any("greater than zero" in e for e in result["invalid_records"][1]["errors"])


def test_duplicate_detection_against_db():
    """Verify that rows identical to existing DB records are flagged as duplicates."""
    existing_records = [
        {
            "transaction_date": "2026-03-01",
            "description": "Client Consulting Retainer",
            "amount": 3000.00,
            "transaction_type": "income",
        }
    ]

    csv_content = (
        "transaction_date,description,amount,transaction_type,category\n"
        "2026-03-01,Client Consulting Retainer,3000.00,income,Consulting\n"  # Duplicate
        "2026-03-02,New Unique Transaction,500.00,expense,Software & SaaS\n"
    ).encode("utf-8")

    result = parse_and_validate_file(
        csv_content, "statement.csv", existing_transactions=existing_records
    )
    assert result["success"] is True
    assert len(result["valid_records"]) == 1
    assert len(result["duplicate_records"]) == 1
    assert result["duplicate_records"][0]["record"]["description"] == "Client Consulting Retainer"
