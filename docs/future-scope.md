# MedGuide AI — Future Scope

## 3 Months: Depth & Observability

- **LangSmith tracing** — full visibility into every agent decision, retrieval score, and token cost per query. Already a resume-listed skill; natural next integration.
- **Expand the document corpus** — add 5-10 more guideline PDFs covering related conditions (hypertension in depth, cardiovascular risk scoring), while keeping the same architecture.
- **Retrieval quality tuning** — experiment with chunk size/overlap and compare answer quality; currently locked at 1000/150 from Day 3, never revisited with real usage data.
- **Bring-your-own-API-key option** — deliberately scoped out during the 10-day build (Day 9) to protect stability near launch. Revisit now with proper testing time: restructure `build_graph()` so the Groq client can be created per-session rather than once at startup.

## 6 Months: Broader Domain & Real Users

- **Second condition domain** — add a parallel guideline set + lab reference table for a second condition (e.g., cardiovascular risk), proving the architecture generalizes beyond diabetes without a rewrite.
- **User feedback loop** — a lightweight thumbs up/down on each answer, logged to a free-tier database (e.g., Supabase free tier), to start building a real signal for which answers are actually useful.
- **Structured output mode** — offer an optional "clinical summary card" format (structured fields: condition, key findings, citations) alongside the current prose answer, for users who want scannable output.
- **Multi-turn conversation memory** — currently every question is stateless; add session-scoped conversation history so follow-up questions ("what about for someone with kidney disease?") work naturally.

## 12 Months: Platform Maturity

- **Multi-agent architecture** — split into specialized sub-agents (a literature-search agent, a lab-interpretation agent, a patient-education-writing agent) coordinated by a supervisor graph, directly building on LangGraph skills already demonstrated.
- **Real evaluation suite** — a small, curated set of question/expected-answer pairs (with expert-reviewed gold answers) to measure answer quality quantitatively over time, not just spot-check manually.
- **Optional authenticated mode** — for a specific pilot audience (e.g., a clinic or research team), add lightweight auth and per-user history, while keeping the current public demo mode available separately.
- **Formal disclaimer/compliance review** — if ever positioned as more than a portfolio demo, a real legal/clinical review of the "not a medical device" framing would be a prerequisite, not an afterthought.

## What Won't Change

Regardless of how far this grows, three Day-1 decisions stay: **zero-cost-to-run architecture** (free tiers only), **honest AI behavior** (say "I don't know" rather than hallucinate), and **synthetic-only lab data** (never real patient information) unless a genuine clinical partnership with proper data governance is established.
