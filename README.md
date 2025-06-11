---

## 🧾 Project Overview

**Financial RAG + Agent** is a prototype system that compares two approaches to question answering over long, structured financial documents:

1. **Retrieval-Augmented Generation (RAG)**  
2. **Agentic Reasoning with Tool-Calling and Multi-Step Logic**

The system extracts structured insights (e.g. revenue, cash flow, debt) from public financial documents such as 10-K reports, treasury filings, and risk disclosures. It is evaluated on a curated set of 20+ numeric QA pairs for accuracy, timing, and answer quality.

---

## 🚧 Status: Work in Progress (Demo / Proof of Concept)

This is a **portfolio demo**, not a production application.  
Some features are fully implemented, while others are in progress or planned.

---

### ✅ Implemented (Working)

- 🔎 **Semantic Retriever** using `sentence-transformers` and FAISS
- 🧠 **Agentic QA Pipeline** with interpretable reasoning trace
- 📊 **Side-by-Side RAG vs Agent Evaluation** (accuracy + latency)
- 🧾 **Exact-Match QA Benchmark** on financial reporting metrics
- 📁 **Structured Report Export** to `eval_report.csv`

---

### 🧩 Partially Implemented

- 🛠️ **LangChain-style Tool Traces**  
  The agent executes retrieval → generation with printed trace; full toolchain abstraction TBD.
  
- 🧠 **Retriever Training Setup**  
  A custom retriever class is scaffolded; fine-tuning on QA pairs is planned.

---

### ☁️ Planned (Future Enhancements)

- 🧑‍💼 **Streamlit Frontend**  
  For interactive QA, answer trace display, and chunk visualization

- ☁️ **Azure Deployment**  
  Using a free-tier B1s VM with FAISS backend, Streamlit app, and Azure OpenAI GPT-3.5

- 🧪 **Enterprise Readiness Features**  
  Including chunk metadata tracking, structured logging, and cross-domain benchmarking

---

## 💡 Why This Matters

Documents like 10-Ks and regulatory filings contain dense, high-stakes information.  
Building QA systems that are:

- **Precise** (return correct numbers)
- **Transparent** (show where answers came from)
- **Flexible** (work across domains like audit, legal, compliance)

…is critical for GenAI adoption in the financial industry.

This project demonstrates how retrieval, LLM reasoning, and structured evaluation can be combined into a clear and extensible system.

---

## 📦 Technologies Used

- Python 3.10+
- FAISS (semantic vector index)
- HuggingFace `sentence-transformers`
- OpenAI GPT-3.5 (chat + completion)
- Streamlit (planned)
- Azure B1s VM (planned)
- CSV/JSON-based benchmarking and evaluation

---


## 📊 Current Evaluation Result

With the Apple 2016 financial report, the system currently achieves:

- **RAG Accuracy:** ~75%  
  (exact match on **normalized numeric answers** using a **strict substring-based evaluator** — no tolerance for rounding, rephrasing, or alternative units)  
- **Agent Accuracy:** Higher reasoning capacity but slower response time

---

## 🛠️ Potential Enhancements to Improve Accuracy, Robustness, and Generalization

### 🔍 Retriever Optimization
- Fine-tune the retriever on domain-specific QA pairs (e.g. 10-K/10-Q forms)
- Use dense retriever + reranker (e.g. `bge-base-en`, `colbert`, or `splade`)
- Index heading-based or structured chunks to improve semantic grouping

### 🧮 Answer Format Constraints
- Apply prompt constraints like:  
  *“Answer with only a number in millions. Do not include currency symbols.”*
- Add post-processing regex to extract numbers from noisy outputs
- Use function-calling format (OpenAI or Claude) to return structured fields

### 🧠 Agent Reasoning Enhancements
- Add scratchpad reasoning: “Here’s what I found. Next, I’ll...”
- Let the agent re-query or retry if insufficient data found
- Implement confidence estimation or answer validation step

### 📊 Training with Synthetic Supervision (GPT-4)
- Use GPT-4 to auto-label 1000+ QA pairs with question, answer, and relevant chunk IDs
- Train a retriever or reranker using this as weak supervision
- Optionally, use GPT as a judge to compare RAG vs Agent output quality

### 📈 Chunking Strategy Tuning
- Implement heading-aware or section-based chunking
- Use sentence/window overlap with semantic cohesion
- Auto-tune chunk size based on retrieval score coverage

### 🧪 Accuracy Evaluation Improvements
- Normalize numeric scale (e.g., "12.5B" vs "12,500")
- Use fuzzy string matching for text answers
- Incorporate GPT-based judgment for long-form or multi-hop questions

### 🛡️ Robustness & Trust
- Add citation tagging (`[chunk 3]`) to every answer
- Use groundedness scoring: “Is this answer found in retrieved chunks?”
- Detect model uncertainty: “Answer not found in retrieved content.”

---