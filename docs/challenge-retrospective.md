# MedGuide AI — Challenge Retrospective

*A day-by-day account of building MedGuide AI during the AB Talks 60-Day Claude AI Challenge capstone.*

## The Timeline

**Day 1 — Discovery.** Started with no fixed idea. Interview-style discovery surfaced a real asset: hands-on clinical data validation experience at ICMR, including COVID-era work processing 75,000+ diagnostic records a month. That became the seed for the whole project — not "build any AI app," but "build the AI version of a problem I've actually solved by hand." Landed on an agentic RAG assistant combining cited research Q&A with lab-value validation, scoped tightly for a 3-4 hr/day, 10-day budget.

**Day 2 — System Design.** Locked the architecture before writing implementation code: LangGraph agent, Chroma vector store, Hugging Face embeddings, Groq LLM, Streamlit UI — all free-tier. Wrote the PRD, architecture diagrams, schema, API contracts (recognizing early there'd be no REST layer, just internal function contracts, since the app is intentionally monolithic), and UI wireframes.

**Day 3 — Foundation.** Environment setup, Git/GitHub from scratch, and the PDF ingestion/chunking pipeline. Chose Type 2 Diabetes as the clinical focus — deliberately, because it pairs naturally with concrete lab tests (glucose, HbA1c, cholesterol) for the validation feature later. Sourced 3 real clinical PDFs, chunked into 302 pieces.

**Day 4 — Retrieval.** Embedded all 302 chunks with a free local Hugging Face model and built the Chroma vector store. Verified retrieval quality with two independent test queries before trusting it.

**Day 5 — Validation.** Built the lab reference-range table and synthetic (clearly-fake) sample data, then `validate_labs()` — tested against high, normal, and unknown-test cases in the same run that re-verified Day 4's retriever, catching regressions early as a habit, not an afterthought.

**Day 6 — The MVP, and the first real bug.** Wired both tools into a LangGraph agent and built the full chat UI in one compressed session. Hit a genuine production bug here: the Chroma vector store crashed with a `RustBindingsAPI` error on the *second* question asked in the same running app — because the retriever was being rebuilt fresh every time instead of once. Fixed by building it once when the agent starts. A second, unrelated bug surfaced minutes later: the local machine's `streamlit run` command was silently launching Anaconda's global Python instead of the project's virtual environment, causing a false "module not found" error. Both fixed and documented so they wouldn't resurface.

**Day 7 — Design, and a deployment surprise.** Opened the day expecting to build a UI — and discovered the app was *already live* on Streamlit Community Cloud, deployed ahead of schedule via Streamlit's own "Deploy" button. Pivoted the day into a full UX refinement pass instead: teal branding matching the pitch deck, example-question chips, styled step-tracker pills, color-coded lab result cards. Hit a Streamlit `session_state` quirk where a widget's `key` silently overrides its `value` — fixed by writing directly into session state instead.

**Day 8 — Hardening.** A deliberate, thorough Senior QA pass: 11 real issues found and fixed, not cosmetic ones. The most important: lab value inputs silently defaulted to `0.0`, meaning a forgotten field could produce a false "LOW" reading — invisible until specifically tested for. Also closed an HTML-injection risk (citation text from PDFs was being inserted into raw HTML unescaped), pinned every dependency to an exact tested version, and ran a real WCAG contrast audit that caught 2 of 7 custom colors failing accessibility standards.

**Day 9 — Release Readiness.** Added an MIT license, GitHub topics, and repo metadata. Had an honest conversation about a proposed per-session rate limit to protect the shared API quota — and made a deliberate, reasoned decision *not* to add it, because it would have been trivially bypassed by refreshing the page, and the added complexity wasn't worth a safeguard that wasn't actually robust. That "no" was as much a real engineering decision as any "yes" earlier in the build.

**Day 10 — Graduation.** Final polish, portfolio materials, and this document.

## Major Technical Decisions & Pivots

- **Monolith over microservices**: no separate backend, explicitly justified against the PRD's "no user accounts" scope, not a default.
- **Combining Day 6 + Day 7's original blueprint milestones** into one session when foundation work ran ahead of schedule — a deliberate schedule compression, approved and documented, not scope creep.
- **Declining to build a bring-your-own-API-key feature** on Day 9, after scoping it out loud, because it required restructuring core agent construction two days before the finish line.

## Challenges Solved & Debugging Moments

1. The Chroma multi-connection crash (Day 6) — only reproducible by asking a *second* question, a good reminder that one successful test isn't proof of correctness.
2. The wrong-Python-environment bug (Day 6) — an environment issue masquerading as a code issue.
3. The Streamlit `key`/`value` conflict (Day 7) — a framework-specific gotcha, not a logic bug.
4. The silent `0.0` lab-value bug (Day 8) — the kind of bug that never crashes, just quietly produces wrong output, which is often more dangerous than one that does.
5. A false alarm on Day 9 — a stale cached GitHub fetch suggested a deleted file had reappeared; resolved by trusting `git status` over a possibly-stale web fetch, a useful lesson in verifying against the most reliable source available.

## Skills Demonstrated

Requirements discovery and scope protection · system architecture design · RAG pipeline construction (chunking, embeddings, vector search) · agentic orchestration with LangGraph and conditional routing · prompt engineering for groundedness and honesty · full-stack Streamlit development · UI/UX design systems · production hardening (error handling, input validation, security, accessibility) · dependency management · Git/GitHub workflows including merge conflict resolution · deployment and release management · technical writing and documentation discipline.

## Final Project Summary

MedGuide AI is a complete, deployed, production-hardened agentic RAG system — built from a blank page to a live public URL in 10 days, following a real SDLC (requirements → design → implementation → testing → deployment → maintenance), grounded in a genuine personal connection to the problem it solves.

## Lessons Learned

- **Test the second interaction, not just the first.** Multiple real bugs (Chroma, the silent lab-value default) only appeared on a second question or a specific unlucky input — not the first happy-path test.
- **Saying "no" to a feature is a real engineering decision, not a failure to build it.** The rate-limit and BYOK-key discussions on Day 9 were as valuable as any feature that shipped.
- **Documentation discipline compounds.** Recording every deviation as it happened (Day 2 through Day 9 addenda) made Day 10 possible to write honestly instead of reconstructing history from memory.

## A Farewell Note, From Your AI Pair Programmer

Ten days ago you didn't have a project idea. You had a Claude challenge to finish and a background at ICMR you weren't yet sure how to turn into a portfolio piece. What you built instead is genuinely yours — the lab-validation feature isn't a generic AI demo bolted onto a resume line, it's the shape of work you actually did by hand, now automated responsibly and honestly.

I want to name something specific: the moment on Day 9 when you asked "what if I remove the key later, will it break?" and then asked whether adding a feature was really worth it — that's not a beginner's question. That's someone thinking like the engineer who has to maintain this thing after the demo is over. Keep asking those questions.

Go build the next thing.
