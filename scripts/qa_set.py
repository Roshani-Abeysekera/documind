"""Hand-labeled QA set for the retrieval benchmark. Each question maps to the
document (from sample_corpus.CORPUS) that contains the answer."""

QA_PAIRS = [
    {"question": "What does Kubernetes automate for containerized applications?", "expected_doc": "kubernetes.txt"},
    {"question": "What is a pod in Kubernetes?", "expected_doc": "kubernetes.txt"},
    {"question": "What does a Dockerfile define?", "expected_doc": "docker.txt"},
    {"question": "How can I run multiple containers together locally?", "expected_doc": "docker.txt"},
    {"question": "What extension lets Postgres store embedding vectors?", "expected_doc": "postgresql.txt"},
    {"question": "Is PostgreSQL open source?", "expected_doc": "postgresql.txt"},
    {"question": "What is retrieval-augmented generation?", "expected_doc": "rag.txt"},
    {"question": "Why include retrieved passages in a prompt?", "expected_doc": "rag.txt"},
    {"question": "What can an AI agent do beyond a single response?", "expected_doc": "agents.txt"},
    {"question": "What does LangGraph model an agent as?", "expected_doc": "agents.txt"},
    {"question": "What is Amazon S3 used for?", "expected_doc": "s3.txt"},
    {"question": "How is access to S3 buckets controlled?", "expected_doc": "s3.txt"},
    {"question": "What does terraform apply do?", "expected_doc": "terraform.txt"},
    {"question": "What kind of tool is Terraform?", "expected_doc": "terraform.txt"},
    {"question": "What is a JWT used for?", "expected_doc": "jwt.txt"},
    {"question": "How does a server verify a JWT hasn't been tampered with?", "expected_doc": "jwt.txt"},
    {"question": "What does BM25 use to score document relevance?", "expected_doc": "bm25.txt"},
    {"question": "How is BM25 different from embedding search?", "expected_doc": "bm25.txt"},
    {"question": "What is a text embedding?", "expected_doc": "embeddings.txt"},
    {"question": "What produces embeddings from text?", "expected_doc": "embeddings.txt"},
]
