from omnix.agents.planner import ask

def test_planner_routes_sql():
    out = ask("Trend last 4 weeks RX in ON")
    assert out["route"] == "data"
    assert "sql" in out and "result" in out

def test_planner_routes_docs():
    out = ask("Summarize formulary constraints for Drug X in Ontario")
    assert out["route"] == "docs"
    assert out["citations"], "docs route must include citations"
