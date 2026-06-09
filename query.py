import numpy as np

def search(query, model, index, texts, k=3):
    q_emb = model.encode([query])
    distances, indices = index.search(np.array(q_emb), k)

    return [texts[i] for i in indices[0]]