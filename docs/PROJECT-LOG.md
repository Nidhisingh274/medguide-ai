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

Day 5 — Lab Validation Complete. Built lab_reference.csv (6 tests) and synthetic_labs.csv (3 fake sample patients). Implemented and tested validate_labs() in agent/tools.py — 4 test cases pass, including graceful handling of an unknown test. Confirmed get_retriever() (Day 4) has no regressions. Zero-cost, no API keys used. Both core tools now ready for Day 6's agent to import.

Day 6 — MVP Complete. Built the LangGraph agent (agent/graph.py, agent/prompts.py) with conditional routing between guideline search and lab validation. Rebuilt app.py into the full chat UI with question input, lab form, live step tracker, citations, lab validation detail, and the required AB Talks Challenge footer. Fixed two bugs: a Chroma multi-connection crash (retriever now built once) and a wrong-Python-environment issue (now launching via python -m streamlit run). Verified end-to-end in the browser — full MVP working locally. Day 6 and Day 7 blueprint milestones compressed into one day per approval; Day 8 hardening and Day 9 deployment remain as separately scheduled.