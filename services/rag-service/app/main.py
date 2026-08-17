from fastapi import FastAPI

from app.api.routes import router
from app.db import init_db

app = FastAPI(title="DocuMind RAG Service")


@app.on_event("startup")
def startup():
    init_db()


app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
