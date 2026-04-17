# PolicyMind

A Graph-RAG chatbot that lets you upload internal policy documents and ask natural language questions about them — such as *"What do I need to consider before launching a new vendor relationship?"*

Built with LangChain, Neo4j, and FastAPI. React frontend coming soon.

---

## Why Graph-RAG?

Standard RAG retrieves isolated text chunks. PolicyMind uses a **knowledge graph** to capture relationships between policies, topics, and dependencies. This means answers are more complete — if Policy A references Policy B, the system understands that connection.

---

## Features

- Upload PDF or Markdown policy documents via API
- Automatic extraction of entities and relationships into Neo4j
- Natural language Q&A grounded in your documents
- Source citations for every answer
- Dynamic: swap in any document set without code changes

---
### How it works

1. Documents are ingested and split into chunks.
2. Each chunk is embedded and stored in :contentReference[oaicite:1]{index=1}.
3. A vector similarity search retrieves the most relevant chunks.
4. The system optionally expands context using graph relationships between chunks and entities.
5. The final context is passed to a language model via :contentReference[oaicite:2]{index=2}.
6. The model generates a grounded answer with references to the source documents.

The LLM backend (e.g. via :contentReference[oaicite:3]{index=3}) ensures that responses are generated locally or via configurable providers.

The API layer is built with :contentReference[oaicite:4]{index=4}, and the frontend is planned using :contentReference[oaicite:5]{index=5}.

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | LangChain |
| Graph Database | Neo4j |
| Embeddings | OpenAI / HuggingFace |
| Backend API | FastAPI |
| Frontend | React (in progress) |

---

## Project Structure

```
policymind/
├── backend/
│   ├── api/          # FastAPI routes
│   ├── core/         # LangChain chains and RAG logic
│   ├── graph/        # Neo4j ingestion and query logic
│   └── models/       # Pydantic schemas
├── docs/             # Example policy documents
├── scripts/          # Ingestion and setup scripts
├── docker-compose.yml
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- OpenAI API key (or local HuggingFace model)

### Setup

```bash
git clone https://github.com/your-username/policymind.git
cd policymind

cp .env.example .env
# Add your API keys to .env

docker compose up -d        # Starts Neo4j
pip install -r requirements.txt
python scripts/ingest.py --file docs/example_policy.pdf
uvicorn backend.api.main:app --reload
```

### Example Query

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What do I need to consider before onboarding a new vendor?"}'
```

```json
{
  "answer": "According to the Vendor Management Policy, you must complete a risk assessment, obtain approval from the procurement team, and ensure GDPR compliance before onboarding a new vendor.",
  "sources": ["vendor_management_policy.pdf", "data_privacy_guidelines.pdf"]
}
```

---
## Roadmap

### Core RAG System
- [x] Document ingestion pipeline (PDF / Text → Chunking → Neo4j storage)
- [x] Vector-based retrieval with Neo4j (embedding similarity search)
- [x] LLM-based question answering via RAG pipeline
- [ ] Upgrade to true Graph-RAG (relationship-aware retrieval + multi-hop traversal)
  - [ ] Use Neo4j relationships (e.g. NEXT, RELATED, HAS_ENTITY) during retrieval
  - [ ] Add graph-based context expansion after vector search
  - [ ] Implement hybrid retrieval (vector + graph traversal)
  - [ ] Add reranking of expanded context for better answer quality

### Backend API
- [ ] FastAPI Q&A endpoint (production-ready API layer)
- [ ] Structured response format (answer + sources + context)
- [ ] Streaming responses for real-time output

### Frontend
- [ ] React frontend with document upload UI
- [ ] Chat interface for querying policies
- [ ] Source highlighting and traceable answers

### System Features
- [ ] Multi-tenant support (separate knowledge graphs per tenant)
- [ ] Authentication & role-based access control
- [ ] Document versioning and updates

### Infrastructure & Quality
- [ ] Dockerized full-stack setup
- [ ] CI/CD pipeline for backend
- [ ] Observability (logging + tracing for RAG pipeline)
---

## License

MIT
