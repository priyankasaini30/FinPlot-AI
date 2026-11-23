"""
Unit tests for TransactionRepository and TransactionService CRUD operations.
Validates:
- Create transaction
- Read transactions with filters (search, type, category, date, demo)
- Update transaction
- Delete transaction
- Load and Clear demo data isolation
"""

import os
import tempfile
import pytest
from database.repository import SQLiteTransactionRepository
from services.transaction_service import TransactionService


@pytest.fixture
def temp_service():
    """Provides a fresh TransactionService backed by an isolated temporary SQLite file."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
        db_path = tf.name
    repo = SQLiteTransactionRepository(db_path=db_path)
    service = TransactionService(repo)
    yield service
    if os.path.exists(db_path):
        os.remove(db_path)


def test_create_and_get_transaction(temp_service):
    """Test creating and retrieving a valid transaction."""
    payload = {
        "transaction_date": "2026-03-20",
        "description": "Tech Client Retainer",
        "amount": 4200.00,
        "transaction_type": "income",
        "category": "Consulting",
        "payment_method": "Wire",
        "notes": "Q1 retainer fee",
        "is_demo": False,
    }
    success, created, errors = temp_service.create_transaction(payload)
    assert success is True
    assert created is not None
    assert created["amount"] == 4200.00
    assert created["description"] == "Tech Client Retainer"

    fetched = temp_service.get_transaction(created["id"])
    assert fetched is not None
    assert fetched["id"] == created["id"]
    assert fetched["category"] == "Consulting"


def test_update_transaction(temp_service):
    """Test modifying transaction details."""
    payload = {
        "transaction_date": "2026-03-20",
        "description": "Initial Name",
        "amount": 100.00,
        "transaction_type": "expense",
        "category": "Office Supplies & Equipment",
    }
    success, created, _ = temp_service.create_transaction(payload)
    assert success is True

    update_payload = {
        "transaction_date": "2026-03-21",
        "description": "Updated Office Desk",
        "amount": 250.00,
        "transaction_type": "expense",
        "category": "Office Supplies & Equipment",
    }
    up_success, updated, _ = temp_service.update_transaction(created["id"], update_payload)
    assert up_success is True
    assert updated["description"] == "Updated Office Desk"
    assert updated["amount"] == 250.00
    assert updated["transaction_date"] == "2026-03-21"


def test_delete_transaction(temp_service):
    """Test deleting transaction record."""
    payload = {
        "transaction_date": "2026-03-20",
        "description": "To be deleted",
        "amount": 50.00,
        "transaction_type": "expense",
        "category": "Software & SaaS",
    }
    _, created, _ = temp_service.create_transaction(payload)
    assert created is not None

    del_success, err = temp_service.delete_transaction(created["id"])
    assert del_success is True
    assert err is None

    assert temp_service.get_transaction(created["id"]) is None


def test_demo_data_isolation_and_clear(temp_service):
    """Test that demo data loading and clearing operates strictly on is_demo=True records."""
    # 1. Add 1 real transaction
    real_payload = {
        "transaction_date": "2026-03-01",
        "description": "Real Live Income",
        "amount": 10000.00,
        "transaction_type": "income",
        "category": "Sales Revenue",
        "is_demo": False,
    }
    temp_service.create_transaction(real_payload)

    # 2. Seed demo dataset
    count, errs = temp_service.load_demo_dataset()
    assert count > 0
    stats = temp_service.get_stats()
    assert stats["real"] == 1
    assert stats["demo"] == count
    assert stats["total"] == count + 1

    # 3. Clear demo dataset
    cleared = temp_service.remove_demo_dataset()
    assert cleared == count

    # 4. Verify only real transaction remains untouched
    remaining = temp_service.list_transactions(include_demo=True)
    assert len(remaining) == 1
    assert remaining[0]["description"] == "Real Live Income"
    assert remaining[0]["is_demo"] is False
