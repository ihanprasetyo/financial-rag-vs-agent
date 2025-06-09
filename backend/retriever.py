from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle

class FinancialRetriever:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.doc_embeddings = None

    def build_index(self, chunks):
        self.documents = chunks
        self.doc_embeddings = self.model.encode(chunks, convert_to_tensor=False)
        dim = self.doc_embeddings[0].shape[0]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.doc_embeddings)

    def retrieve(self, query, k=3):
        query_embedding = self.model.encode([query])
        D, I = self.index.search(query_embedding, k)
        return [self.documents[i] for i in I[0]]

    def save_index(self, path='models/faiss_index'):
        os.makedirs(path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(path, 'index.faiss'))
        with open(os.path.join(path, 'docs.pkl'), 'wb') as f:
            pickle.dump(self.documents, f)

    def load_index(self, path='models/faiss_index'):
        self.index = faiss.read_index(os.path.join(path, 'index.faiss'))
        with open(os.path.join(path, 'docs.pkl'), 'rb') as f:
            self.documents = pickle.load(f)