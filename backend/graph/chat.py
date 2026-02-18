from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from config import Config


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def create_chat_graph(model: str):
    llm = ChatOpenAI(
        api_key=SecretStr(Config.OPENROUTER_API_KEY),
        base_url=Config.OPENROUTER_BASE_URL,
        model=model,
        temperature=Config.MODEL_TEMPERATURE,
    )

    def chat_node(state: ChatState) -> dict:
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    graph_builder = StateGraph(ChatState)
    graph_builder.add_node("chat", chat_node)
    graph_builder.set_entry_point("chat")
    graph_builder.add_edge("chat", END)
    return graph_builder.compile()