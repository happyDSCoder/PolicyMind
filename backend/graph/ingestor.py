import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_neo4j import Neo4jGraph
from langchain_ollama import OllamaEmbeddings

load_dotenv()

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


def ingest_document(file_path: str, source_name: str):
    loader = PyPDFLoader(file_path) if file_path.endswith(".pdf") else TextLoader(file_path)

    docs = loader.load()
    chunks = splitter.split_documents(docs)

    # -------------------------
    # 1. Create Document Node
    # -------------------------
    graph.query(
        """
        MERGE (d:Document {name: $name})
        """,
        {"name": source_name},
    )

    previous_chunk_id = None

    for i, chunk in enumerate(chunks):
        text = chunk.page_content

        embedding = embeddings.embed_query(text)

        chunk_id = f"{source_name}_{i}"

        # -------------------------
        # 2. Create Chunk Node
        # -------------------------
        graph.query(
            """
            MERGE (c:Chunk {id: $id})
            SET c.text = $text,
                c.embedding = $embedding,
                c.source = $source,
                c.index = $index

            WITH c
            MATCH (d:Document {name: $source})
            MERGE (d)-[:HAS_CHUNK]->(c)
            """,
            {
                "id": chunk_id,
                "text": text,
                "embedding": embedding,
                "source": source_name,
                "index": i,
            },
        )

        # -------------------------
        # 3. Sequential Linking (IMPORTANT)
        # -------------------------
        if previous_chunk_id:
            graph.query(
                """
                MATCH (a:Chunk {id: $prev})
                MATCH (b:Chunk {id: $curr})
                MERGE (a)-[:NEXT]->(b)
                """,
                {"prev": previous_chunk_id, "curr": chunk_id},
            )

        previous_chunk_id = chunk_id

    print(f"Ingested {len(chunks)} chunks with graph structure from {source_name}")