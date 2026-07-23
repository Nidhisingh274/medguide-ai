# MedGuide AI — Setup Guide

**Status:** Reflects the actual environment as of Day 3. Follow this to set up the project from scratch on a new machine.

## Prerequisites

| Tool | Why it's needed |
|---|---|
| Python 3.10-3.12 | The project's runtime. Avoid 3.13 — some ML libraries (sentence-transformers/torch) may lack prebuilt wheels for it. |
| Git | Version control and the mechanism Streamlit Cloud uses to deploy (Day 9). |
| A code editor (VS Code used in this project) | Editing Python files, viewing folder structure, integrated terminal. |
| A GitHub account | Hosts the repo; required for Streamlit Community Cloud deployment. |
| A Groq API key (already obtained Day 1) | Powers the LLM — free tier, no cost. |

## 1. Clone the Repository

```
git clone https://github.com/<your-username>/medguide-ai.git
cd medguide-ai
```

## 2. Create and Activate a Virtual Environment

**Why:** Keeps this project's Python packages isolated from other projects on your machine, avoiding version conflicts.

```
python -m venv venv
```

Activate it:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

You'll know it worked when your terminal prompt starts with `(venv)`.

## 3. Install Dependencies

```
pip install -r requirements.txt
```

Current contents of `requirements.txt`:
```
streamlit
langchain
langgraph
langchain-groq
langchain-community
langchain-huggingface
chromadb
sentence-transformers
pypdf
python-dotenv
pandas
langchain-text-splitters
groq
```

**Note:** first install takes several minutes — `sentence-transformers` pulls in PyTorch, which is a large download. This is expected.

## 4. Configure Environment Variables

Create a `.env` file in the project root (never commit this file):
```
GROQ_API_KEY=your_actual_groq_key_here
```

See `ENVIRONMENT.md` for the full list of environment variables and where each is used.

## 5. Verify the Groq Connection (One-Time Check)

This was verified Day 1 via a throwaway `test_groq.py` script that prints a one-sentence response from the Groq API. If setting up fresh, recreate that script temporarily to confirm your key works before proceeding.

## 6. Run the Application

```
streamlit run app.py
```

This opens `http://localhost:8501` in your browser, showing the current Hello World foundation page. The full chat interface is built Day 7.

## 7. Run the Ingestion Pipeline (Optional — Only Needed Before Day 4)

Once source PDFs are in `data/raw_pdfs/`:
```
python ingestion/build_index.py
```

This loads and chunks the PDFs and prints a summary — it does **not** yet build the vector store (that's Day 4).

## Project Status Snapshot (End of Day 3)

- ✅ Environment fully configured
- ✅ 3 clinical PDFs sourced and chunked (302 chunks total)
- ✅ Hello World Streamlit app running
- ⏳ Vector store (Chroma) — built Day 4
- ⏳ Lab validation data — built Day 5
- ⏳ Agent logic — built Day 6
- ⏳ Full chat UI — built Day 7
