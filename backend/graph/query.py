"""ReAct agent graph: LLM reasons and calls tools (execute_sql, get_database_schema)."""

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from pydantic import SecretStr

from config import Config
from data.claims_db import get_claims_schema, CLAIMS_TABLE_NAME
from graph.tools import execute_sql, get_database_schema

SYSTEM_PROMPT = f"""You are a helpful assistant for a Legal Operations indemnification claims platform.
You have access to a DuckDB database with indemnification claims data.

{get_claims_schema()}

SQL rules:
- Use table name: {CLAIMS_TABLE_NAME}
- Generate ONLY single SELECT statements. No INSERT, UPDATE, DELETE, DDL, or multiple statements.
- Use exact column and enum values as listed in the schema (e.g. 'Lost Agricultural Income', 'Under Review').
- For percentage comparisons like "approved amount less than X% of requested", use: Approved_Amount < (Requested_Amount * X / 100.0) and handle NULL Approved_Amount.
- Return valid DuckDB SQL only.

Behavior:
- When the user asks about claims data, write a SQL query and use the execute_sql tool to run it.
- If the query returns an error, analyze the error, fix the SQL, and retry.
- After getting results, provide a concise answer (2-4 sentences). If rows are returned, mention that a table is shown below. Do not repeat all the data verbatim.
- If the user asks a general question unrelated to claims data, respond directly without using tools.
- If you are unsure about column names or enum values, use the get_database_schema tool to check.
"""


def create_query_graph(model: str):
    llm = ChatOpenAI(
        api_key=SecretStr(Config.OPENROUTER_API_KEY),
        base_url=Config.OPENROUTER_BASE_URL,
        model=model,
        temperature=Config.MODEL_TEMPERATURE,
    )

    tools = [execute_sql, get_database_schema]

    return create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
