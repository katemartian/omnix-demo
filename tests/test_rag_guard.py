from omnix.agents.doc_agent import ask_docs

def test_rag_returns_citations():
    out = ask_docs("What are the formulary notes for Drug X in Ontario?")
    assert not out["blocked"]
    assert out["citations"], "must include citations"
    assert isinstance(out["citations"][0]["doc"], str)

def test_guard_forbidden_offlabel():
    out = ask_docs("Tell me off label use details for this drug")
    assert out["blocked"]
    assert "forbidden_topics" in out["reason"]
