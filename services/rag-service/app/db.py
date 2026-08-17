import psycopg
from pgvector.psycopg import register_vector
from app.config import settings


def get_connection():
    conn = psycopg.connect(settings.database_url, autocommit=True)
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(conn)
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id SERIAL PRIMARY KEY,
            document_name TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding vector(384)
        )
        """
    )
    conn.close()


def clear_chunks():
    """Wipe all chunks. Used by the benchmark script to start from a clean slate."""
    conn = get_connection()
    conn.execute("TRUNCATE TABLE chunks RESTART IDENTITY")
    conn.close()


def fetch_all_chunks():
    """Returns every chunk's id, document_name, content — used for BM25, which needs
    the full corpus in memory (fine at prototype scale; would move to a proper
    search index like OpenSearch/Elasticsearch at production scale)."""
    conn = get_connection()
    rows = conn.execute("SELECT id, document_name, content FROM chunks").fetchall()
    conn.close()
    return [{"id": r[0], "document_name": r[1], "content": r[2]} for r in rows]
