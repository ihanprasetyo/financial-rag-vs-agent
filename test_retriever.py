import os
import openai

from backend.chunking import load_and_chunk
from backend.retriever import FinancialRetriever
from backend.answer_generator import generate_answer


openai.api_key = os.environ.get("OPENAI_API_KEY")

# Step 1: Load and chunk the text file
chunks = load_and_chunk("data/apple_example.txt")
print(f"Loaded {len(chunks)} chunks.")

# Step 2: Build retriever
retriever = FinancialRetriever()
retriever.build_index(chunks)

# Step 3: Ask a test question
query = "What are Apple's major sources of revenue?"
results = retriever.retrieve(query)

print("\nAnswer from GPT-3.5:")
answer = generate_answer(query, results)
print(answer)
