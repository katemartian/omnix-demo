from __future__ import annotations
from typing import Any, Dict, Tuple
from .db import get_conn

# Whitelist to keep things safe for the demo
_ALLOWED_PREFIXES = ("SELECT", "WITH")

def run_sql(sql: str, params: Tuple[Any, ...] = ()) -> list[dict]:
    sql_strip = sql.strip().upper()
    if not sql_strip.startswith(_ALLOWED_PREFIXES):
        raise ValueError("Only SELECT/WITH statements are allowed.")
    con = get_conn()
    res = con.execute(sql, params).df()
    return res.to_dict(orient="records")
