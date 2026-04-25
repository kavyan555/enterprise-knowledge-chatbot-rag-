from app.ingestion import load_documents, split_documents
from app.vectorstore import create_vectorstore, save_vectorstore, load_vectorstore
from app.rag_pipeline import create_rag_chain
from app.config import CHUNK_SIZE, CHUNK_OVERLAP
import os

VECTOR_PATH = "faiss_index"

def setup_pipeline():
    if not os.path.exists(VECTOR_PATH):
        docs = load_documents()
        chunks = split_documents(docs, CHUNK_SIZE, CHUNK_OVERLAP)
        vectorstore = create_vectorstore(chunks)
        save_vectorstore(vectorstore)
    else:
        vectorstore = load_vectorstore()

    chain = create_rag_chain(vectorstore)
    return chain