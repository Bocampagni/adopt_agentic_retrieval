"""NL-to-SQL query graph: router -> generate_sql -> execute -> answer, or chitchat."""

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from pydantic import SecretStr

from config import Config
from graph.state import QueryState
from graph.nodes import (
    router_node,
    generate_sql_node,
    execute_query_node,
    answer_node,
    chat_node,
)


def create_query_graph(model: str):
    llm = ChatOpenAI(
        api_key=SecretStr(Config.OPENROUTER_API_KEY),
        base_url=Config.OPENROUTER_BASE_URL,
        model=model,
        temperature=Config.MODEL_TEMPERATURE,
    )

    def _sql_node(s: QueryState) -> dict:
        return generate_sql_node(s, llm)

    def _answer_node(s: QueryState) -> dict:
        return answer_node(s, llm)

    def _chat_node(s: QueryState) -> dict:
        return chat_node(s, llm)

    graph_builder = StateGraph(QueryState)
    graph_builder.add_node("router", router_node)
    graph_builder.add_node("generate_sql", _sql_node)
    graph_builder.add_node("execute_query", execute_query_node)
    graph_builder.add_node("answer", _answer_node)
    graph_builder.add_node("chat", _chat_node)

    graph_builder.set_entry_point("router")
    graph_builder.add_conditional_edges(
        "router",
        lambda s: s.get("next_step", "chitchat"),
        {"data_query": "generate_sql", "chitchat": "chat"},
    )
    graph_builder.add_edge("generate_sql", "execute_query")
    graph_builder.add_edge("execute_query", "answer")
    graph_builder.add_edge("answer", END)
    graph_builder.add_edge("chat", END)

    return graph_builder.compile()
