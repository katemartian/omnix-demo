from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Tuple
import faiss
import numpy as np

_CHUNK_SIZE = 350
_CHUNK_OVERLAP = 40

def _read_docs(doc_dir: Path) -> List[Tuple[str, str]]:
    docs = []
    for p in sorted(doc_dir.glob("*.md")):
        docs.append((p.name, p.read_text(encoding="utf-8")))
    return docs

def _chunk_text(text: str, size: int = _CHUNK_SIZE, overlap: int = _CHUNK_OVERLAP) -> List[str]:
    # simple paragraph-aware chunking
    paras = [p.strip() for p in text.splitlines()]
    chunks = []
    cur = ""
    for p in paras:
        if not p:
            continue
        if len(cur) + 1 + len(p) <= size:
            cur = (cur + "\n" + p).strip()
        else:
            if cur:
                chunks.append(cur)
            # overlap last tail
            tail = cur[-overlap:] if overlap > 0 else ""
            cur = (tail + "\n" + p).strip()
    if cur:
        chunks.append(cur)
    return [c for c in chunks if c]

def build_corpus(doc_dir: Path) -> List[Dict]:
    corpus: List[Dict] = []
    for fname, text in _read_docs(doc_dir):
        chunks = _chunk_text(text)
        for i, chunk in enumerate(chunks):
            corpus.append({
                "doc": fname,
                "chunk_id": i,
                "text": chunk
            })
    return corpus

# Lazy import to avoid heavy startup if not used
_model = None
def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model

def _embed(texts: List[str]) -> np.ndarray:
    model = _get_model()
    vecs = model.encode(texts, normalize_embeddings=True)
    return np.asarray(vecs, dtype="float32")

class Retriever:
    def __init__(self, corpus: List[Dict]):
        self.corpus = corpus
        self.index = None
        if corpus:
            self._build()

    def _build(self):
        texts = [c["text"] for c in self.corpus]
        embs = _embed(texts)
        d = embs.shape[1]
        self.index = faiss.IndexFlatIP(d)
        self.index.add(embs)

    def search(self, query: str, k: int = 3) -> List[Dict]:
        if not self.corpus:
            return []
        q = _embed([query])
        D, idxs = self.index.search(q, min(k, len(self.corpus)))
        out = []
        for score, idx in zip(D[0], idxs[0]):
            if idx == -1:
                continue
            c = self.corpus[int(idx)]
            out.append({
                "doc": c["doc"],
                "chunk_id": c["chunk_id"],
                "text": c["text"],
                "score": float(score)
            })
        return out

def load_default() -> Retriever:
    root = Path(__file__).resolve().parents[3] / "data" / "docs"
    corpus = build_corpus(root)
    return Retriever(corpus)
