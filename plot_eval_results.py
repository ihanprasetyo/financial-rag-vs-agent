import pandas as pd
import matplotlib.pyplot as plt

# Load results
df = pd.read_csv("eval_compare_retrievers_report.csv")
total = len(df)

# Accuracy summary
acc = {
    "RAG + Financial": (df["rag_financial_match"] == "✅").sum() / total * 100,
    "RAG + Baseline": (df["rag_baseline_match"] == "✅").sum() / total * 100,
    "Agent + Financial": (df["agent_financial_match"] == "✅").sum() / total * 100,
    "Agent + Baseline": (df["agent_baseline_match"] == "✅").sum() / total * 100,
}

# Timing summary
avg_time = {
    "RAG + Financial": df["rag_financial_time"].mean(),
    "RAG + Baseline": df["rag_baseline_time"].mean(),
    "Agent + Financial": df["agent_financial_time"].mean(),
    "Agent + Baseline": df["agent_baseline_time"].mean(),
}

# --- Plot Accuracy ---
plt.figure(figsize=(8, 5))
plt.bar(acc.keys(), acc.values())
plt.title("Accuracy by Mode and Retriever")
plt.ylabel("Accuracy (%)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("accuracy_plot.png")
plt.show()

# --- Plot Latency ---
plt.figure(figsize=(8, 5))
plt.bar(avg_time.keys(), avg_time.values(), color="orange")
plt.title("Average Latency by Mode and Retriever")
plt.ylabel("Time (s)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("latency_plot.png")
plt.show()