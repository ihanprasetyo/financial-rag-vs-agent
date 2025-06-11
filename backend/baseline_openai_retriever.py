# backend/baseline_openai_retriever.py
import openai
import faiss
import numpy as np
import os
import pickle
from dotenv import load_dotenv

load_dotenv()

class BaselineOpenAIRetriever:
    def __init__(self, model="text-embedding-ada-002"):
        self.model = model
        self.index = None
        self.documents = []

    def embed(self, texts):
        client = openai.OpenAI()  # New API client
        response = client.embeddings.create(
            input=texts,
            model=self.model
        )
        return [r.embedding for r in response.data]

    def build_index(self, chunks):
        self.documents = chunks
        embeddings = self.embed(chunks)
        dim = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings).astype("float32"))

    def retrieve(self, query, k=3):
        query_embedding = self.embed([query])[0]
        D, I = self.index.search(np.array([query_embedding]).astype("float32"), k)
        return [self.documents[i] for i in I[0]]

    def save_index(self, path='models/openai_baseline_index'):
        os.makedirs(path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(path, 'index.faiss'))
        with open(os.path.join(path, 'docs.pkl'), 'wb') as f:
            pickle.dump(self.documents, f)

    def load_index(self, path='models/openai_baseline_index'):
        self.index = faiss.read_index(os.path.join(path, 'index.faiss'))
        with open(os.path.join(path, 'docs.pkl'), 'rb') as f:
            self.documents = pickle.load(f)