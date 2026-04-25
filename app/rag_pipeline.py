from google import genai
from app.config import GOOGLE_API_KEY
import time

# initialize client
client = genai.Client(api_key=GOOGLE_API_KEY)


def create_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})  # 🔥 reduce load

    def chain(query):
        docs = retriever.invoke(query)

        # 🔥 reduce token usage (VERY IMPORTANT)
        context = "\n".join([doc.page_content[:400] for doc in docs])

        prompt = f"""
        You are a helpful enterprise assistant.

        Answer ONLY using the given context.
        If the answer is not present, say "Not found in provided documents."

        Context:
        {context}

        Question:
        {query}
        """

        # 🔁 smarter retry (handles overload + quota)
        for attempt in range(5):
            try:
                response = client.models.generate_content(
                    model="models/gemini-2.0-flash-lite",
                    contents=prompt
                )
                return {"answer": response.text.strip()}

            except Exception as e:
                error_msg = str(e)

                if "429" in error_msg or "503" in error_msg:
                    wait = (attempt + 1) * 6  # increasing delay
                    time.sleep(wait)
                else:
                    return {"answer": f"Error: {error_msg}"}

        return {"answer": "⚠️ API busy. Try again after a minute."}

    return chain