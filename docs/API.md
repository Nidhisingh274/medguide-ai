# MedGuide AI — API Design

**Status:** Locked Day 2. Do not change without updating the PRD and Implementation Blueprint first.

## Framing Note — Read This First

A traditional "list every endpoint" exercise assumes a client-server split with HTTP routes. MedGuide AI's locked architecture (Day 1) is a **monolithic Streamlit app** — there is no separate backend server, so there are no REST endpoints. Introducing one now (e.g. a FastAPI layer) would be scope creep with no benefit to a single-user demo, and would consume time budget with no portfolio upside.

**Decision:** the internal Python function signatures are documented as the "API contract" instead, with the same rigor you'd expect from REST docs (purpose, request, response, validation, auth, error cases). This is the standard approach for a monolithic app's internal module boundaries.

## Internal Function Contracts

### `get_retriever(k=4)`
- **Module:** `agent/tools.py`
- **Purpose:** Returns a configured Chroma retriever for similarity search
- **Request:** `k: int` — number of chunks to retrieve
- **Response:** LangChain retriever object
- **Validation:** `k > 0`
- **Auth:** None (local file access only)
- **Error cases:** `chroma_store/` missing or empty → friendly error message prompting the user to re-run ingestion

### `validate_labs(test_values: dict)`
- **Module:** `agent/tools.py`
- **Purpose:** Validates submitted lab values against the reference-range table
- **Request:** `{test_name: value, ...}` — dict of test names to numeric values
- **Response:** `[{test_name, value, status, message}, ...]` — one entry per submitted test
- **Validation:** Values must be numeric
- **Auth:** None
- **Error cases:** Unknown test name → `status: "unknown_test"` with an explanatory message; never raises/crashes

### `build_graph()`
- **Module:** `agent/graph.py`
- **Purpose:** Compiles the LangGraph agent (factory function, called once per app session via `@st.cache_resource`)
- **Request:** None
- **Response:** Compiled LangGraph app object
- **Validation:** N/A
- **Auth:** None
- **Error cases:** Missing `GROQ_API_KEY` → raised at `ChatGroq` initialization, caught in `app.py` and shown as a friendly UI error

### `app.invoke(state)`
- **Module:** Called from `app.py`, defined by `build_graph()`'s compiled output
- **Purpose:** Runs the full agent for one user question — this is the closest equivalent to a single "endpoint" in this system
- **Request:** `{question: str, lab_values: dict}`
- **Response:** `{steps_log: list[str], retrieved_chunks: list[str], lab_results: list[dict], final_answer: str}`
- **Validation:** `question` must be non-empty (enforced in the Streamlit UI layer before this is called)
- **Auth:** None
- **Error cases:** Groq API failure → `safe_llm_call` (Day 8) returns a readable error string instead of crashing; empty retrieval results → `context` defaults to `"No guideline search was needed."` rather than erroring

## Summary Table

| Function | Purpose | Request | Response | Auth | Key Error Case |
|---|---|---|---|---|---|
| `get_retriever(k=4)` | Configured retriever | `k: int` | Retriever object | None | Missing vector store |
| `validate_labs(test_values)` | Lab value validation | `dict` | `list[dict]` | None | Unknown test name |
| `build_graph()` | Compile agent | None | Compiled graph | None | Missing API key |
| `app.invoke(state)` | Run one full query | `dict` | `dict` | None | Groq API failure |
