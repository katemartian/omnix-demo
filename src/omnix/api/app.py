from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from omnix.agents.planner import ask as plan_ask

app = FastAPI(title="OmniRx API", version="0.0.1")

class AskReq(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: AskReq):
    out = plan_ask(req.query)
    return out
