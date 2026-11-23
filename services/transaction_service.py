"""
Transaction management service orchestrator for FinPlot AI.
Coordinates CRUD validation, business rules, demo data seeding, and storage access.
"""

from datetime import date
from typing import Any, Dict, List, Optional, Tuple

from database.repository import BaseRepository
from utils.validators import validate_transaction_payload
from utils.sample_data import get_demo_transactions


class TransactionService:
    """Service handling transaction business logic, validation, and repository persistence."""

    def __init__(self, repository: BaseRepository):
        self.repo = repository

    def list_transactions(
        self,
        search_query: Optional[str] = None,
        transaction_type: Optional[str] = None,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        include_demo: bool = True,
    ) -> List[Dict[str, Any]]:
        return self.repo.get_all(
            search_query=search_query,
            transaction_type=transaction_type,
            category=category,
            start_date=start_date,
            end_date=end_date,
            include_demo=include_demo,
        )

    def get_transaction(self, tx_id: str) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_id(tx_id)

    def create_transaction(self, data: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]], List[str]]:
        """
        Validates and creates a new transaction.
        Returns (success, created_record_or_None, list_of_errors).
        """
        is_valid, errors = validate_transaction_payload(data)
        if not is_valid:
            return False, None, errors

        try:
            record = self.repo.create(data)
            return True, record, []
        except Exception as exc:
            return False, None, [f"Database error while saving transaction: {str(exc)}"]

    def update_transaction(
        self, tx_id: str, data: Dict[str, Any]
    ) -> Tuple[bool, Optional[Dict[str, Any]], List[str]]:
        """
        Validates and updates an existing transaction.
        Returns (success, updated_record_or_None, list_of_errors).
        """
        is_valid, errors = validate_transaction_payload(data)
        if not is_valid:
            return False, None, errors

        try:
            record = self.repo.update(tx_id, data)
            return True, record, []
        except Exception as exc:
            return False, None, [f"Database error while updating transaction: {str(exc)}"]

    def delete_transaction(self, tx_id: str) -> Tuple[bool, Optional[str]]:
        """Deletes a transaction by ID. Returns (success, error_message_or_None)."""
        try:
            success = self.repo.delete(tx_id)
            if not success:
                return False, f"Transaction '{tx_id}' was not found or could not be removed."
            return True, None
        except Exception as exc:
            return False, f"Database deletion failed: {str(exc)}"

    def load_demo_dataset(self) -> Tuple[int, List[str]]:
        """Seeds curated demo transactions with is_demo = True."""
        sample_records = get_demo_transactions()
        return self.repo.bulk_create(sample_records)

    def remove_demo_dataset(self) -> int:
        """Removes only records marked is_demo = True, safeguarding live records."""
        return self.repo.clear_demo_data()

    def bulk_import_records(self, records: List[Dict[str, Any]]) -> Tuple[int, List[str]]:
        """Persists imported and validated transactions."""
        return self.repo.bulk_create(records)

    def get_stats(self) -> Dict[str, int]:
        return self.repo.get_stats()
