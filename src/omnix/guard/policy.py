from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
import yaml

def load_policy() -> Dict[str, Any]:
    path = Path(__file__).resolve().parents[3] / "contracts" / "policy.yml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def forbidden_hit(text: str, policy: Dict[str, Any]) -> List[str]:
    topics = policy.get("forbidden_topics", [])
    hits = []
    tl = text.lower()
    for t in topics:
        if t.replace("_", " ") in tl:
            hits.append(t)
    return hits
