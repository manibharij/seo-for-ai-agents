# Understand — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the Understand (schema) skill. Run Reach and Read first — schema describes content that must already exist and be readable.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** Review every change on the *served* output and test before you publish. See the repo's `DISCLAIMER.md`.

---

You are adding **structured data (schema.org as JSON-LD)** so engines can identify the entities on my pages. This is rung 3 of the Visibility Ladder. The unbreakable rule: **only mark up information that is genuinely visible and true on the page.** Never invent authors, ratings, reviews, prices, or FAQs. Work in four steps.

**Verify on what is actually SERVED.** Schema injected only client-side may never be seen — it must be in the raw HTML.

## Step 1 — Diagnose
- Classify each template by what it actually is: article → `BlogPosting`/`Article`; product → `Product` (+ `Offer`); the business → `Organization`/`LocalBusiness`; a person → `Person`; real Q&As → `FAQPage`; nav trail → `BreadcrumbList`. (Note: Google retired `HowTo` rich results, and `FAQPage` rich results are now restricted to government/health sites — on a normal site add these for entity clarity/AEO, not expecting a Google snippet. Verify current per-type eligibility before promising any rich result.)
- Fetch the served HTML and find existing `<script type="application/ld+json">` blocks. Are there any? Are they in the served HTML or only client-side? Do they **match the visible content**, or claim things the page doesn't show (placeholder ratings, fake authors, wrong `@type`)?

## Step 2 — Fix
- Add/correct JSON-LD using the **right type** and **only properties you can fill truthfully from the visible page**. Use ISO dates, absolute URLs, ISO currency (`GBP`), and schema.org enum URLs (`https://schema.org/InStock`).
- **Next.js App Router:** render the JSON-LD from the **same data the page uses**, in a server component, so it lands in the served HTML:
  ```tsx
  <script type="application/ld+json"
    dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
  ```
- Link recurring entities with a consistent `@id` (the publisher that is also the business), with identical name/URL/logo.
- **White-hat lines you must not cross:** no fabricated ratings/reviews; no fake authors/dates/credentials; no `FAQPage` of invented questions; no marking up hidden content. If real trust data is missing, **tell me to provide it** — don't invent it.

## Step 3 — Verify (re-fetch + validate + honesty-check)
- **Served:** confirm the JSON-LD is in the raw served HTML, per template.
- **Valid:** JSON parses; `@type` valid; required/recommended properties present (check Google's per-type requirements). Report eligibility honestly — eligible ≠ guaranteed to show.
- **Honest:** re-read the page and confirm every schema value appears on it and is true.

## Step 4 — Explain it to me in plain English
1. **What was wrong** (e.g. "your product pages didn't state product/price/availability in a structured way, so they couldn't qualify for the richer result format").
2. **What you added and why it matters.**
3. **Proof** — the validated JSON-LD now in the served HTML, mirroring the visible page.
4. **What only I can provide** — any real authors/reviews/credentials you deliberately did **not** invent.

Then tell me the next step is **Connect** (wiring these understood pages together with internal links and canonicals).
