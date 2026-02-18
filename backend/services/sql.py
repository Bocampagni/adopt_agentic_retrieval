"""Natural language to SQL: prompts and structured generation."""

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from data import CLAIMS_TABLE_NAME, get_claims_schema

SYSTEM_PROMPT = f"""You are a SQL expert. Given a natural language question about indemnification claims, output a single DuckDB SQL query.

{get_claims_schema()}

Rules:
- Use table name: {CLAIMS_TABLE_NAME}
- Generate ONLY a single SELECT statement. No INSERT, UPDATE, DELETE, DDL, or multiple statements.
- Use exact column and enum values as in the schema (e.g. 'Lost Agricultural Income', 'Under Review').
- For "approved amount less than X% of requested", use: Approved_Amount < (Requested_Amount * X / 100.0) and handle NULL Approved_Amount (e.g. WHERE ... AND Approved_Amount IS NOT NULL AND ...).
- Return valid DuckDB SQL only."""


class SQLGeneration(BaseModel):
    """Structured output for NL to SQL."""

    query: str = Field(description="A single DuckDB SELECT query.")
    explanation: str | None = Field(
        default=None,
        description="Brief explanation of what the query does.",
    )


def generate_sql_from_nl(llm, user_message: str) -> tuple[str | None, str | None]:
    """
    Generate a DuckDB SELECT from natural language.
    Returns (sql_string, explanation) or (None, error_message) on failure.
    """
    try:
        structured_llm = llm.with_structured_output(SQLGeneration)
        result: SQLGeneration = structured_llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_message),
            ]
        )
        sql = result.query.strip()
        if not sql.upper().startswith("SELECT"):
            return None, "Generated code is not a SELECT statement."
        return sql, result.explanation
    except Exception as e:
        return None, str(e)
