from typing import Any

from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    model: str


class TableData(BaseModel):
    columns: list[str]
    rows: list[list[Any]]


class ChatResponse(BaseModel):
    message: ChatMessage
    table: TableData | None = None


class SchemaResponse(BaseModel):
    table_name: str
    columns: list[str]
    sample_rows: list[list[Any]]
