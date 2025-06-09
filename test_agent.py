# test_agent.py

from backend.agent import FinanceAgent

agent = FinanceAgent("data/solvency_example.txt")
result = agent.run("At which % is SCR calibration done?")

print("\n--- AGENT REASONING TRACE ---")
for step in result["trace"]:
    print(step)

print("\n--- TOP RETRIEVED CHUNKS ---")
for i, chunk in enumerate(result["retrieved_chunks"], 1):
    print(f"\n[Chunk {i}]\n{chunk[:300]}...")

print("\n--- FINAL ANSWER ---")
print(result["answer"])