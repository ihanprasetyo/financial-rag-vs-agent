from backend.baseline_openai_retriever import BaselineOpenAIRetriever
from backend.chunking import load_and_chunk

def main():
    # Load and chunk the document
    chunks = load_and_chunk("data/apple_example.txt")

    # Build the retriever
    retriever = BaselineOpenAIRetriever()
    retriever.build_index(chunks)

    # Test query
    question = "What is Apple's liquidity position?"
    top_chunks = retriever.retrieve(question, k=3)

    # Display results
    print("\n🔍 Top Retrieved Chunks:")
    for i, chunk in enumerate(top_chunks, 1):
        print(f"\n--- Chunk {i} ---\n{chunk[:300]}...")

if __name__ == "__main__":
    main()