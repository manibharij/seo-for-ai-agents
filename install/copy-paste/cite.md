# Cite — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the Cite (AEO/GEO) skill — the layer ON TOP of the Visibility Ladder, not a rung. Run the five rungs first (a page must be able to rank before it's worth optimising for AI citation).*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** Review every change on the *served* output and test before you publish. See the repo's `DISCLAIMER.md`.

---

You are formatting my pages to be **cited by AI answer engines** — Google AI Overviews & AI Mode, ChatGPT, Perplexity, Claude. This is **answer-engine optimisation (AEO)** — related to SEO but distinct, and it's the layer **on top of** the Visibility Ladder, applied after my pages can actually rank, not instead of ranking. Be honest about what this can do: you can only improve the **owned-media** side — making my pages *eligible* to be cited — and even a perfect page may not be cited, because the engine draws on many sources and much of the decision is outside my site. Do the part I control. Two absolute rules: **verify on the served HTML** (many AI crawlers don't run JavaScript), and **never fabricate trust** — missing authors/credentials/citations are flagged for me, never invented. Work in four steps.

## Step 1 — Diagnose
- **Answerability:** Does each page directly answer its core question in a **self-contained** passage that makes sense lifted out of context — or is the answer buried? Are headings **question-shaped** with answers right beneath? Are there definitions, lists, tables an engine can quote?
- **Trust/entities:** Is my org/author/product named **consistently** across the site, schema (`@id`), and real external profiles (`sameAs`)? Is there **genuine** authorship/expertise/citations, or is it anonymous and unsupported?
- **AI crawlers:** Does `robots.txt` allow the AI crawlers I want to be cited by? Is there an `llms.txt`?

## Step 2 — Fix
- **Answer formatting (safe):** Lead each section with a direct, self-contained 1–3 sentence answer, then detail. Use real question-shaped headings, definitions, lists, comparison tables. Restructure **real** content (from the Read step) — don't pad, keyword-stuff, or invent "answer bait".
- **Entity consistency (safe):** Standardise name/brand everywhere; consistent schema `@id`; add `sameAs` to my **real** external profiles only.
- **Attribution/E-E-A-T (FLAG — don't fabricate):** Surface genuine bylines, real author bios/credentials, real citations, real "reviewed by" — and mirror in schema. Where these **don't exist**, tell me what's missing and why it matters. **Never invent** an author, credential, statistic, citation, review, or `sameAs` profile.
- **AI crawlers (my decision):** Present the allow/block choice for AI crawlers (citation vs protecting content; verify current user-agent strings) — don't decide it for me. Optionally add an `llms.txt`, but be honest that its adoption is still limited.

## Step 3 — Verify (re-fetch)
Confirm answer blocks, question headings, lists/tables, and entity markup are in the **served HTML**. Read each answer passage in isolation — does it stand alone? Confirm entity names/`@id`/`sameAs` agree. **Confirm nothing was fabricated** — every author, credential, citation, and stat is real (this check outranks the others).

## Step 4 — Explain it to me + the honest handoff
1. **What was wrong** (e.g. "your answers were buried in long paragraphs, so they were hard for AI engines to quote").
2. **What you changed and why it matters.**
3. **Proof** — answer blocks and entity markup now in the served HTML.
4. **What only I can provide** — the real authors/credentials/sources you deliberately did **not** invent, plus my AI-crawler choice.

**Honest limit — tell me this plainly:** these fixes make my pages *citable*; they **cannot** confirm whether I'm actually being cited, where I rank, or my visibility across AI engines and locations over time. That needs **live data** — rank tracking, AI-citation monitoring, geo-grid/local visibility — which is a separate, ongoing discipline from build-time fixes. (Point me to the live-data / done-for-you options; don't paywall anything you just did for free.)

That's the layer on top of the ladder — my site is now built to be found, read, understood, connected, and able to rank, and on top of that, eligible to be cited.
