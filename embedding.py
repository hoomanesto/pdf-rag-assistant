from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# load model
model = SentenceTransformer("all-MiniLM-L6-v2")

def build_index(chunks):
    texts = [c.page_content for c in chunks]

    embeddings = model.encode(texts)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    return index, texts, model