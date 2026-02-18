"""Simple chat node for non-query turns."""

from langchain_core.messages import AIMessage

from graph.state import QueryState


def chat_node(state: QueryState, llm) -> dict:
    """Append an AIMessage from the LLM based on conversation history."""
    messages = state.get("messages") or []
    response = llm.invoke(messages)
    content = response.content if hasattr(response, "content") else str(response)
    return {"messages": [AIMessage(content=content)]}
