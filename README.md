# DocuMind

Multi-tenant RAG and agentic AI platform. Upload documents, get cited answers,
and run multi-step autonomous tasks over your document set.

[Live demo](#) · [Architecture](docs/architecture.md) · [Demo video](#)

## What it does

- Retrieval-augmented Q&A with citation grounding over uploaded documents
- Agentic workflows (e.g. "summarize all contracts expiring in 30 days")
- Multi-tenant document isolation, JWT auth
- Deployed on Kubernetes (EKS), infra managed via Terraform

## Architecture

[diagram — add once services are built]

- **rag-service** (Python/FastAPI) — ingestion, retrieval, generation, agent logic
- **core-service** (Java/Spring Boot) — auth, tenant management, document metadata
- **worker** — async ingestion jobs (Celery/SQS)
- **frontend** (React/TypeScript) — chat UI with streaming and citation display

## Tech stack

Java, Spring Boot, Python, FastAPI, LangGraph, pgvector, AWS (EKS, S3, RDS, SQS),
Kubernetes, Terraform, Docker, React, TypeScript, Prometheus/Grafana

## Status

🚧 In progress — see [build plan](docs/architecture.md) for current milestone.

## Running locally

docker-compose up
(instructions filled in as services are built)

## Benchmark results

(retrieval recall@k numbers go here once available)
