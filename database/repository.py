"""
Data repository layer for FinPlot AI transactions.
Provides unified CRUD operations across Supabase PostgreSQL (Cloud)
and an isolated local SQLite storage engine (for offline/demo mode without credentials).
Guarantees persistent storage, reliable error reporting, and no fabricated operations.
"""

from contextlib import contextmanager
from datetime import datetime, date
import os
import sqlite3
from typing import Any, Dict, List, Optional, Tuple
import uuid

from .connection import get_supabase_client, check_supabase_configuration


class BaseRepository:
    """Abstract interface defining the contract for transaction storage."""

    def get_all(
        self,
        search_query: Optional[str] = None,
        transaction_type: Optional[str] = None,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        include_demo: bool = True,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def get_by_id(self, tx_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def update(self, tx_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def delete(self, tx_id: str) -> bool:
        raise NotImplementedError

    def bulk_create(self, records: List[Dict[str, Any]]) -> Tuple[int, List[str]]:
        raise NotImplementedError

    def clear_demo_data(self) -> int:
        raise NotImplementedError

    def get_stats(self) -> Dict[str, int]:
        raise NotImplementedError


class SQLiteTransactionRepository(BaseRepository):
    """
    Local SQLite persistent repository.
    Used when Supabase credentials are not configured or when running offline.
    Never fabricates cloud sync; transparently manages a local SQLite file.
    """

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            # Default to workspace root database
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(base_dir, "finplot_local.db")
        else:
            self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Initializes SQLite tables matching the Supabase schema structure."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    transaction_date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount > 0),
                    transaction_type TEXT NOT NULL CHECK(transaction_type IN ('income', 'expense')),
                    category TEXT NOT NULL,
                    payment_method TEXT,
                    notes TEXT,
                    is_demo INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            # Create indexes
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_tx_date ON transactions(transaction_date DESC)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_tx_cat ON transactions(category)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_tx_demo ON transactions(is_demo)"
            )
            conn.commit()

    def get_all(
        self,
        search_query: Optional[str] = None,
        transaction_type: Optional[str] = None,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        include_demo: bool = True,
    ) -> List[Dict[str, Any]]:
        query = "SELECT * FROM transactions WHERE 1=1"
        params: List[Any] = []

        if not include_demo:
            query += " AND is_demo = 0"

        if transaction_type and transaction_type.lower() in ("income", "expense"):
            query += " AND transaction_type = ?"
            params.append(transaction_type.lower())

        if category and category != "All":
            query += " AND category = ?"
            params.append(category)

        if start_date:
            query += " AND transaction_date >= ?"
            params.append(start_date.isoformat())

        if end_date:
            query += " AND transaction_date <= ?"
            params.append(end_date.isoformat())

        if search_query and search_query.strip():
            sq = f"%{search_query.strip()}%"
            query += " AND (description LIKE ? OR notes LIKE ? OR category LIKE ? OR payment_method LIKE ?)"
            params.extend([sq, sq, sq, sq])

        query += " ORDER BY transaction_date DESC, created_at DESC"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [
                {
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "transaction_date": row["transaction_date"],
                    "description": row["description"],
                    "amount": float(row["amount"]),
                    "transaction_type": row["transaction_type"],
                    "category": row["category"],
                    "payment_method": row["payment_method"],
                    "notes": row["notes"],
                    "is_demo": bool(row["is_demo"]),
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }
                for row in rows
            ]

    def get_by_id(self, tx_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE id = ?", (tx_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                "id": row["id"],
                "user_id": row["user_id"],
                "transaction_date": row["transaction_date"],
                "description": row["description"],
                "amount": float(row["amount"]),
                "transaction_type": row["transaction_type"],
                "category": row["category"],
                "payment_method": row["payment_method"],
                "notes": row["notes"],
                "is_demo": bool(row["is_demo"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        tx_id = data.get("id") or str(uuid.uuid4())
        now_iso = datetime.now().isoformat()
        t_date = data["transaction_date"]
        if isinstance(t_date, (date, datetime)):
            t_date = t_date.isoformat()

        record = {
            "id": tx_id,
            "user_id": data.get("user_id"),
            "transaction_date": str(t_date),
            "description": str(data["description"]).strip(),
            "amount": float(data["amount"]),
            "transaction_type": str(data["transaction_type"]).strip().lower(),
            "category": str(data["category"]).strip(),
            "payment_method": data.get("payment_method"),
            "notes": data.get("notes"),
            "is_demo": 1 if data.get("is_demo", False) else 0,
            "created_at": data.get("created_at") or now_iso,
            "updated_at": now_iso,
        }

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO transactions (
                    id, user_id, transaction_date, description, amount,
                    transaction_type, category, payment_method, notes,
                    is_demo, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record["id"],
                    record["user_id"],
                    record["transaction_date"],
                    record["description"],
                    record["amount"],
                    record["transaction_type"],
                    record["category"],
                    record["payment_method"],
                    record["notes"],
                    record["is_demo"],
                    record["created_at"],
                    record["updated_at"],
                ),
            )
            conn.commit()

        record["is_demo"] = bool(record["is_demo"])
        return record

    def update(self, tx_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        existing = self.get_by_id(tx_id)
        if not existing:
            raise ValueError(f"Transaction with ID '{tx_id}' not found.")

        now_iso = datetime.now().isoformat()
        t_date = data.get("transaction_date", existing["transaction_date"])
        if isinstance(t_date, (date, datetime)):
            t_date = t_date.isoformat()

        updated_record = {
            "transaction_date": str(t_date),
            "description": str(
                data.get("description", existing["description"])
            ).strip(),
            "amount": float(data.get("amount", existing["amount"])),
            "transaction_type": str(
                data.get("transaction_type", existing["transaction_type"])
            )
            .strip()
            .lower(),
            "category": str(data.get("category", existing["category"])).strip(),
            "payment_method": data.get("payment_method", existing["payment_method"]),
            "notes": data.get("notes", existing["notes"]),
            "updated_at": now_iso,
        }

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE transactions SET
                    transaction_date = ?,
                    description = ?,
                    amount = ?,
                    transaction_type = ?,
                    category = ?,
                    payment_method = ?,
                    notes = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    updated_record["transaction_date"],
                    updated_record["description"],
                    updated_record["amount"],
                    updated_record["transaction_type"],
                    updated_record["category"],
                    updated_record["payment_method"],
                    updated_record["notes"],
                    updated_record["updated_at"],
                    tx_id,
                ),
            )
            conn.commit()

        return self.get_by_id(tx_id)  # type: ignore

    def delete(self, tx_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
            conn.commit()
            return cursor.rowcount > 0

    def bulk_create(self, records: List[Dict[str, Any]]) -> Tuple[int, List[str]]:
        success_count = 0
        errors: List[str] = []
        for idx, rec in enumerate(records, start=1):
            try:
                self.create(rec)
                success_count += 1
            except Exception as e:
                errors.append(f"Row {idx} failed: {str(e)}")
        return success_count, errors

    def clear_demo_data(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE is_demo = 1")
            conn.commit()
            return cursor.rowcount

    def get_stats(self) -> Dict[str, int]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM transactions")
            total = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM transactions WHERE is_demo = 1")
            demo = cursor.fetchone()[0]
            return {
                "total": total,
                "real": total - demo,
                "demo": demo,
            }


class SupabaseTransactionRepository(BaseRepository):
    """
    Cloud persistent repository communicating with Supabase PostgreSQL
    via Supabase client and Row-Level Security policies.
    """

    def __init__(self, client: Any):
        self.client = client
        self.table_name = "transactions"

    def get_all(
        self,
        search_query: Optional[str] = None,
        transaction_type: Optional[str] = None,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        include_demo: bool = True,
    ) -> List[Dict[str, Any]]:
        query = self.client.table(self.table_name).select("*")

        if not include_demo:
            query = query.eq("is_demo", False)

        if transaction_type and transaction_type.lower() in ("income", "expense"):
            query = query.eq("transaction_type", transaction_type.lower())

        if category and category != "All":
            query = query.eq("category", category)

        if start_date:
            query = query.gte("transaction_date", start_date.isoformat())

        if end_date:
            query = query.lte("transaction_date", end_date.isoformat())

        # PostgREST query execution
        response = query.order("transaction_date", desc=True).execute()
        rows = response.data or []

        # Client-side text filter if search query provided
        if search_query and search_query.strip():
            sq = search_query.strip().lower()
            filtered = []
            for r in rows:
                desc = str(r.get("description") or "").lower()
                notes = str(r.get("notes") or "").lower()
                cat = str(r.get("category") or "").lower()
                pm = str(r.get("payment_method") or "").lower()
                if sq in desc or sq in notes or sq in cat or sq in pm:
                    filtered.append(r)
            rows = filtered

        # Normalize amount to float
        for r in rows:
            r["amount"] = float(r["amount"])
            r["is_demo"] = bool(r.get("is_demo", False))

        return rows

    def get_by_id(self, tx_id: str) -> Optional[Dict[str, Any]]:
        response = (
            self.client.table(self.table_name).select("*").eq("id", tx_id).execute()
        )
        if response.data and len(response.data) > 0:
            rec = response.data[0]
            rec["amount"] = float(rec["amount"])
            rec["is_demo"] = bool(rec.get("is_demo", False))
            return rec
        return None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        t_date = data["transaction_date"]
        if isinstance(t_date, (date, datetime)):
            t_date = t_date.isoformat()

        payload = {
            "description": str(data["description"]).strip(),
            "amount": float(data["amount"]),
            "transaction_type": str(data["transaction_type"]).strip().lower(),
            "category": str(data["category"]).strip(),
            "payment_method": data.get("payment_method"),
            "notes": data.get("notes"),
            "transaction_date": str(t_date),
            "is_demo": bool(data.get("is_demo", False)),
        }
        if data.get("id"):
            payload["id"] = data["id"]
        if data.get("user_id"):
            payload["user_id"] = data["user_id"]

        response = self.client.table(self.table_name).insert(payload).execute()
        if response.data and len(response.data) > 0:
            rec = response.data[0]
            rec["amount"] = float(rec["amount"])
            return rec
        raise RuntimeError(
            "Supabase insert failed: No record returned from database."
        )

    def update(self, tx_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        if "description" in data:
            payload["description"] = str(data["description"]).strip()
        if "amount" in data:
            payload["amount"] = float(data["amount"])
        if "transaction_type" in data:
            payload["transaction_type"] = (
                str(data["transaction_type"]).strip().lower()
            )
        if "category" in data:
            payload["category"] = str(data["category"]).strip()
        if "payment_method" in data:
            payload["payment_method"] = data["payment_method"]
        if "notes" in data:
            payload["notes"] = data["notes"]
        if "transaction_date" in data:
            t_date = data["transaction_date"]
            if isinstance(t_date, (date, datetime)):
                t_date = t_date.isoformat()
            payload["transaction_date"] = str(t_date)

        response = (
            self.client.table(self.table_name)
            .update(payload)
            .eq("id", tx_id)
            .execute()
        )
        if response.data and len(response.data) > 0:
            rec = response.data[0]
            rec["amount"] = float(rec["amount"])
            return rec
        raise RuntimeError(f"Failed to update transaction {tx_id} in Supabase.")

    def delete(self, tx_id: str) -> bool:
        response = (
            self.client.table(self.table_name).delete().eq("id", tx_id).execute()
        )
        return bool(response.data)

    def bulk_create(self, records: List[Dict[str, Any]]) -> Tuple[int, List[str]]:
        success_count = 0
        errors: List[str] = []
        for idx, rec in enumerate(records, start=1):
            try:
                self.create(rec)
                success_count += 1
            except Exception as e:
                errors.append(f"Row {idx} failed: {str(e)}")
        return success_count, errors

    def clear_demo_data(self) -> int:
        response = (
            self.client.table(self.table_name)
            .delete()
            .eq("is_demo", True)
            .execute()
        )
        return len(response.data) if response.data else 0

    def get_stats(self) -> Dict[str, int]:
        all_data = (
            self.client.table(self.table_name).select("id, is_demo").execute().data
            or []
        )
        total = len(all_data)
        demo = sum(1 for r in all_data if r.get("is_demo") is True)
        return {
            "total": total,
            "real": total - demo,
            "demo": demo,
        }


def get_repository() -> Tuple[BaseRepository, Dict[str, Any]]:
    """
    Factory function returning the active repository instance along with connection status.
    If Supabase is configured and reachable, returns SupabaseTransactionRepository.
    Otherwise returns SQLiteTransactionRepository with clear explanation.
    """
    client, status = get_supabase_client()
    if client is not None and status.get("is_connected", False):
        try:
            # Ping test table
            client.table("transactions").select("id").limit(1).execute()
            return SupabaseTransactionRepository(client), status
        except Exception as err:
            status["is_connected"] = False
            status["mode"] = "local_sqlite"
            status["message"] = (
                f"Supabase connection test failed ({str(err)}). "
                "Ensure SQL migration (20260101_init_schema.sql) was executed. Falling back to local SQLite."
            )
            return SQLiteTransactionRepository(), status

    return SQLiteTransactionRepository(), status
