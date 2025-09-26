import json
from pathlib import Path
from omnix.agents.planner import ask

def test_nl2sql_eval():
    f = Path(__file__).with_name("eval_nl2sql.jsonl")
    total = 0
    passed = 0
    for line in f.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        total += 1
        item = json.loads(line)
        out = ask(item["q"])
        ok = True
        # must route to data
        ok &= out.get("route") == "data"
        rows = out.get("result", [])
        # keys present
        if rows:
            ok &= set(item["expect_keys"]).issubset(rows[0].keys())
        # minimal row count
        ok &= len(rows) >= item["min_rows"]
        if ok:
            passed += 1
    # print summary in test output
    print(f"\nNL→SQL eval: {passed}/{total} passed")
    # require >=80% pass as success criteria
    assert passed / max(1, total) >= 0.8, "NL→SQL accuracy below target"
