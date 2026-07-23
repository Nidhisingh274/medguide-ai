# MedGuide AI — Project Log

## Day 3 — Foundation Complete
- Installed remaining dependencies (`pypdf`, `langchain-text-splitters`).
- Built and verified a running Hello World Streamlit app (`app.py`).
- Locked clinical topic: Type 2 Diabetes.
- Sourced 3 clinical PDFs (~256,000 characters combined) into `data/raw_pdfs/`.
- Built and tested the ingestion/chunking pipeline — **302 chunks** produced, all verified clean.
- Updated `SETUP.md`, `ENVIRONMENT.md`, `PROJECT-STRUCTURE.md`; added `DAY3-SUMMARY.md`.
- Day 4 (embeddings + Chroma vector store) ready to begin.

Day 4 — Embeddings & Vector Store Complete. Embedded all 302 chunks using sentence-transformers/all-MiniLM-L6-v2, stored in a persisted Chroma vector store. Built and tested get_retriever() in agent/tools.py — verified with two independent queries returning correctly-sourced, relevant results. Swapped deprecated langchain_community Chroma import for langchain_chroma. RAG half of the product is complete. Day 5 ready to begin: synthetic lab data + reference-range validation.