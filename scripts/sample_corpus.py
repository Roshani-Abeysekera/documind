"""A small, self-contained corpus used only for benchmarking retrieval quality."""

CORPUS = {
    "kubernetes.txt": (
        "Kubernetes is a container orchestration platform that automates deployment, "
        "scaling, and management of containerized applications. It groups containers "
        "into logical units called pods, and uses a control plane to schedule them "
        "onto worker nodes based on resource availability."
    ),
    "docker.txt": (
        "Docker packages an application and its dependencies into a portable image "
        "that runs consistently across environments. A Dockerfile defines the build "
        "steps, and Docker Compose can run multiple related containers together for "
        "local development."
    ),
    "postgresql.txt": (
        "PostgreSQL is an open-source relational database known for standards "
        "compliance and extensibility. Extensions like pgvector add native support "
        "for storing and querying high-dimensional embedding vectors directly "
        "inside the database."
    ),
    "rag.txt": (
        "Retrieval-augmented generation combines a search step with a language "
        "model generation step. Relevant passages are retrieved from a knowledge "
        "base and included in the prompt, letting the model answer using specific, "
        "up-to-date context instead of relying only on its training data."
    ),
    "agents.txt": (
        "An AI agent is a system that can plan multi-step actions and call external "
        "tools to accomplish a goal, rather than producing a single response. Agent "
        "frameworks like LangGraph model this as a graph of steps with state passed "
        "between them, including loops for retrying or reflecting on results."
    ),
    "s3.txt": (
        "Amazon S3 is an object storage service used for storing files such as "
        "documents, backups, and static assets at scale. Objects are stored in "
        "buckets, and access is controlled through IAM policies and bucket "
        "policies rather than a traditional filesystem."
    ),
    "terraform.txt": (
        "Terraform is an infrastructure-as-code tool that lets you define cloud "
        "resources such as servers, networks, and databases in declarative "
        "configuration files. Running terraform apply creates or updates the "
        "actual infrastructure to match that configuration."
    ),
    "jwt.txt": (
        "JSON Web Tokens are a compact way to represent claims securely between "
        "two parties. A JWT is signed so the server can verify it wasn't tampered "
        "with, and is commonly used to authenticate API requests without needing "
        "a server-side session store."
    ),
    "bm25.txt": (
        "BM25 is a keyword-based ranking function used in search engines to score "
        "how relevant a document is to a query, based on term frequency and "
        "inverse document frequency. Unlike embedding search, it matches exact "
        "terms rather than semantic meaning."
    ),
    "embeddings.txt": (
        "Embeddings are numerical vector representations of text where semantically "
        "similar pieces of text end up close together in vector space. They are "
        "produced by encoder models and are the basis for vector similarity search "
        "in retrieval systems."
    ),
}
