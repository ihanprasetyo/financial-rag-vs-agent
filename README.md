---

## 🧾 Project Overview

**Financial RAG + Agent** is a prototype system that compares two approaches to question answering over long, structured financial documents:

1. **Retrieval-Augmented Generation (RAG)**  
2. **Agentic Reasoning with Tool-Calling and Multi-Step Logic**

The system extracts structured insights (e.g. revenue, cash flow, debt) from public financial documents such as 10-K reports, treasury filings, and risk disclosures. It is evaluated on a curated set of numeric QA pairs for accuracy, timing, and answer quality.

---

## 💡 Potential Use Cases

This project demonstrates how Retrieval-Augmented Generation (RAG) and basic agentic reasoning can be applied to real-world finance workflows.

### ✅ Practical Applications

1. **Confidential Document QA**  
   Can be deployed internally at scale to answer questions over confidential company documents (e.g. treasury reports, audit filings) — without uploading files externally.

2. **Integrated Financial Analysis**  
   Can be extended to connect with structured or relational databases (e.g. SQL, Excel exports) for faster, automated analysis — especially useful for CFOs, controllers, and treasury teams.

3. **Format-Agnostic by Design**  
   Many financial reports follow similar templates (e.g. 10-Ks, annual reports, filings), so high performance can be achieved without needing extreme reasoning or complex parsing logic.


## 🚀 Status: Live Demo Deployed on Azure

This is a **portfolio demo**, publicly deployed and running on an Azure B1s Linux VM:  
🔗 [**Live App** (Streamlit)](http://20.199.160.183:8501/)

Core features like RAG retrieval, GPT-3.5 QA, FAISS index, and a working frontend are fully implemented.  
Agent logic, retriever training, and advanced evaluation remain in progress.

⚠️ **Note:** This demo runs on a low-cost Azure VM with limited memory and compute.  
As a result, response times may be very slow or unstable, and accuracy might be low.  
For production use:
- Scale up to a larger cloud instance (e.g., Azure Standard B2s or above)
- Integrate a more capable LLM (e.g., GPT-4-turbo or fine-tuned domain-specific model)

---

### ✅ Implemented (Working)

- 🔎 **Semantic Retriever** using `sentence-transformers` and FAISS
- 🧠 **RAG Pipeline** with chunk retrieval + GPT-3.5 generation
- 🖥️ **Streamlit Frontend** hosted on public Azure IP (B1s VM)
- ☁️ **Azure Deployment** with persistent FAISS index and secure `.env` API key
- 📁 **Local Financial Reports** stored securely on VM and indexed at runtime

---

### 🧩 Partially Implemented

- 🛠️ **Agentic QA Pipeline** with multi-step reasoning scaffolding (logic WIP)
- 🧠 **Retriever Training Setup** (planned for fine-tuning on QA pairs)
- 📊 **Evaluation Script** (`eval_rag_financial.py`) to be added
- 📄 **Structured Logging + Chunk Metadata** (placeholder only)

---

### ☁️ Potential Expansion

- 🧑‍💼 **LangChain-style Agent Execution** with interpretable traces
- 📊 **Side-by-Side RAG vs Agent Evaluation**
- 🧾 **Exact-Match QA Benchmark** and report export to CSV
- 🧪 **Enterprise Readiness Features** — auto-scaling, retries, monitoring

---

## 📦 Technologies Used

- **Python 3.10+**
- **FAISS** — Semantic vector index for fast retrieval
- **HuggingFace `sentence-transformers`** — Embedding generation for chunk retrieval
- **OpenAI GPT-3.5** — Used via `openai` Python SDK for chat-based generation
- **LangChain (light usage)** — Used for a modular, interpretable answer generation pipeline
- **Streamlit** — Lightweight frontend for user interaction and live QA
- **Azure B1s Linux VM** — Hosting the app with persistent FAISS index and secure `.env` access
- **CSV / JSON** — Benchmarking, QA evaluation, and result storage

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