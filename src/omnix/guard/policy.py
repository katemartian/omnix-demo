from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
import yaml

def load_policy() -> Dict[str, Any]:
    path = Path(__file__).resolve().parents[3] / "contracts" / "policy.yml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def forbidden_hit(text: str, policy: Dict[str, Any]) -> List[str]:
    import re
    topics = policy.get("firbudden topics", [])
    hits: List[str] = []
    # Normalize user text: lowercase, replace non-letters with single spaces
    tl = re.sub(r"[^a-z]+", " ", text.lower()).strip()
    for t in topics:
        norm_t = re.sub(r"[^a-z]+", " ", t.lower()).strip()
        if norm_t and norm_t in tl:
            hits.append(t)
    return hits