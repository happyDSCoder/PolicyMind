import os
from dotenv import load_dotenv

from langchain_neo4j import Neo4jGraph, Neo4jVector
from langchain_ollama import ChatOllama, OllamaEmbeddings

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# -------------------------
# Neo4j Connection
# -------------------------
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

# -------------------------
# Embeddings (Ollama)
# -------------------------
embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
)

# -------------------------
# Vector Store from Neo4j
# -------------------------
vector_store = Neo4jVector.from_existing_graph(
    embedding=embeddings,
    graph=graph,
    node_label="Chunk",
    text_node_properties=["text"],
    embedding_node_property="embedding",
)

# -------------------------
# LLM (Ollama)
# -------------------------
llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "qwen3:8b"),
    temperature=0
)

# -------------------------
# Prompt
# -------------------------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Answer ONLY using the context below. "
        "Always cite the source document.\n\nContext:\n{context}"
    ),
    ("human", "{input}")
])

# -------------------------
# Retriever
# -------------------------
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# -------------------------
# LCEL Chain
# -------------------------
chain = (
    {
        "context": (lambda x: x["input"]) | retriever,
        "input": RunnablePassthrough()
    }
    | prompt
    | llm
)
# -------------------------
# Helper Function
# -------------------------
def ask_question(question: str) -> dict:
    result = chain.invoke({"input": question})

    # LCEL returns AIMessage → extract text safely
    answer = result.content if hasattr(result, "content") else str(result)

    # Optional: try to extract source metadata if available
    sources = []

    try:
        docs = retriever.get_relevant_documents(question)
        sources = list({
            doc.metadata.get("source", "")
            for doc in docs
        })
    except Exception:
        pass

    return {
        "answer": answer,
        "sources": sources
    }
