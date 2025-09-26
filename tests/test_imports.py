def test_imports():
    modules = [
        "omnix",
        "omnix.agents",
        "omnix.tools",
        "omnix.sql",
        "omnix.rag",
        "omnix.guard",
        "omnix.api",
    ]

    for m in modules:
        __import__(m)