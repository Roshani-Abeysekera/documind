"""Retrieval benchmark: ingests a small hand-built corpus, runs a hand-labeled
QA set against the hybrid retrieval + reranking pipeline, and reports
recall@k and MRR.

Run inside the rag-service container:
    docker compose up -d db rag-service
    docker compose exec rag-service python scripts/benchmark_retrieval.py

Or locally, with services/rag-service/requirements.txt installed and
DATABASE_URL pointing at a reachable Postgres:
    python scripts/benchmark_retrieval.py
"""
import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))

# Make "app.*" importable regardless of whether this runs inside the
# container (docker-compose mounts app at /app/app, cwd /app) or locally
# against the repo layout (services/rag-service/app).
for _candidate in (
    os.path.join(_HERE, "..", "services", "rag-service"),  # local repo layout
    "/app",  # docker-compose layout
):
    if os.path.isdir(_candidate) and _candidate not in sys.path:
        sys.path.insert(0, _candidate)

from app.db import init_db, clear_chunks  # noqa: E402
from app.ingestion.pipeline import ingest_text  # noqa: E402
from app.retrieval.hybrid_search import hybrid_search  # noqa: E402
from app.retrieval.reranker import rerank  # noqa: E402

from sample_corpus import CORPUS  # noqa: E402
from qa_set import QA_PAIRS  # noqa: E402

TOP_K = 5


def build_corpus():
    print("Resetting chunks table...")
    init_db()
    clear_chunks()
    print(f"Ingesting {len(CORPUS)} documents...")
    for doc_name, text in CORPUS.items():
        ingest_text(doc_name, text)


def run_benchmark():
    hits_at_k = 0
    reciprocal_ranks = []

    print(f"\nRunning {len(QA_PAIRS)} queries...\n")
    for pair in QA_PAIRS:
        question = pair["question"]
        expected = pair["expected_doc"]

        fused = hybrid_search(question, top_k=20)
        results = rerank(question, fused, top_k=TOP_K)
        retrieved_docs = [r["document_name"] for r in results]

        hit = expected in retrieved_docs
        hits_at_k += int(hit)

        if hit:
            rank = retrieved_docs.index(expected) + 1
            reciprocal_ranks.append(1.0 / rank)
        else:
            reciprocal_ranks.append(0.0)

        status = "PASS" if hit else "FAIL"
        print(f"[{status}] {question}\n    expected: {expected} | got: {retrieved_docs}")

    recall_at_k = hits_at_k / len(QA_PAIRS)
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)

    print("\n--- Results ---")
    print(f"Recall@{TOP_K}: {recall_at_k:.2%}  ({hits_at_k}/{len(QA_PAIRS)})")
    print(f"MRR:       {mrr:.3f}")

    return recall_at_k, mrr


def write_report(recall_at_k: float, mrr: float):
    report_path = os.path.join(_HERE, "..", "docs", "benchmark_results.md")
    with open(report_path, "w") as f:
        f.write("# Retrieval Benchmark Results\n\n")
        f.write(f"- Corpus size: {len(CORPUS)} documents\n")
        f.write(f"- QA set size: {len(QA_PAIRS)} questions\n")
        f.write("- Pipeline: hybrid search (vector + BM25, RRF-fused) + cross-encoder rerank\n\n")
        f.write("| Metric | Value |\n|---|---|\n")
        f.write(f"| Recall@{TOP_K} | {recall_at_k:.2%} |\n")
        f.write(f"| MRR | {mrr:.3f} |\n")
    print(f"\nReport written to {report_path}")


if __name__ == "__main__":
    build_corpus()
    recall, mrr = run_benchmark()
    write_report(recall, mrr)
