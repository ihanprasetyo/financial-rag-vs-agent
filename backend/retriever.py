from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle
import re
import numpy as np

class FinancialRetriever:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.doc_embeddings = None

    def retrieve(self, query, k=3):
        query_embedding = self.model.encode([query])

        # Light filtering for quarter-specific queries
        quarter_terms = ["q1", "q2", "q3", "q4", "first quarter", "second quarter", "third quarter", "fourth quarter"]
        query_lower = query.lower()

        if any(q in query_lower for q in quarter_terms):
            filtered = [
                (i, doc) for i, doc in enumerate(self.documents)
                if any(q in doc.lower() for q in quarter_terms)
            ]
            if filtered:
                indices, filtered_docs = zip(*filtered)
                doc_embeddings = [self.doc_embeddings[i] for i in indices]
                temp_index = faiss.IndexFlatL2(doc_embeddings[0].shape[0])
                temp_index.add(np.array(doc_embeddings).astype("float32"))
                D, I = temp_index.search(query_embedding, k)
                return [filtered_docs[i] for i in I[0]]

        # Fallback to full index
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

    def build_index(self, chunks):
        self.documents = [self._annotate_units(c) for c in chunks]
        self.doc_embeddings = self.model.encode(self.documents, convert_to_tensor=False)
        dim = self.doc_embeddings[0].shape[0]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.doc_embeddings)

    def _annotate_units(self, chunk):
        chunk = re.sub(r"\$([\d.]+)\s*billion", r"\$\1 billion USD", chunk, flags=re.IGNORECASE)
        chunk = re.sub(r"\$([\d,]+)", r"\$\1 million USD", chunk)  # rough assumption
        return chunk
