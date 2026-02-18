"""Shared state types for LangGraph."""

from typing import Annotated, Any, TypedDict

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class QueryState(TypedDict, total=False):
    """State for the NL-to-SQL query graph."""

    messages: Annotated[list[BaseMessage], add_messages]
    last_sql: str | None
    last_result: dict[str, Any] | None  # { columns, rows, error }
    last_explanation: str | None
    next_step: str  # for router: "data_query" | "chitchat"
