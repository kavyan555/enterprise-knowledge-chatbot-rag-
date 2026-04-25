from app.ingestion import load_documents
from app.vectorstore import create_vectorstore
from app.rag_pipeline import create_rag_chain

from langchain_text_splitters import RecursiveCharacterTextSplitter

def setup_pipeline():
    docs = load_documents("documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    vectorstore = create_vectorstore(chunks)

    chain = create_rag_chain(vectorstore)

    return chain