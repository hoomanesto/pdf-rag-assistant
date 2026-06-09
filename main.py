from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
import os

load_dotenv()

def main():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # LOAD existing DB (NO rebuilding)
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever()

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    while True:
        query = input("Ask: ")

        if query.lower() == "exit":
            break

        docs = retriever.invoke(query)

        context = "\n\n".join([d.page_content for d in docs])

        prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{query}
"""

        response = llm.invoke(prompt)

        print("\nAnswer:\n", response.content)

if __name__ == "__main__":
    main()