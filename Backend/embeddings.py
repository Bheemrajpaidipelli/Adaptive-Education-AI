import numpy as np
import gensim.downloader as api
from langchain_core.embeddings import Embeddings

class WordAverageEmbeddings(Embeddings):
    def __init__(self):
        self.model = api.load("glove-wiki-gigaword-100")
        self.dim = 100

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            emb = self._embed(text)
            embeddings.append(emb)
        return embeddings

    def embed_query(self, text):
        return self._embed(text)

    def _embed(self, text):
        words = text.lower().split()
        vectors = [self.model[w] for w in words if w in self.model]

        if not vectors:
            return [0.0] * self.dim  # SAFE fallback

        return np.mean(vectors, axis=0).tolist()
