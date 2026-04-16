import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_neo4j import Neo4jGraph, Neo4jVector
from langchain_openai import OpenAIEmbeddings

load_dotenv()

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)


def ingest_document(file_path: str, source_name: str):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)

    docs = loader.load()
    chunks = splitter.split_documents(docs)

    for chunk in chunks:
        chunk.metadata["source"] = source_name

    Neo4jVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        graph=graph,
        node_label="Chunk",
        text_node_property="text",
        embedding_node_property="embedding",
    )

    print(f"Ingested {len(chunks)} chunks from {source_name}")