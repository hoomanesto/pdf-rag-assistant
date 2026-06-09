from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

#load pdf
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(r"Data\Video_Games_RAG_Dataset.pdf")
documents = loader.load()

def load_pdf():

    print(f"Pages loaded: {len(documents)}")

    return documents