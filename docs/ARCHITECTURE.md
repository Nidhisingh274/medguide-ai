# MedGuide AI — System Architecture

**Status:** Locked Day 2. Do not change without updating the PRD and Implementation Blueprint first.

## 1. Overview

MedGuide AI is a **monolithic Streamlit application** — there is no separate backend server. `app.py` calls a LangGraph agent in-process, which calls two tools (a retriever and a validator) and one external API (Groq). The vector store is built once, offline, by `ingestion/build_index.py`, and only *read* at runtime.

## 2. Component Diagram

```mermaid
graph TD
    U[User Browser] -->|HTTPS| ST["Streamlit App (app.py)"]
    ST --> LG["LangGraph Agent (agent/graph.py)"]
    LG --> RT["Retriever Tool (agent/tools.py)"]
    LG --> VAL["Validator Tool (agent/tools.py)"]
    LG --> GROQ["Groq LLM API (llama-3.3-70b)"]
    RT --> CHROMA[("Chroma Vector Store\nchroma_store/")]
    VAL --> CSV[("lab_reference.csv")]
    ING["ingestion/build_index.py"] -->|builds at setup time| CHROMA
    PDFS[("data/raw_pdfs/*.pdf")] --> ING
    EMB["HuggingFace Embeddings\n(all-MiniLM-L6-v2)"] --> ING
```

## 3. Data Flow

### 3.1 Ingestion-time flow (run once, before deployment — not per user request)

```mermaid
flowchart LR
    A[PDF files in data/raw_pdfs/] --> B[Extract text - pypdf]
    B --> C[Chunk text - RecursiveCharacterTextSplitter]
    C --> D[Embed chunks - HuggingFace model]
    D --> E[(Store in Chroma - chroma_store/)]
```

### 3.2 Query-time flow (runs on every user question)

```mermaid
flowchart LR
    A[User question + optional lab values] --> B[LangGraph: classify_intent]
    B --> C{Needs search?}
    C -->|Yes| D[Query Chroma for relevant chunks]
    C -->|No| E{Needs validation?}
    D --> E
    E -->|Yes| F[Validate lab values vs reference ranges]
    E -->|No| G[Synthesize answer via Groq]
    F --> G
    G --> H[Return answer + steps_log to UI]
```

## 4. Request Lifecycle (Sequence Diagram)

```mermaid
sequenceDiagram
    participant U as User
    participant S as Streamlit UI
    participant G as LangGraph Agent
    participant R as Retriever (Chroma)
    participant V as Validator (CSV)
    participant L as Groq LLM

    U->>S: Enter question + optional lab values, click Ask
    S->>G: app.invoke({question, lab_values})
    G->>L: classify_intent(question)
    L-->>G: SEARCH: true/false, VALIDATE: true/false
    alt needs_search
        G->>R: similarity_search(question, k=4)
        R-->>G: retrieved_chunks [with source metadata]
    end
    alt needs_validation
        G->>V: validate_labs(lab_values)
        V-->>G: lab_results [status + message per test]
    end
    G->>L: synthesize_answer(question, context, lab_results)
    L-->>G: final_answer (cited, plain-English)
    G-->>S: {steps_log, retrieved_chunks, lab_results, final_answer}
    S-->>U: Render step tracker, answer, validation detail
```

## 5. AI Interaction — Agent State Machine

```mermaid
stateDiagram-v2
    [*] --> classify_intent
    classify_intent --> search_guidelines: needs_search
    classify_intent --> check_labs: validation only
    classify_intent --> synthesize_answer: neither needed
    search_guidelines --> check_labs: also needs_validation
    search_guidelines --> synthesize_answer: search only
    check_labs --> synthesize_answer
    synthesize_answer --> [*]
```

## 6. External Services

| Service | Purpose | When called | Free tier limits to be aware of |
|---|---|---|---|
| Groq API | LLM inference (routing + synthesis) | Every user query | Rate limits apply — handled via `safe_llm_call` (Day 8) |
| HuggingFace Hub | Download embedding model | Once, at first run/deploy | Model cached locally after first download |
| GitHub | Source control, triggers deployment | Every `git push` | None (public repo) |
| Streamlit Community Cloud | Hosting | Continuous (live app) | App may sleep after inactivity — noted in README |

## 7. Why This Architecture (Not a Client-Server Split)

A traditional frontend/backend/database split was deliberately rejected on Day 1:

- **No user accounts** → no need for a database or auth layer
- **Single-user demo, not a multi-tenant product** → a separate REST API server would add operational complexity (hosting, CORS, auth tokens) with zero benefit
- **Time budget is 3-4 hrs/day for 10 days** → every architectural layer we don't need is time we can't afford to spend

This is a monolith by design, not by oversight.
