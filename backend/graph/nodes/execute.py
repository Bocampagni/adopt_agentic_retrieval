"""Execute last_sql and put result in last_result."""

import logging

from data import execute_query
from graph.state import QueryState

logger = logging.getLogger(__name__)


def execute_query_node(state: QueryState) -> dict:
    """Run state["last_sql"] and return last_result (columns, rows, or error)."""
    sql = state.get("last_sql")
    if not sql:
        return {"last_result": {"columns": [], "rows": [], "error": "No SQL to execute."}}
    logger.info("Generated SQL:\n%s", sql)
    result = execute_query(sql)
    return {"last_result": result.to_dict()}
