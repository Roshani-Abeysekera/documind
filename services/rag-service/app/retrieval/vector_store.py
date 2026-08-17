from app.ingestion.embedder import embed
from app.db import get_connection


def vector_search(query: str, top_k: int = 10) -> list[dict]:
    """Pure vector similarity search (cosine distance via pgvector's <=> operator)."""
    query_vector = embed([query])[0]
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT id, document_name, content, embedding <=> %s AS distance
        FROM chunks
        ORDER BY distance ASC
        LIMIT %s
        """,
        (query_vector, top_k),
    ).fetchall()
    conn.close()
    return [
        {"id": r[0], "document_name": r[1], "content": r[2], "distance": float(r[3])}
        for r in rows
    ]
