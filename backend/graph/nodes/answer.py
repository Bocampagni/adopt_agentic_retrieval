"""Answer node: turn last_result + messages into a natural language reply."""

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

from graph.state import QueryState

ANSWER_SYSTEM = """You are a helpful assistant for a Legal Operations indemnification claims platform.
Given the user's question and the result of a SQL query (columns and rows, or an error), write a short, clear answer.
- If there is an error, explain it in plain language and suggest rephrasing the question.
- If there are rows, summarize the result and mention that a table is shown below. Do not repeat all the data.
- Be concise (2-4 sentences)."""


def _last_user_message(messages: list[BaseMessage]) -> str:
    for m in reversed(messages):
        if isinstance(m, HumanMessage):
            return (m.content or "").strip()
    return ""


def _format_result_for_prompt(result: dict) -> str:
    err = result.get("error")
    if err:
        return f"Query error: {err}"
    cols = result.get("columns") or []
    rows = result.get("rows") or []
    if not cols:
        return "No columns in result."
    lines = ["Columns: " + ", ".join(cols)]
    for i, row in enumerate(rows[:20]):  # cap for prompt size
        lines.append(f"Row {i+1}: {row}")
    if len(rows) > 20:
        lines.append(f"... and {len(rows) - 20} more rows.")
    return "\n".join(lines)


def answer_node(state: QueryState, llm) -> dict:
    """Append an AIMessage with the natural language answer."""
    messages = state.get("messages") or []
    result = state.get("last_result") or {}
    user_message = _last_user_message(messages)
    result_text = _format_result_for_prompt(result)
    prompt = f"User question: {user_message}\n\nQuery result:\n{result_text}"
    response = llm.invoke(
        [
            SystemMessage(content=ANSWER_SYSTEM),
            HumanMessage(content=prompt),
        ]
    )
    content = response.content if hasattr(response, "content") else str(response)
    return {"messages": [AIMessage(content=content)]}
