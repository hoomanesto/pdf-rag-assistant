from pdf_loader import load_pdf
from text_splitter import split_documents

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

def main():
    # 1. Load PDF
    docs = load_pdf()

    # 2. Split into chunks
    chunks = split_documents(docs)

    # 3. Embeddings model (lightweight & free)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 4. Chroma DB folder
    persist_dir = "./chroma_db"

    # 5. Create or load vector DB
    if os.path.exists(persist_dir):
        print("Loading existing Chroma DB...")
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )
    else:
        print("Creating new Chroma DB...")
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_dir
        )

    print("DB ready!")

    # 6. Test search
    query = "What video games are mentioned?"
    results = vectorstore.similarity_search(query, k=2)

    print("\nTop result:\n")
    print(results[0].page_content)

if __name__ == "__main__":
    main()