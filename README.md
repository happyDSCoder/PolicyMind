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

- [x] Document ingestion pipeline
- [x] Graph-based retrieval with Neo4j
- [x] FastAPI Q&A endpoint
- [ ] React frontend with document upload UI
- [ ] Multi-tenant support
- [ ] Authentication

---

## License

MIT
