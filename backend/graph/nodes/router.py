"""Router node: decide whether to run a data query or plain chat."""

from langchain_core.messages import BaseMessage

from graph.state import QueryState

DATA_QUERY_KEYWORDS = (
    "claim", "claims", "amount", "status", "show", "list", "total", "sum",
    "how many", "what is", "which", "approved", "requested", "damage",
    "business", "individual", "review", "disbursed", "rejected", "agricultural",
    "structural", "relocation", "counsel", "filing", "resolution",
)


def _last_user_content(messages: list[BaseMessage]) -> str:
    for m in reversed(messages):
        if hasattr(m, "content") and getattr(m, "type", "") == "human":
            return (m.content or "").strip().lower()
    return ""


def router_node(state: QueryState) -> dict:
    """Route to data_query or chitchat based on last user message."""
    messages = state.get("messages") or []
    content = _last_user_content(messages)
    if not content:
        return {"next_step": "chitchat"}
    next_step = "data_query" if any(kw in content for kw in DATA_QUERY_KEYWORDS) else "chitchat"
    return {"next_step": next_step}
