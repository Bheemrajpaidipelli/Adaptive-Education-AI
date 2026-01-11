import numpy as np
import re

class WordAverageEmbeddings:
    def __init__(self, glove_path="data/glove.6B.100d.txt"):
        self.word_vectors = {}
        self.dim = 100

        with open(glove_path, "r", encoding="utf-8") as f:
            for line in f:
                values = line.split()
                word = values[0]
                vector = np.asarray(values[1:], dtype="float32")
                self.word_vectors[word] = vector

    def preprocess(self, text):
        text = text.lower()
        text = re.sub(r"[^a-z\s]", "", text)
        return text.split()

    def embed_text(self, text):
        words = self.preprocess(text)
        vectors = [
            self.word_vectors[w]
            for w in words
            if w in self.word_vectors
        ]

        if not vectors:
            return np.zeros(self.dim, dtype="float32")

        return np.mean(vectors, axis=0)

    # 🔑 REQUIRED BY FAISS
    def __call__(self, text):
        return self.embed_text(text)

    def embed_documents(self, texts):
        return [self.embed_text(t) for t in texts]

    def embed_query(self, text):
        return self.embed_text(text)
