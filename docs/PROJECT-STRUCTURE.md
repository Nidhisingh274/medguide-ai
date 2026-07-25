# MedGuide AI — Project Structure

**Status:** Updated Day 6 to reflect actual implementation state. Do not change the overall shape without updating the PRD and Implementation Blueprint first.

## Folder Structure (Current, End of Day 6)

```
medguide-ai/
├── app.py                  # ✅ POPULATED Day 6 — full chat UI, lab form, step tracker, footer
├── agent/                  # All agent/orchestration logic lives here, isolated from UI code
│   ├── __init__.py
│   ├── graph.py             # ✅ POPULATED Day 6 — LangGraph StateGraph, retriever built once (Chroma fix)
│   ├── tools.py             # ✅ Day 4: get_retriever() — ✅ Day 5: validate_labs() added
│   └── prompts.py           # ✅ POPULATED Day 6 — ROUTER_PROMPT, SYNTHESIS_PROMPT
├── ingestion/               # Offline/setup-time scripts — never called at runtime by app.py
│   ├── __init__.py
│   └── build_index.py       # ✅ UPDATED Day 4 — embedding + Chroma storage added
├── data/                    # All static/source data — no code
│   ├── raw_pdfs/             # ✅ POPULATED Day 3 — 3 clinical PDFs on Type 2 Diabetes
│   │   ├── bmc_diabetes_clinical_practice.pdf
│   │   ├── cdc_diabetes_referral_strategies.pdf
│   │   └── frontiers_diabetes_cardiovascular_care.pdf
│   ├── lab_reference.csv    # ✅ POPULATED Day 5 — 6 lab tests with reference ranges
│   └── synthetic_labs.csv   # ✅ POPULATED Day 5 — 3 synthetic sample patients (SYN- prefixed)
├── docs/                    # Design + setup artifacts
│   ├── ARCHITECTURE.md
│   ├── SCHEMA.md
│   ├── API.md
│   ├── UI-WIREFRAMES.md
│   ├── PROJECT-STRUCTURE.md  # this file
│   ├── SETUP.md              # ✅ NEW Day 3
│   ├── ENVIRONMENT.md        # ✅ NEW Day 3
│   ├── DAY3-SUMMARY.md       # ✅ NEW Day 3
│   ├── DAY4-SUMMARY.md       # ✅ NEW Day 4
│   ├── DAY5-SUMMARY.md       # ✅ NEW Day 5
│   ├── DAY6-SUMMARY.md       # ✅ NEW Day 6
│   └── screenshots/          # populated Day 10
├── chroma_store/            # Not yet created — built Day 4, gitignored until Day 9
├── tests/                   # Reserved for Day 8 testing work
├── requirements.txt          # ✅ UPDATED Day 3 (pypdf, langchain-text-splitters) + Day 4 (langchain-huggingface, chromadb, langchain-chroma, sentence-transformers)
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

## Change Log — Day 5

- **`data/lab_reference.csv` created** — 6 lab tests (Fasting Glucose, HbA1c, LDL/HDL Cholesterol, Triglycerides, Systolic Blood Pressure) with reference ranges, matching the Type 2 Diabetes topic
- **`data/synthetic_labs.csv` created** — 3 clearly-fake sample patients (`SYN-001` to `SYN-003`) with test values spanning normal and abnormal cases
- **`agent/tools.py` extended** — `validate_labs()` added alongside `get_retriever()`; tested together in the same run to confirm no regression to Day 4's retriever
- The second core feature (lab validation) is now fully functional and verified — both PRD features (6.1 Research Q&A, 6.2 Lab Validation) have working backing logic. Only the agent orchestration (Day 6) and UI (Day 7) remain to connect them into the full product.

## Change Log — Day 6

- **`agent/prompts.py` created** — ROUTER_PROMPT (classifies intent) and SYNTHESIS_PROMPT (writes the final cited answer)
- **`agent/graph.py` created** — full LangGraph StateGraph wiring together classify_intent → search_guidelines / check_labs → synthesize_answer, with conditional routing
- **Bug found and fixed:** Chroma throws a `RustBindingsAPI` error if a second connection to the same persisted store is opened in one running process. Fixed by building the retriever once inside `build_graph()` instead of on every question — verified with a 3-question test run in the same process.
- **`app.py` fully rebuilt** — Hello World replaced with the complete chat UI: question box, optional lab value form, live step tracker, cited answer, lab validation detail, guideline excerpts expander, sidebar, and the required challenge footer
- **Environment issue found and fixed:** on this machine, the plain `streamlit run` command could launch Anaconda's global Python instead of the project's venv, causing a false `ModuleNotFoundError`. Fixed by always launching via `python -m streamlit run app.py`, which forces the active venv's Python to be used.
- **Day 6/7/9 blueprint compression:** per explicit approval, today combined the originally-separate Day 6 (agent) and Day 7 (UI) blueprint milestones into one day, since foundation work was ahead of schedule. Deployment (originally Day 9) was NOT pulled forward — still scheduled separately. Day 8's dedicated hardening pass (deeper edge-case testing) also still stands, even though basic error handling (`safe_llm_call`, try/except in the UI) was included today so the live demo doesn't crash.
- **MVP milestone reached:** all core features (Q&A with citations, lab validation, visible agent reasoning) now work together in one running application, verified end-to-end in the browser.

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
