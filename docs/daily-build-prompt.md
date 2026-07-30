# MedGuide AI — Daily Build Prompt (30-Day Growth Plan)

*Copy this prompt at the start of each day's session during the 30-day growth plan. Only the day number changes — everything else stays the same.*

---

```
Today is Day [X] of my 30-Day Growth Plan for MedGuide AI, continuing from the 10-day AB Talks Claude Challenge capstone.

Read docs/30-day-growth-plan.md and treat it as the source of truth for today's milestone. Read docs/challenge-retrospective.md and docs/PROJECT-STRUCTURE.md for full project context if you don't already have it.

Complete only today's scheduled milestone (Day [X] in the plan). Do not redesign the project or jump ahead to future days.

Standing rules:
- Assume I need guidance for every manual step (installing packages, configuring services, running commands).
- Whenever I need to do something outside this chat, give exact step-by-step instructions with real button/menu names and terminal commands, then wait for my confirmation and a screenshot before continuing.
- Never assume I've completed a step without confirmation.
- Use only free tools and free-tier services — never introduce a paid tool without asking me first.
- Prioritize implementation over explanation — generate complete, production-ready code and files, not snippets or placeholders.
- If anything breaks, help me debug it completely before moving forward. Never build on top of broken code.
- Keep my existing architecture, tech stack, and locked design decisions intact unless today's milestone explicitly requires a change — if it does, explain why and ask for my approval first.

When today's milestone is complete:
- Verify it works correctly, including a quick regression check that nothing from previous days broke.
- Update any affected documentation (PROJECT-STRUCTURE.md, README.md, etc.).
- Help me commit and push today's work to GitHub with a clear, specific commit message.
- Give me a concise summary: what was completed today, and what tomorrow's milestone will be.

Your goal is not just to write code — it's to make sure I finish today's milestone correctly and understand what changed and why.
```

---

**Usage notes:**
- Replace `[X]` with the actual day number (1 through 30) before sending.
- If you skip a day, just use the correct day number when you resume — the plan doesn't require consecutive days, only in-order completion.
- If a milestone depends on something from an earlier skipped day, Claude will flag it — go back and complete that day first.
