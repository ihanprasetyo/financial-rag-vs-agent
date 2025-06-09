# compare_rag_vs_agent.py

import time
from backend.chunking import load_and_chunk
from backend.retriever import FinancialRetriever
from backend.answer_generator import generate_answer
from backend.agent import FinanceAgent

def run_rag(question, filepath):
    print("🔷 Running RAG pipeline...")
    start = time.time()

    chunks = load_and_chunk(filepath)
    retriever = FinancialRetriever()
    retriever.build_index(chunks)
    top_chunks = retriever.retrieve(question)
    answer = generate_answer(question, top_chunks)

    end = time.time()
    return {
        "answer": answer,
        "retrieved_chunks": top_chunks,
        "time": round(end - start, 2)
    }

def run_agent(question, filepath):
    print("🔶 Running Agentic pipeline...")
    start = time.time()

    agent = FinanceAgent(filepath)
    result = agent.run(question)

    end = time.time()
    result["time"] = round(end - start, 2)
    return result

# ------------- COMPARISON STARTS HERE -------------

question = "What are Apple's major sources of revenue?"
filepath = "data/apple_example.txt"

rag_result = run_rag(question, filepath)
agent_result = run_agent(question, filepath)

print("\n\n===== COMPARISON REPORT =====")
print(f"❓ Question: {question}")
print("\n--- RAG Answer ---")
print(f"(⏱️ {rag_result['time']}s)\n{rag_result['answer']}")

print("\n--- Agentic Answer ---")
print(f"(⏱️ {agent_result['time']}s)\n{agent_result['answer']}")

print("\n--- Timing Comparison ---")
print(f"RAG took {rag_result['time']}s, Agent took {agent_result['time']}s.")

print("\n✅ Comparison complete.")