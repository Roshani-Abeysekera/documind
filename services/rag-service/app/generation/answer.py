"""Citation-grounded answer generation.

If OPENAI_API_KEY is set in the environment, this calls the OpenAI API to
produce a natural-language answer that must cite chunk IDs it used. If no key
is configured, it falls back to a deterministic extractive answer (no LLM
call), so the pipeline stays fully runnable and testable with zero external
API dependencies — useful for local development and CI.
"""
import os


def _format_context(chunks: list[dict]) -> str:
    return "\n\n".join(f"[{c['id']}] ({c['document_name']}): {c['content']}" for c in chunks)


def _extractive_fallback(query: str, chunks: list[dict]) -> dict:
    if not chunks:
        return {"answer": "No relevant documents found.", "citations": []}

    top = chunks[0]
    answer = (
        f"Based on the most relevant passage [{top['id']}] from '{top['document_name']}': "
        f"{top['content'][:400]}"
    )
    return {"answer": answer, "citations": [c["id"] for c in chunks]}


def _openai_generate(query: str, chunks: list[dict]) -> dict:
    from openai import OpenAI

    client = OpenAI()
    context = _format_context(chunks)

    system_prompt = (
        "You answer questions using ONLY the provided context chunks. "
        "Every claim must cite the chunk id it came from, like [3]. "
        "If the context doesn't contain the answer, say so plainly."
    )
    user_prompt = f"Context:\n{context}\n\nQuestion: {query}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )

    return {
        "answer": response.choices[0].message.content,
        "citations": [c["id"] for c in chunks],
    }


def generate_answer(query: str, chunks: list[dict]) -> dict:
    if os.getenv("OPENAI_API_KEY"):
        try:
            return _openai_generate(query, chunks)
        except Exception as exc:  # fall back gracefully rather than 500 the request
            fallback = _extractive_fallback(query, chunks)
            fallback["generation_error"] = str(exc)
            return fallback
    return _extractive_fallback(query, chunks)
