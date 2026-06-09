from fastapi import FastAPI
from pydantic import BaseModel

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str


# load embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# load saved Chroma DB
db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

retriever = db.as_retriever()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


@app.post("/ask")
def ask(req: QuestionRequest):

    query = req.question

    # 1. retrieve docs
    docs = retriever.invoke(query)

    context = "\n\n".join([d.page_content for d in docs])

    # 2. prompt
    prompt = f"""
    Answer the question using ONLY the context below.

    Context:
    {context}

    Question:
    {query}
    """

    # 3. LLM call
    result = llm.invoke(prompt)

    return {
        "answer": result.content
    }