from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def create_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    return FAISS.from_documents(chunks, embeddings)

def save_vectorstore(vectorstore, path="faiss_index"):
    vectorstore.save_local(path)

def load_vectorstore(path="faiss_index"):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)