"""DuckDB data layer for indemnification claims CSV."""

from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import duckdb

_BACKEND_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = _BACKEND_DIR / "indemnification_claims_data.csv"

CLAIMS_TABLE_NAME = "claims"


def get_claims_schema() -> str:
    """Return schema description for LLM prompts (column names and types)."""
    return """
Table: claims (from indemnification_claims_data.csv)

Columns:
- Claim_ID: VARCHAR (e.g. CLM-10001)
- Claimant_Type: VARCHAR — one of: Individual, Business, Municipality
- Damage_Category: VARCHAR — one of: Property Damage, Relocation Expenses, Lost Agricultural Income, Business Interruption, Structural Damage
- Status: VARCHAR — one of: Under Review, Approved, Disbursed, Rejected
- Requested_Amount: DOUBLE
- Approved_Amount: DOUBLE (NULL when Status = 'Under Review')
- Assigned_Counsel: VARCHAR
- Filing_Date: DATE (YYYY-MM-DD)
- Resolution_Date: DATE (NULL when Status = 'Under Review')

Business rules:
- Approved_Amount and Resolution_Date are NULL when Status = 'Under Review'.
- Use exact enum values for Status, Claimant_Type, and Damage_Category (e.g. 'Lost Agricultural Income' not 'Lost Income').
""".strip()


class QueryResult:
    """Result of a SQL query: columns and rows, or an error."""

    def __init__(
        self,
        columns: list[str] | None = None,
        rows: list[list[Any]] | None = None,
        error: str | None = None,
    ):
        self.columns = columns or []
        self.rows = rows or []
        self.error = error

    def to_dict(self) -> dict[str, Any]:
        if self.error:
            return {"columns": [], "rows": [], "error": self.error}
        return {"columns": self.columns, "rows": self.rows, "error": None}


def get_connection() -> duckdb.DuckDBPyConnection:
    """Return a DuckDB connection with the claims CSV registered as a table."""
    conn = duckdb.connect(":memory:")
    path = str(CSV_PATH.resolve())
    conn.execute(
        f"CREATE VIEW {CLAIMS_TABLE_NAME} AS SELECT * FROM read_csv_auto({path!r})"
    )
    return conn


def execute_query(sql: str) -> QueryResult:
    """
    Execute a SELECT query against the claims data.
    Returns QueryResult with columns/rows or error.
    """
    sql_stripped = sql.strip().upper()
    if not sql_stripped.startswith("SELECT"):
        return QueryResult(error="Only SELECT queries are allowed.")
    def _serialize(v: Any) -> Any:
        if v is None:
            return None
        if isinstance(v, (date, datetime)):
            return v.isoformat()
        if isinstance(v, Decimal):
            return float(v)
        return v

    try:
        conn = get_connection()
        try:
            result = conn.execute(sql)
            columns = [d[0] for d in result.description]
            rows = result.fetchall()
            rows_list = [[_serialize(cell) for cell in r] for r in rows]
            return QueryResult(columns=columns, rows=rows_list)
        finally:
            conn.close()
    except Exception as e:
        return QueryResult(error=str(e))
