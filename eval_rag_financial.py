# eval_rag_financial.py

import json
import time
import re
from backend.chunking import load_and_chunk
from backend.retriever import FinancialRetriever
from backend.answer_generator import generate_answer

def load_eval_set(path="eval_set_apple.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    return re.sub(r"[,\$\s]", "", text.lower())

def check_exact_match(answer, expected):
    return normalize(expected) in normalize(answer)

def main():
    data = load_eval_set()
    filepath = "data/apple_example.txt"
    chunks = load_and_chunk(filepath)

    retriever = FinancialRetriever()
    retriever.build_index(chunks)

    correct = 0
    total_time = 0

    print("\n===== RAG Evaluation (FinancialRetriever) =====")

    for i, item in enumerate(data, 1):
        q = item["question"]
        expected = item["expected_answer"]

        t0 = time.time()
        answer = generate_answer(q, retriever.retrieve(q))
        t1 = time.time()

        match = check_exact_match(answer, expected)
        correct += int(match)
        elapsed = round(t1 - t0, 2)
        total_time += elapsed

        print(f"\n🔹 Q{i}: {q}")
        print(f"🔸 Expected: {expected}")
        print(f"🔷 Answer: {answer} ({'✅' if match else '❌'}, {elapsed}s)")

    print("\n===== Final Score =====")
    print(f"✅ Accuracy: {correct}/{len(data)} ({correct/len(data)*100:.1f}%)")
    print(f"⏱️ Avg Time: {total_time/len(data):.2f}s")

if __name__ == "__main__":
    main()