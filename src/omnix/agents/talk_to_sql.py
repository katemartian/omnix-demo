from __future__ import annotations
from .nl2sql import parse_intent, to_sql
from ..sql.queries import run_sql

def ask(text: str) -> dict:
    parsed = parse_intent(text)
    sql, params = to_sql(parsed)
    rows = run_sql(sql, params)
    return {"intent": parsed.get("intent"), "sql": sql.strip(), "rows": rows}
