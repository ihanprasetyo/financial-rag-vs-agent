import json
import time
import csv
import re
from backend.chunking import load_and_chunk
from backend.retriever import FinancialRetriever
from backend.baseline_openai_retriever import BaselineOpenAIRetriever
from backend.answer_generator import generate_answer
from backend.agent import FinanceAgent


def load_eval_set(path="eval_set.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    return re.sub(r"[,\$\s]", "", text.lower())

def run_rag(question, retriever):
    top_chunks = retriever.retrieve(question)
    return generate_answer(question, top_chunks)

def run_agent(question, filepath, retriever):
    agent = FinanceAgent(filepath)
    agent.retriever = retriever  # Inject the retriever
    result = agent.run(question)
    return result["answer"]

def check_exact_match(answer, expected):
    return normalize(expected) in normalize(answer)

def main():
    eval_data = load_eval_set()
    filepath = "data/apple_example.txt"
    chunks = load_and_chunk(filepath)

    # Init both retrievers
    retrievers = {
        "financial": FinancialRetriever(),
        "baseline": BaselineOpenAIRetriever()
    }
    for r in retrievers.values():
        r.build_index(chunks)

    results = []
    scores = {key: {"rag": 0, "agent": 0} for key in retrievers}
    times = {key: {"rag": 0.0, "agent": 0.0} for key in retrievers}

    print("\n===== RETRIEVER COMPARISON STARTED =====")

    for i, item in enumerate(eval_data, 1):
        q = item["question"]
        expected = item["expected_answer"]
        print(f"\n🧪 Q{i}: {q}\n🔹 Expected: {expected}")

        row = {"question": q, "expected": expected}

        for name, retriever in retrievers.items():
            # --- RAG ---
            t0 = time.time()
            rag_answer = run_rag(q, retriever)
            t1 = time.time()
            rag_time = round(t1 - t0, 2)
            rag_match = check_exact_match(rag_answer, expected)
            scores[name]["rag"] += int(rag_match)
            times[name]["rag"] += rag_time

            print(f"\n🔷 RAG ({name}): {rag_answer} ({'✅' if rag_match else '❌'}, {rag_time}s)")
            row[f"rag_{name}_answer"] = rag_answer
            row[f"rag_{name}_match"] = "✅" if rag_match else "❌"
            row[f"rag_{name}_time"] = rag_time

            # --- Agent ---
            t0 = time.time()
            agent_answer = run_agent(q, filepath, retriever)
            t1 = time.time()
            agent_time = round(t1 - t0, 2)
            agent_match = check_exact_match(agent_answer, expected)
            scores[name]["agent"] += int(agent_match)
            times[name]["agent"] += agent_time

            print(f"\n🔶 Agent ({name}): {agent_answer} ({'✅' if agent_match else '❌'}, {agent_time}s)")
            row[f"agent_{name}_answer"] = agent_answer
            row[f"agent_{name}_match"] = "✅" if agent_match else "❌"
            row[f"agent_{name}_time"] = agent_time

        results.append(row)

    total = len(eval_data)
    print("\n===== FINAL COMPARISON RESULTS =====")
    for name in retrievers:
        for mode in ["rag", "agent"]:
            acc = scores[name][mode] / total * 100
            avg_t = times[name][mode] / total
            print(f"{mode.upper()} + {name.title():<10} | Accuracy: {acc:.1f}% | Avg Time: {avg_t:.2f}s")

    with open("eval_compare_retrievers_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print("📄 Saved results to eval_compare_retrievers_report.csv")

if __name__ == "__main__":
    main()