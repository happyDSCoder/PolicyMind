import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph, Neo4jVector
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain

load_dotenv()

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))

vector_store = Neo4jVector.from_existing_graph(
    embedding=embeddings,
    graph=graph,
    node_label="Chunk",
    text_node_properties=["text"],
    embedding_node_property="embedding",
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
)


def ask_question(question: str) -> dict:
    result = chain.invoke({"question": question})
    sources = [s.strip() for s in result.get("sources", "").split(",") if s.strip()]
    return {"answer": result["answer"], "sources": sources}