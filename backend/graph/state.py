"""Shared state types for LangGraph."""

from typing import Annotated

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class QueryState:
    """State for the ReAct agent graph. Only messages are needed; the agent
    manages SQL generation and results through tool call messages."""

    messages: Annotated[list[BaseMessage], add_messages]
