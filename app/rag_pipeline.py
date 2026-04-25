import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# ✅ Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key missing in .env")

genai.configure(api_key=api_key)

# ✅ Use stable working model
model = genai.GenerativeModel("gemini-flash-latest")


def create_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    def chain(query):
        docs = retriever.invoke(query)

        # ✅ limit context (prevents API overload)
        context = "\n\n".join([doc.page_content[:300] for doc in docs])

        prompt = f"""
You are a helpful enterprise assistant.

Answer ONLY from the given context.
If the answer is not present, say "Not found in provided documents".
Be concise and clear.
Do NOT mention "context" or "provided documents" in your answer.
Answer like a direct response.

Context:
{context}

Question:
{query}
"""

        try:
            time.sleep(1)  # ✅ small delay to avoid rate limit

            response = model.generate_content(prompt)

            return {
                "answer": response.text.strip() if response.text else "No response"
            }

        except Exception as e:
            return {"answer": f"⚠️ API Error: {str(e)}"}

    return chain