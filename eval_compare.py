import json
import time
import csv
import re
from backend.chunking import load_and_chunk
from backend.retriever import FinancialRetriever
from backend.answer_generator import generate_answer
from backend.agent import FinanceAgent

def load_eval_set(path="eval_set.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    return re.sub(r"[,\$\s]", "", text.lower())

def run_rag(question, filepath):
    chunks = load_and_chunk(filepath)
    retriever = FinancialRetriever()
    retriever.build_index(chunks)
    top_chunks = retriever.retrieve(question)
    answer = generate_answer(question, top_chunks)
    return answer

def run_agent(question, filepath):
    agent = FinanceAgent(filepath)
    result = agent.run(question)
    return result["answer"]

def check_exact_match(answer, expected_answer):
    return normalize(expected_answer) in normalize(answer)

def main():
    eval_data = load_eval_set()
    filepath = "data/apple_example.txt"

    rag_correct, agent_correct = 0, 0
    rag_total_time, agent_total_time = 0, 0

    results = []

    print("\n===== EVALUATION STARTED =====")

    for i, item in enumerate(eval_data, 1):
        q = item["question"]
        expected = item["expected_answer"]

        print(f"\n🧪 Question {i}: {q}")
        print(f"🔹 Expected answer: {expected}")

        # RAG
        start_rag = time.time()
        rag_answer = run_rag(q, filepath)
        end_rag = time.time()
        rag_time = round(end_rag - start_rag, 2)
        rag_match = check_exact_match(rag_answer, expected)
        if rag_match: rag_correct += 1
        rag_total_time += rag_time

        # Agent
        start_agent = time.time()
        agent_answer = run_agent(q, filepath)
        end_agent = time.time()
        agent_time = round(end_agent - start_agent, 2)
        agent_match = check_exact_match(agent_answer, expected)
        if agent_match: agent_correct += 1
        agent_total_time += agent_time

        # Print answers
        print(f"\n🔷 RAG Answer ({'✅' if rag_match else '❌'}, {rag_time}s):")
        print(rag_answer)

        print(f"\n🔶 Agent Answer ({'✅' if agent_match else '❌'}, {agent_time}s):")
        print(agent_answer)

        # Save row
        results.append({
            "question": q,
            "expected": expected,
            "rag_answer": rag_answer,
            "rag_match": "✅" if rag_match else "❌",
            "rag_time": rag_time,
            "agent_answer": agent_answer,
            "agent_match": "✅" if agent_match else "❌",
            "agent_time": agent_time
        })

    total = len(eval_data)
    print("\n===== FINAL RESULTS =====")
    print(f"✅ RAG   Accuracy: {rag_correct}/{total} ({(rag_correct/total)*100:.1f}%)")
    print(f"✅ Agent Accuracy: {agent_correct}/{total} ({(agent_correct/total)*100:.1f}%)")
    print(f"⏱️ Avg RAG time:   {rag_total_time/total:.2f}s")
    print(f"⏱️ Avg Agent time: {agent_total_time/total:.2f}s")

    # Write CSV
    with open("eval_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "question", "expected",
            "rag_answer", "rag_match", "rag_time",
            "agent_answer", "agent_match", "agent_time"
        ])
        writer.writeheader()
        writer.writerows(results)
    print("📄 Saved results to eval_report.csv")

if __name__ == "__main__":
    main()