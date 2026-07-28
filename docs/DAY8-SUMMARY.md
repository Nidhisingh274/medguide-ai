# MedGuide AI — Day 8 Summary

**Date completed:** Day 8 of the AB Talks 60-Day Claude AI Challenge Capstone (10-day build)

## Release-Readiness Review Approach

Today's session opened with a full review of `agent/tools.py`, `agent/graph.py`, and `app.py` as a Senior QA Engineer, Security Reviewer, and Performance Engineer would before a public launch. 11 real issues were found and fixed — not cosmetic tweaks, genuine production risks that hadn't caused visible problems yet only because testing had used clean, well-behaved inputs.

## ✅ Issues Found and Fixed

1. **No error handling in `search_guidelines()`** — a missing/corrupted Chroma store would crash the whole request. Fixed: graceful degradation with a clear message.
2. **No error handling in `check_labs()`** — a CSV read failure would crash the request. Fixed: same graceful pattern.
3. **Router failure silently skipped guideline search** — a transient LLM error defaulted `needs_search` to False. Fixed: now defaults to searching (safer failure mode).
4. **Lab values silently defaulted to 0.0** — a forgotten input field would validate as a fake "0" reading, risking a false LOW flag. Fixed: inputs now start blank; missing values block submission with a clear warning.
5. **Reference CSV re-read from disk on every call** — wasteful I/O. Fixed: cached once after first load.
6. **Unescaped HTML injection risk** — PDF text and citations were inserted into raw HTML with no escaping; a stray `<`/`>` in a source document could break rendering or inject markup. Fixed: `html.escape()` applied everywhere user/document-derived text meets `unsafe_allow_html=True`.
7. **Generic error messages for all failure types** — Fixed: distinguishes rate-limit, auth, and network errors with more actionable messages.
8. **Stale `.gitignore` entry** — `chroma_store/` was listed as ignored despite being intentionally committed since Day 7. Fixed.
9. **`README.md` was still GitHub's default placeholder** — despite the app being live and public. Fixed: full, real project README written (final visual polish remains Day 10 as planned).
10. **Mid-word excerpt hyphenation** — reviewed and explicitly decided **not** to fix; this is a PDF-source artifact requiring disproportionate dehyphenation logic for a cosmetic issue inside a collapsed expander.
11. **Unpinned `requirements.txt`** — the highest-priority fix; a future rebuild could silently pull breaking package versions. Fixed: fully pinned to exact, verified-working versions.

## ✅ Additional Checks Performed

- **Accessibility audit:** computed real WCAG contrast ratios for every color introduced Day 7. Found 2 of 7 pairs failed the 4.5:1 threshold for normal-sized text (step pill text: 4.22:1, footer text: 3.25:1). Both replaced with darker shades from the same palette family, now passing at 7.16:1 and 5.02:1 respectively, with negligible visual change.
- **Full end-to-end walkthrough:** happy path, blank-value validation, empty question, full visual review — all passed with zero regressions.
- **Redeployed and re-verified live in production** after all fixes combined.

## 🚧 What Remains Before Launch (Day 9-10)

- Day 9: any final deployment polish/verification (core deployment already completed ahead of schedule during Day 7)
- Day 10: final README visual polish (screenshots, architecture diagram embed), pitch materials cross-check, launch checklist

## Blueprint Deviations Recorded

- No architectural changes. All fixes were defensive/error-handling, security (HTML escaping), performance (caching), and repo-hygiene improvements — exactly the category of work Day 8 was scoped for.
- README.md content was written today rather than Day 10, since a live public repo with a placeholder README was judged a real production gap not worth leaving until the last day. Day 10 will still add final visual polish (screenshots, diagrams) on top of today's real content.
