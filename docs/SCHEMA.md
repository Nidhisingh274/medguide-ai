# MedGuide AI — Data Schema

**Status:** Locked Day 2. Do not change without updating the PRD and Implementation Blueprint first.

## Framing Note

This project does **not** use a traditional relational or document database (no Postgres/MySQL/MongoDB). That is an intentional Day 1 decision, not an oversight — there are no user accounts and no multi-user data to manage. Storage is split between a **vector store (Chroma)** and **flat CSV files**.

## 1. Collection: Chroma `medguide_docs`

Auto-created by `Chroma.from_documents()` in `ingestion/build_index.py`.

| Field | Type | Description | Constraint |
|---|---|---|---|
| `id` | string (auto) | Chroma-generated unique chunk ID | Auto, unique |
| `page_content` | text | The chunk's raw text (~1000 chars) | Non-empty |
| `metadata.source` | string | Source PDF filename | Required |
| `metadata.chunk_id` | integer | Position of chunk within its source doc | Required, ≥ 0 |
| `embedding` | vector(384) | MiniLM-L6-v2 embedding, auto-generated | 384 dimensions |

**Validates against:** PRD Feature 6.1 (Agentic Research Q&A) — every chunk carries its source filename, which is exactly what enables cited answers.

## 2. Table (CSV): `data/lab_reference.csv`

| Field | Type | Description | Constraint |
|---|---|---|---|
| `test_name` | string | e.g. "Fasting Glucose" | **Primary key** — unique, matched case-insensitively at query time |
| `unit` | string | e.g. "mg/dL" | Required |
| `low` | float | Lower bound of normal range | Required; `low < high` |
| `high` | float | Upper bound of normal range | Required |
| `notes` | string | Plain-English clinical note | Optional |

## 3. Table (CSV): `data/synthetic_labs.csv`

| Field | Type | Description | Constraint |
|---|---|---|---|
| `patient_id` | string | e.g. "SYN-001" | Must start with `SYN-` (enforces "clearly fake" rule from PRD) |
| `test_name` | string | Foreign key → `lab_reference.test_name` | Should exist in reference table; if not, `validate_labs()` returns `status: "unknown_test"` gracefully rather than enforcing a hard constraint |
| `value` | float | The lab value | Required, numeric |

**Note on referential integrity:** CSVs can't enforce foreign keys at the storage layer. This is enforced at the *application* layer instead, inside `validate_labs()` (Day 5 of the Implementation Blueprint) — the correct, minimal-effort choice given there's no DB engine in this architecture.

## 4. Schema Validation Against PRD User Stories

| PRD Requirement | Covered By | Status |
|---|---|---|
| 6.1 Agentic Research Q&A — cited answers | `medguide_docs.metadata.source` | ✅ Covered |
| 6.2 Lab Value Validation — flag anomalies | `lab_reference.csv` (ranges) + `synthetic_labs.csv` (sample data) | ✅ Covered |
| Out-of-scope: no user accounts/auth | No `users` table exists | ✅ Correctly absent |
| Out-of-scope: no persisted chat history | No `conversations`/`messages` table exists | ✅ Correctly absent |
| Out-of-scope: no real patient data | `synthetic_labs.csv` uses `SYN-` prefixed fake IDs only | ✅ Enforced by convention |

No schema gaps found against any PRD user story.
