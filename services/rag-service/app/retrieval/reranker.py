"""Cross-encoder reranking: re-scores the fused candidate list by feeding
(query, chunk) pairs jointly through a cross-encoder model. This is more
accurate than the bi-encoder similarity used for initial retrieval, because
the cross-encoder attends to the query and chunk together rather than
comparing pre-computed independent embeddings — but it's slower, which is
why it only runs on a small shortlist instead of the whole corpus.
"""
from sentence_transformers import CrossEncoder

_reranker = None

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def get_reranker():
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(RERANKER_MODEL)
    return _reranker


def rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    if not candidates:
        return []

    model = get_reranker()
    pairs = [(query, c["content"]) for c in candidates]
    scores = model.predict(pairs)

    for candidate, score in zip(candidates, scores):
        candidate["rerank_score"] = float(score)

    reranked = sorted(candidates, key=lambda c: c["rerank_score"], reverse=True)
    return reranked[:top_k]
