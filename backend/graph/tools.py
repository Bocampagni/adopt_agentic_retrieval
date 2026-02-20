"""LangChain tools for the ReAct agent."""

import json

from langchain_core.tools import tool

from data.claims_db import execute_query, get_claims_schema


@tool
def execute_sql(sql: str) -> str:
    """Execute a SELECT SQL query against the indemnification claims DuckDB database.

    Use this tool when you need to query claims data. Only SELECT statements are allowed.
    The result includes columns, rows, and any error that occurred.

    Args:
        sql: A valid DuckDB SELECT query against the 'claims' table.
    """
    result = execute_query(sql)
    return json.dumps(result.to_dict())


@tool
def get_database_schema() -> str:
    """Return the schema of the claims database table including column names, types, and valid enum values.

    Use this tool when you need to check the exact column names, data types, or
    allowed enum values before writing a SQL query.
    """
    return get_claims_schema()
