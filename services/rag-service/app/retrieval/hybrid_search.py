"""Hybrid retrieval: fuses vector similarity search with BM25 keyword search
using Reciprocal Rank Fusion (RRF).

Why hybrid: vector search is great at semantic/paraphrase matches but can miss
exact keyword hits (product codes, acronyms, names). BM25 is the opposite.
Fusing both ranked lists is a simple, well-established way to get the benefit
of each without needing to tune a blend weight.
"""
from rank_bm25 import BM25Okapi

from app.db import fetch_all_chunks
from app.retrieval.vector_store import vector_search

RRF_K = 60  # standard smoothing constant used in reciprocal rank fusion


def _tokenize(text: str) -> list[str]:
    return text.lower().split()


def bm25_search(query: str, top_k: int = 10) -> list[dict]:
    corpus = fetch_all_chunks()
    if not corpus:
        return []

    tokenized_corpus = [_tokenize(c["content"]) for c in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(_tokenize(query))

    ranked = sorted(zip(corpus, scores), key=lambda x: x[1], reverse=True)
    return [
        {"id": c["id"], "document_name": c["document_name"], "content": c["content"], "bm25_score": float(s)}
        for c, s in ranked[:top_k]
    ]


def reciprocal_rank_fusion(vector_results: list[dict], bm25_results: list[dict], top_k: int = 10) -> list[dict]:
    scores: dict[int, float] = {}
    chunk_lookup: dict[int, dict] = {}

    for rank, item in enumerate(vector_results):
        scores[item["id"]] = scores.get(item["id"], 0.0) + 1.0 / (RRF_K + rank + 1)
        chunk_lookup[item["id"]] = item

    for rank, item in enumerate(bm25_results):
        scores[item["id"]] = scores.get(item["id"], 0.0) + 1.0 / (RRF_K + rank + 1)
        chunk_lookup.setdefault(item["id"], item)

    fused = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [
        {
            "id": chunk_id,
            "document_name": chunk_lookup[chunk_id]["document_name"],
            "content": chunk_lookup[chunk_id]["content"],
            "fused_score": score,
        }
        for chunk_id, score in fused
    ]


def hybrid_search(query: str, top_k: int = 10, candidate_pool: int = 20) -> list[dict]:
    vector_results = vector_search(query, top_k=candidate_pool)
    bm25_results = bm25_search(query, top_k=candidate_pool)
    return reciprocal_rank_fusion(vector_results, bm25_results, top_k=top_k)
