from app.ingestion.parser import extract_text, chunk_text
from app.ingestion.embedder import embed
from app.db import get_connection


def _store_chunks(document_name: str, chunks: list[str]) -> int:
    embeddings = embed(chunks)
    conn = get_connection()
    for chunk, vector in zip(chunks, embeddings):
        conn.execute(
            "INSERT INTO chunks (document_name, content, embedding) VALUES (%s, %s, %s)",
            (document_name, chunk, vector),
        )
    conn.close()
    return len(chunks)


def ingest_document(document_name: str, file_bytes: bytes) -> int:
    """Ingest a PDF: extract -> chunk -> embed -> store."""
    text = extract_text(file_bytes)
    chunks = chunk_text(text)
    return _store_chunks(document_name, chunks)


def ingest_text(document_name: str, text: str) -> int:
    """Ingest raw text directly (no PDF parsing). Useful for testing/benchmarking
    without needing a sample PDF on disk."""
    chunks = chunk_text(text, chunk_size=120, overlap=20)
    return _store_chunks(document_name, chunks)
