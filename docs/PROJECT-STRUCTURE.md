# MedGuide AI — Project Structure

**Status:** Updated Day 3 to reflect actual implementation state. Do not change the overall shape without updating the PRD and Implementation Blueprint first.

## Folder Structure (Current, End of Day 3)

```
medguide-ai/
├── app.py                  # Streamlit entrypoint — Hello World foundation running (full UI: Day 7)
├── agent/                  # All agent/orchestration logic lives here, isolated from UI code
│   ├── __init__.py
│   ├── graph.py             # LangGraph StateGraph — empty, built Day 6
│   ├── tools.py             # ✅ POPULATED Day 4 — get_retriever() implemented and tested
│   └── prompts.py           # Prompt text — empty, built Day 6
├── ingestion/               # Offline/setup-time scripts — never called at runtime by app.py
│   ├── __init__.py
│   └── build_index.py       # ✅ UPDATED Day 4 — embedding + Chroma storage added
├── data/                    # All static/source data — no code
│   ├── raw_pdfs/             # ✅ POPULATED Day 3 — 3 clinical PDFs on Type 2 Diabetes
│   │   ├── bmc_diabetes_clinical_practice.pdf
│   │   ├── cdc_diabetes_referral_strategies.pdf
│   │   └── frontiers_diabetes_cardiovascular_care.pdf
│   ├── lab_reference.csv    # Empty, built Day 5
│   └── synthetic_labs.csv   # Empty, built Day 5
├── docs/                    # Design + setup artifacts
│   ├── ARCHITECTURE.md
│   ├── SCHEMA.md
│   ├── API.md
│   ├── UI-WIREFRAMES.md
│   ├── PROJECT-STRUCTURE.md  # this file
│   ├── SETUP.md              # ✅ NEW Day 3
│   ├── ENVIRONMENT.md        # ✅ NEW Day 3
│   ├── DAY3-SUMMARY.md       # ✅ NEW Day 3
│   └── screenshots/          # populated Day 10
├── chroma_store/            # Not yet created — built Day 4, gitignored until Day 9
├── tests/                   # Reserved for Day 8 testing work
├── requirements.txt          # ✅ UPDATED Day 3 — added pypdf, langchain-text-splitters
├── .env                     # Local secrets, gitignored — never committed
├── .gitignore
└── README.md
```

## Change Log Since Day 2

- **Topic decided:** Type 2 Diabetes management (drives PDF selection and will drive Day 5's lab test selection: glucose, HbA1c, cholesterol, blood pressure)
- **3 PDFs used, not 5:** within the Day 1 blueprint's "3-5 documents" guidance — not a deviation, just the specific number chosen given document length (~256,000 characters combined, which is substantial)
- **`ingestion/build_index.py` fully implemented** for the load + chunk stage (embedding + Chroma storage still pending, Day 4)
- **`app.py` has a working Hello World page** — added as a Day 3 foundation milestone, not originally itemized in the Day 1 blueprint's Day 3 section, but consistent with "Day 3 Readiness"-style foundation work

## Change Log — Day 4

- **`ingestion/build_index.py` completed** — now embeds all 302 chunks using `sentence-transformers/all-MiniLM-L6-v2` and stores them in a persisted Chroma store at `chroma_store/`
- **`agent/tools.py` completed** — `get_retriever(k=4)` implemented and tested with two different queries, both returning correctly-sourced, relevant results
- **Package swap:** `langchain_community.vectorstores.Chroma` (deprecated) replaced with `langchain_chroma.Chroma` (current) in both files — added `langchain-chroma` to `requirements.txt`
- The RAG half of the product (PDFs → chunks → embeddings → Chroma → retriever) is now fully functional and verified

## Rationale Per Folder

| Folder/File | Responsibility | Why it's structured this way |
|---|---|---|
| `app.py` | Entire UI layer | Single entrypoint keeps the "frontend" trivially easy to find — no routing/pages needed given the single-screen design |
| `agent/` | Orchestration + reasoning | Isolated from UI code so the agent logic could theoretically be tested or reused independently of Streamlit |
| `agent/graph.py` | The LangGraph state machine | Kept separate from `tools.py` so the *flow* (who calls whom) is readable independently of the *implementation* of each tool |
| `agent/tools.py` | Retriever + validator functions | Both tools live together since they're both "things the agent can call," even though their internals are unrelated |
| `agent/prompts.py` | All prompt text | Centralizing prompts means tuning wording never requires touching graph logic — reduces risk of breaking the state machine while iterating on answer quality |
| `ingestion/` | One-time/offline processing | Physically separated from `agent/` to make it obvious this code runs at setup time, not at request time — prevents accidentally calling ingestion logic from the live app |
| `data/` | All static content | Pure data, no code — keeps source PDFs and CSVs easy to find/update without touching any script |
| `docs/` | All design + reference documentation | New as of Day 2 — this is where every architectural decision lives so any future AI conversation (or Nidhi, months later) can reconstruct the whole system without re-reading code |
| `chroma_store/` | Persisted vector DB | Generated, not hand-written — treated as a build artifact (gitignored until deployment requires committing it on Day 9) |
| `tests/` | Test scripts | Reserved specifically for Day 8's structured testing pass — kept empty until then to avoid untested scaffolding |

## Where Future Code Will Live

- **Days 3-4** (ingestion, embeddings): `ingestion/build_index.py`, reading from `data/raw_pdfs/`, writing to `chroma_store/`
- **Day 5** (validation): `data/lab_reference.csv`, `data/synthetic_labs.csv`, functions added to `agent/tools.py`
- **Day 6** (agent): `agent/graph.py`, `agent/prompts.py`
- **Day 7** (UI): `app.py`
- **Day 8** (testing): `tests/`, plus hardening edits inside `agent/graph.py` and `app.py`
- **Day 9** (deployment): no new files — `chroma_store/` gets committed, `.gitignore` updated
- **Day 10** (polish): `README.md`, `docs/screenshots/`

This structure was chosen to mirror the system architecture's component boundaries exactly — each folder maps to one box in the Architecture diagram, so there's never ambiguity about where a new piece of code belongs.
