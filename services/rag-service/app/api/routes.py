from fastapi import APIRouter, UploadFile, File

from app.ingestion.pipeline import ingest_document
from app.retrieval.hybrid_search import hybrid_search
from app.retrieval.reranker import rerank
from app.generation.answer import generate_answer

router = APIRouter()


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    file_bytes = await file.read()
    num_chunks = ingest_document(file.filename, file_bytes)
    return {"document": file.filename, "chunks_stored": num_chunks}


@router.get("/query")
def query(q: str, top_k: int = 5, candidate_pool: int = 20):
    """Top-k reranked chunks for a query.
    Pipeline: vector search + BM25 -> reciprocal rank fusion -> cross-encoder rerank."""
    fused = hybrid_search(q, top_k=candidate_pool)
    results = rerank(q, fused, top_k=top_k)
    return {"query": q, "results": results}


@router.get("/answer")
def answer(q: str, top_k: int = 5, candidate_pool: int = 20):
    """Full RAG: retrieve + rerank + generate a citation-grounded answer."""
    fused = hybrid_search(q, top_k=candidate_pool)
    top_chunks = rerank(q, fused, top_k=top_k)
    result = generate_answer(q, top_chunks)
    return {"query": q, **result, "sources": top_chunks}
