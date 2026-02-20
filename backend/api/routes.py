import json

from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.messages.base import BaseMessage

from api.schemas import ChatMessage, ChatRequest, ChatResponse, SchemaResponse, TableData
from data.claims_db import CLAIMS_TABLE_NAME, execute_query
from graph import create_query_graph

router = APIRouter()


def _to_langchain(m: ChatMessage) -> BaseMessage:
    if m.role == "user":
        return HumanMessage(content=m.content)
    if m.role == "assistant":
        return AIMessage(content=m.content)
    return HumanMessage(content=m.content)


def _extract_table_from_messages(messages: list[BaseMessage]) -> TableData | None:
    """Scan messages in reverse for the last execute_sql ToolMessage with valid results."""
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage) and msg.name == "execute_sql":
            if not isinstance(msg.content, str):
                continue
            try:
                data = json.loads(msg.content)
            except (json.JSONDecodeError, TypeError):
                continue
            if data.get("rows") and not data.get("error"):
                return TableData(
                    columns=data.get("columns", []),
                    rows=data.get("rows", []),
                )
    return None


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/api/schema", response_model=SchemaResponse)
def schema_preview():
    result = execute_query(f"SELECT * FROM {CLAIMS_TABLE_NAME} LIMIT 15")
    if result.error:
        raise HTTPException(status_code=500, detail=result.error)
    return SchemaResponse(
        table_name=CLAIMS_TABLE_NAME,
        columns=result.columns,
        sample_rows=result.rows,
    )


@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.messages:
        raise HTTPException(status_code=400, detail="messages cannot be empty")

    lc_messages = [_to_langchain(m) for m in request.messages]
    graph = create_query_graph(request.model)
    result = await graph.ainvoke({"messages": lc_messages})

    messages = result["messages"]
    last_ai = next(
        (m for m in reversed(messages)
         if isinstance(m, AIMessage) and isinstance(m.content, str) and m.content),
        None,
    )
    if last_ai is None:
        raise HTTPException(status_code=500, detail="Agent produced no response")

    table = _extract_table_from_messages(messages)
    content = last_ai.content if isinstance(last_ai.content, str) else str(last_ai.content)

    return ChatResponse(
        message=ChatMessage(role="assistant", content=content),
        table=table,
    )
