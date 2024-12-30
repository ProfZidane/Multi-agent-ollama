from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_chroma import Chroma


def retrieval(query):
    embedding = FastEmbedEmbeddings()
    vector_store = Chroma(
        collection_name='documents',
        persist_directory="./embeddings/sql_chroma_db", 
        embedding_function=embedding)
    
    retriever = vector_store.similarity_search(
        query=query,
        k=2,
    )
    return retriever