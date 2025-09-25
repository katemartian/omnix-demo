from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any
import re

from .talk_to_sql import ask as ask_sql
from .doc_agent import ask_docs

@dataclass
class Trace:
    tool: str
    intent: str | None
    notes: str | None

def classify(text: str) -> str:
    t = text.lower()
    # simple heuristics: data vs docs
    if re.search(r"\b(rx|revenue|trend|weeks?|district|segment|forecast|sql|show)\b", t):
        return "data"
    if re.search(r"\b(formulary|label|policy|contraindication|off[- ]?label|payer)\b", t):
        return "docs"
    # fallback: prefer data if mentions province/district; else docs
    if re.search(r"\b(on|qc|bc|district|province)\b", t):  # Canadian provinces
        return "data"
    return "docs"

def ask(text: str) -> Dict[str, Any]:
    route = classify(text)
    if route == "data":
        out = ask_sql(text)
        trace = Trace(tool="sql", intent=out.get("intent"), notes="nl→sql")
        return {
            "route": route,
            "result": out["rows"],
            "sql": out["sql"],
            "trace": asdict(trace),
        }
    else:
        out = ask_docs(text)
        trace = Trace(tool="docs", intent=None, notes="rag")
        return {
            "route": route,
            "blocked": out.get("blocked", False),
            "reason": out.get("reason"),
            "answer": out.get("answer"),
            "citations": out.get("citations"),
            "trace": asdict(trace),
        }
