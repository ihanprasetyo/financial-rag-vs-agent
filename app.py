import streamlit as st
import time
import os
from backend.chunking import load_and_chunk
from backend.retriever import FinancialRetriever
from backend.answer_generator import generate_answer
from backend.agent import FinanceAgent

# Preloaded reports
PRELOADED_REPORTS = {
    "Apple 2016": "data/apple_example.txt",
    "Simulated Company": "data/simulated_example.txt"
}

st.title("Financial Report Q&A Assistant")
st.write("Select a preloaded financial report and ask questions using RAG or Agentic reasoning.")

st.markdown(
    """
    ### ⚠️ Note  
    This is a prototype system running on a low-cost Azure VM (B1s tier).  
    Response time and model accuracy may vary due to resource limits.  
    """
)

# 1. Disabled Upload TXT file input (demo only)
st.file_uploader("Upload a financial report (.txt) - Disabled in demo", disabled=True, help="Upload disabled in demo version. Use preloaded reports.")

# 2. Choose report from preloaded only
report_name = st.selectbox("Choose report:", list(PRELOADED_REPORTS.keys()))

# 3. Question input
question = st.text_input("Ask a question about the report, for example: What is the company's Net sales in 2016?")

mode = st.radio("Choose reasoning method:", ["RAG", "Agent"])

if st.button("Get Answer") and question.strip():
    filepath = PRELOADED_REPORTS[report_name]
    chunks = load_and_chunk(filepath)
    retriever = FinancialRetriever()
    retriever.build_index(chunks)

    start = time.time()


    if mode == "RAG":
        answer = generate_answer(question, retriever.retrieve(question))
    else:
        agent = FinanceAgent(filepath)
        answer = agent.run(question)["answer"]

    end = time.time()

    st.markdown(f"### Answer:")
    st.write(answer)
    st.markdown(f"_Inference time: {end - start:.2f} seconds_")

    # Add official report link right below the answer
    st.markdown(
        """
        ---
        You can compare the answer to the official Apple consolidated financial statements here:  
        [Apple Q4 FY16 Consolidated Financial Statements (PDF)](https://www.apple.com/newsroom/pdfs/Q4FY16ConsolidatedFinancialStatements.pdf)
        """
    )

st.markdown("---")
st.markdown("[GitHub Repo](https://github.com/ihanprasetyo/financial-rag-vs-agent) - Demo project by ihanprasetyo")