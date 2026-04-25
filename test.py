from app.ingestion import load_documents
from app.vectorstore import create_vectorstore
from langchain_text_splitters import RecursiveCharacterTextSplitter

docs = load_documents("documents")
print(f"\n✅ Loaded {len(docs)} documents\n")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(docs)
print(f"✅ Created {len(chunks)} chunks\n")

vectorstore = create_vectorstore(chunks)
print("✅ Vectorstore created\n")

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

query = "What is the leave policy?"
results = retriever.invoke(query)

print("\n🔍 Retrieved Results:\n")

for i, doc in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(doc.page_content[:300])