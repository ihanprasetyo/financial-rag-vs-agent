# backend/agent.py

from backend.chunking import load_and_chunk
from backend.retriever import FinancialRetriever
from backend.answer_generator import generate_answer

class FinanceAgent:
    def __init__(self, doc_path):
        self.doc_path = doc_path
        self.retriever = FinancialRetriever()

    def run(self, question):
        trace = []

        # Step 1: Load and chunk the document
        trace.append("🔍 Step 1: Loading and chunking the document...")
        chunks = load_and_chunk(self.doc_path)
        trace.append(f"✅ Chunked into {len(chunks)} segments.")

        # Step 2: Build retriever and retrieve relevant chunks
        trace.append("🔍 Step 2: Retrieving relevant context...")
        self.retriever.build_index(chunks)
        top_chunks = self.retriever.retrieve(question)
        trace.append(f"✅ Retrieved top {len(top_chunks)} relevant chunks.")

        # Step 3: Generate an answer
        trace.append("💡 Step 3: Generating answer from retrieved chunks...")
        answer = generate_answer(question, top_chunks)
        trace.append("✅ Answer generated.")

        return {
            "question": question,
            "retrieved_chunks": top_chunks,
            "answer": answer,
            "trace": trace
        }