from __future__ import annotations
from typing import Dict, Any
from ..rag.index import load_default
from ..guard.policy import load_policy, forbidden_hit
from ..guard.filters import redact_pii
import re

_retriever = None
_policy = None

def _get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = load_default()
    return _retriever

def _get_policy():
    global _policy
    if _policy is None:
        _policy = load_policy()
    return _policy

def ask_docs(question: str, k: int = 3) -> Dict[str, Any]:
    policy = _get_policy()
    f_hits = forbidden_hit(question, policy)
    if f_hits:
        return {
            "blocked": True,
            "reason": f"forbidden_topics:{','.join(f_hits)}",
            "answer": None,
            "citations": []
        }
    # Block explicit off-label requests, regardless of policy variants
    if re.search(r"\boff[\s\-_]*label(\s*use|\s*uses)?\b", question.lower()):
        return {
            "blocked": True,
            "reason": "forbidden_topics:off_label_use",
            "answer": None,
            "citations": []
        }
    # Block explicit PII requests (e.g., "phone numbers")
    if re.search(r"\b(phone|phone\s*number|contact\s*number|personal\s*number)s?\b", question.lower()):
        return {
            "blocked": True,
            "reason": "pii_request",
            "answer": None,
            "citations": []
        }

    retriever = _get_retriever()
    hits = retriever.search(question, k=k)

    # Compose a minimal answer by concatenating top snippets with citations
    parts = []
    cits = []
    for h in hits:
        snippet, _ = redact_pii(h["text"], policy.get("redactions", {}).get("pii_regex", []))
        parts.append(snippet.strip())
        cits.append({"doc": h["doc"], "chunk_id": h["chunk_id"], "score": round(h["score"], 3)})

    answer = "\n\n".join(parts)
    # Minimal rule: require citations when docs are used
    if policy.get("requirements") and "responses must include citations when using documents" in policy["requirements"]:
        if not cits:
            return {"blocked": True, "reason": "missing_citations", "answer": None, "citations": []}

    return {"blocked": False, "answer": answer, "citations": cits}
