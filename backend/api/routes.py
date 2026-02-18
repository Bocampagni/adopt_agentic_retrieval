from fastapi import APIRouter, HTTPException

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages.base import BaseMessage

from api.schemas import ChatMessage, ChatRequest, ChatResponse, TableData
from graph import create_query_graph


router = APIRouter()


def _to_langchain(m: ChatMessage) -> BaseMessage:
    if m.role == "user":
        return HumanMessage(content=m.content)
    if m.role == "assistant":
        return AIMessage(content=m.content)
    return HumanMessage(content=m.content)


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.messages:
        raise HTTPException(status_code=400, detail="messages cannot be empty")
    lc_messages = [_to_langchain(m) for m in request.messages]
    graph = create_query_graph(request.model)
    result = await graph.ainvoke({"messages": lc_messages})
    last = result["messages"][-1]
    table = None
    last_result = result.get("last_result")
    if last_result and not last_result.get("error") and last_result.get("rows") is not None:
        table = TableData(
            columns=last_result.get("columns") or [],
            rows=last_result.get("rows") or [],
        )
    return ChatResponse(
        message=ChatMessage(role="assistant", content=last.content),
        table=table,
    )
