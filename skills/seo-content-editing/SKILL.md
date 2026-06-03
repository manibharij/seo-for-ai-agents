---
name: seo-content-editing
description: >-
  Improve EXISTING page copy for search and answer engines — clarity, structure,
  depth, search-intent match, readability, and answerability — while keeping it
  truthful and in the author's voice. Use on "improve this content", "edit my copy",
  "make this page clearer/better", "tighten this", "optimise this page's content",
  or after a content audit flags a page to "improve". Strictly white-hat: it edits
  and restructures REAL content and flags where genuine substance is missing — it
  never fabricates facts, sources, or expertise, and never mass-generates content.
---

# Content Editing — improve real copy, honestly

The companion to `seo-content-audit`: where the audit decides *what* to do, this **improves the copy** on pages marked "improve" or "refresh". It makes existing content clearer, deeper (from real material), better matched to intent, and easier for both readers and answer engines to use — **without changing what's true or whose voice it's in.**

> The defining rule, and the reason this skill is safe to ship: **edit, don't invent.** You may restructure, clarify, tighten, and reorganise real content, and weave in material the user provides. You may **not** fabricate facts, statistics, quotes, sources, case studies, or expertise — and you do **not** auto-generate articles to fill gaps. Missing substance is a flagged human task. This is "editing, not generation."

Work the four steps: **Diagnose → Edit → Verify (on served output) → Report.**

---

## Step 1 — Diagnose what's weak

Usually you arrive here from a content-audit verdict; if not, assess the page first (`seo-content-audit/references/quality-and-intent.md`). Identify the specific weaknesses:
- **Intent mismatch** — the content doesn't answer what the reader came for.
- **Buried point / weak structure** — the answer is hard to find; no clear outline.
- **Thinness vs padding** — too little real substance, or real substance drowned in filler.
- **Unclear writing** — long sentences, jargon, passive throat-clearing, walls of text.
- **Weak answerability** — no self-contained answers an engine could quote (ties to Cite).
- **Missing genuine substance/E-E-A-T** — gaps only the user can fill (real data, real examples, real author/sources).

Separate the two kinds of weakness: **editable now** (structure, clarity, intent framing, answerability from existing material) vs **needs the human** (missing real facts/sources/expertise). See `references/editing-principles.md`.

## Step 2 — Edit

Improve what you can, truthfully:
- **Lead with the answer.** Restructure so each section opens with a direct, self-contained answer to its question, then expands (this serves readers, rankings, and AI citation alike).
- **Match intent.** Reframe so the content actually serves the reader's intent; cut or move what doesn't.
- **Tighten and clarify.** Shorter sentences, plain words, active voice, one idea per paragraph; turn dense prose into lists/tables/definitions where it genuinely helps extraction.
- **Deepen from real material only.** Add depth using facts, examples, and detail the user has provided or that already exist on the site — never invented ones.
- **Preserve voice and meaning.** Keep the author's tone and the factual content intact; you're improving expression and structure, not rewriting their position or claims.
- **Surface real E-E-A-T.** If a real author/credentials/sources exist but aren't shown, surface them; if they don't, flag it — never fabricate.
- Keep changes **additive/reversible** on an existing site and in version control (`seo-orchestrator/references/existing-site-safety.md`).

## Step 3 — Verify (on the served output)

- Re-fetch and confirm the improved content is present in the **served HTML**.
- **Truth check (the critical one):** every fact, figure, quote, and source in the edited copy is real and unchanged in meaning — you didn't introduce anything fabricated, and you didn't alter the user's claims. If you can't verify a statement you added, remove it.
- Confirm the lead answers are genuinely self-contained (read them in isolation), and the intent now matches.
- Confirm you preserved meaning — the edit clarified, it didn't distort.

## Step 4 — Report

Show the user, in plain English: what was weak, what you changed (with before/after of key passages) and why it helps, the improved content live in the served output, and — explicitly — **what you did not invent**: the gaps where real substance, data, sources, or author credentials are still needed from them. Note that ongoing performance of the edited page is live data (connect GSC to watch it).

---

## What this skill will not do
- It will not **write fake content**, fabricate statistics/quotes/sources, or invent expertise or case studies.
- It will not **mass-generate** pages or "spin" content to fill gaps — that's the low-value, engine-discounted output the whole pack is built against.
- It will not change the **meaning** of the user's claims or misrepresent them.
- For genuinely missing content, it produces a **brief** (what's needed, what questions to answer) for a human to fill — it doesn't fill it with invention.

## Reference files
- `references/editing-principles.md` — the editable-vs-flag split, the answer-first/clarity/intent techniques, voice and meaning preservation, and the white-hat lines in detail.
