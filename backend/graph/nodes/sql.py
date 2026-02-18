"""Generate SQL from the last user message."""

from langchain_core.messages import BaseMessage, HumanMessage

from graph.state import QueryState
from services.sql import generate_sql_from_nl


def _last_user_message(messages: list[BaseMessage]) -> str:
    for m in reversed(messages):
        if isinstance(m, HumanMessage):
            return (m.content or "").strip()
    return ""


def generate_sql_node(state: QueryState, llm) -> dict:
    """Produce last_sql and last_explanation from NL; on error set last_result.error."""
    messages = state.get("messages") or []
    user_message = _last_user_message(messages)
    if not user_message:
        return {
            "last_sql": None,
            "last_explanation": None,
            "last_result": {"columns": [], "rows": [], "error": "No user message found."},
        }
    sql, explanation = generate_sql_from_nl(llm, user_message)
    if sql is None:
        return {
            "last_sql": None,
            "last_explanation": None,
            "last_result": {"columns": [], "rows": [], "error": explanation or "Failed to generate SQL."},
        }
    return {
        "last_sql": sql,
        "last_explanation": explanation,
        "last_result": None,
    }
