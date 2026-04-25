from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Create vectorstore
def create_vectorstore(docs):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_documents(docs, embeddings)

# Save vectorstore
def save_vectorstore(vectorstore, path="faiss_index"):
    vectorstore.save_local(path)

# Load vectorstore
def load_vectorstore(path="faiss_index"):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)