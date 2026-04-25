import os
from langchain_core.documents import Document

def load_documents(folder_path="documents"):
    docs = []

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)

        if file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                docs.append(Document(
                    page_content=text,
                    metadata={"source": file}
                ))

    return docs