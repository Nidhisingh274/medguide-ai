# MedGuide AI — 30-Day Growth Plan

*A realistic, one-milestone-per-day roadmap taking MedGuide AI from v1.0.0 MVP toward a significantly more complete product. Each day builds on the previous one — do them in order.*

## Week 1: Observability & Quality Foundation (Days 1-7)

| Day | Milestone |
|---|---|
| 1 | Set up a free LangSmith account; add tracing to `agent/graph.py` so every run logs its full decision path |
| 2 | Review 10 real LangSmith traces; identify any routing decisions that look wrong or borderline |
| 3 | Build a small evaluation set: 15 question/expected-answer-characteristics pairs (not exact strings, just "must mention X source" style checks) |
| 4 | Write a simple script that runs the eval set against the agent and reports pass/fail |
| 5 | Tune the synthesis prompt based on eval failures found in Day 4 |
| 6 | Add unit tests for `validate_labs()` covering every branch (high/low/normal/unknown/non-numeric) using `pytest` |
| 7 | Add unit tests for the ingestion chunking logic; commit a `tests/` folder that actually runs, not just exists |

## Week 2: Expand the Knowledge Base (Days 8-14)

| Day | Milestone |
|---|---|
| 8 | Source 3-5 additional guideline PDFs on a second, related topic (e.g., hypertension in depth) |
| 9 | Re-run ingestion; verify chunk count and retrieval quality on the expanded corpus |
| 10 | Add 3-5 new lab tests + reference ranges for the new topic |
| 11 | Update `EXAMPLE_QUESTIONS` in `app.py` to cover both topics |
| 12 | Manually test 10 questions spanning both topics; document any retrieval confusion between them |
| 13 | If confusion exists, add topic-tagging to Chroma metadata and filter retrieval by inferred topic |
| 14 | Update README and architecture docs to reflect the multi-topic corpus |

## Week 3: User Feedback & Structured Output (Days 15-21)

| Day | Milestone |
|---|---|
| 15 | Set up a free Supabase project (or similar free-tier DB) for feedback storage |
| 16 | Add a thumbs up/down button under each answer in `app.py`, writing to the DB |
| 17 | Build a simple admin view (password-protected page or separate script) to review collected feedback |
| 18 | Add an optional "structured summary" output mode (condition/findings/citations as distinct fields) |
| 19 | Let the user toggle between prose and structured output |
| 20 | Add session-scoped follow-up question support (pass recent Q&A history into the synthesis prompt) |
| 21 | Test multi-turn conversations for coherence; fix any context-loss issues |

## Week 4: Polish, Scale-Readiness & Next Chapter (Days 22-30)

| Day | Milestone |
|---|---|
| 22 | Revisit the Day 9 bring-your-own-API-key idea; if pursuing it, restructure `build_graph()` to accept a per-session key |
| 23 | Test the BYOK flow thoroughly (missing key, invalid key, valid key) before shipping |
| 24 | Add a lightweight analytics view (question count, most-asked topics) using the feedback DB from Week 3 |
| 25 | Performance pass: measure and document response time per step; optimize the slowest one |
| 26 | Revisit accessibility with real assistive-tech testing (screen reader pass), not just contrast ratios |
| 27 | Write a proper CONTRIBUTING.md if opening the repo to outside contributions |
| 28 | Record a 2-3 minute demo video using the Day 1-10 demo script as a base, updated for new features |
| 29 | Write a "v2.0" blog post or LinkedIn case study documenting this 30-day extension |
| 30 | Tag a v2.0.0 GitHub release; reflect on what changed and what's next |

## How to Use This Plan

Each day is designed to take roughly the same 3-4 hour budget as the original 10-day sprint. Skipping a day is fine — just don't skip the *order* within a week, since each week builds on the last (you can't tune prompts against an eval set that doesn't exist yet, for example). Use `daily-build-prompt.md` each day to keep momentum without re-explaining context.
