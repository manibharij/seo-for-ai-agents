# Example 3 — Cite: good answers, buried → answer blocks AI can quote

A consultancy has genuinely useful content, but it's written as flowing prose with the answer buried three paragraphs down. The pages reach, read, understand, and connect fine (rungs 1–4 pass). They're just not *formatted to be cited* by AI answer engines. This example shows the AI-search lead and the honest live-data handoff.

*Stack: Next.js App Router. Anonymised. Assumes rungs 1–4 already pass.*

---

## Diagnose — on the served HTML

The agent fetches a key page and reads it the way an answer engine would — looking for a self-contained, extractable answer to the question a user asks.

The question a user actually types: *"how much does a fractional CFO cost?"*

What the served HTML has, under a heading **"Our Approach to Pricing"**:

> "When we begin working with a new client, we take time to understand the unique contours of their financial operations. Every business is different, and we pride ourselves on a bespoke approach honed over many years of partnering with founders across sectors. After an initial discovery process, and once we have a clear picture of scope, we are able to arrive at a figure that reflects the value delivered…"

Three more paragraphs before, eventually: *"…typically between £2,000 and £6,000 per month."*

Diagnosis:
- The **answer exists** but is buried at the end and not self-contained — an engine extracting the opening passage gets throat-clearing, not a price.
- The **heading is not question-shaped** ("Our Approach to Pricing" ≠ "How much does it cost?").
- No definitions, lists, or tables — nothing cleanly extractable.

> Rungs 1–4 pass, so the floor really is Cite. The content is real and good (Read passed) — this is a **formatting** fix, not a content-invention one.

---

## Fix — reformat real content (invent nothing)

The agent restructures the existing, true content into a self-contained answer block under a question-shaped heading:

```markdown
## How much does a fractional CFO cost?

A fractional CFO typically costs **£2,000–£6,000 per month** in the UK, depending on
scope, company size, and how many days a month you need. For most funded startups it
works out far cheaper than a full-time CFO (£120k+ a year) while covering the same
strategic work.

**What changes the price:**
- **Days per month** — one day a week vs three.
- **Company stage** — pre-seed reporting vs Series-B board-level work.
- **Scope** — forecasting only, or fundraising support and investor reporting too.

[The bespoke "Our Approach" detail follows for readers who want it.]
```

- The **direct answer leads**, with the actual figure, in a passage that stands alone.
- The **heading matches the real question.**
- A **list** makes the price factors extractable.
- Every number is the consultancy's **real** pricing — reformatted, not invented.
- The original nuance is kept below for human readers.

The agent also confirmed entity consistency (the firm's name/`@id`/`sameAs` agree — set in earlier rungs) and that a real, named author with genuine credentials is bylined (it was — so it surfaced it; had there been none, it would have flagged it, not invented one).

---

## Verify — served HTML + self-containment

```bash
curl -sL https://example.com/services/fractional-cfo | grep -i "How much does a fractional CFO cost"
```

- **Served:** the question heading, the answer block, and the list are in the raw served HTML.
- **Self-containment test:** read the answer passage in isolation — it answers "how much does a fractional CFO cost?" on its own, with the figure. ✓
- **Honesty:** every figure is the firm's real pricing; the byline and credentials are real. Nothing fabricated.

---

## Report — plain English + the honest handoff

> **What was wrong:** Your pages had the right answers, but buried in long paragraphs under headings like "Our Approach to Pricing". AI answer engines (Google's AI Overviews, ChatGPT, Perplexity) lift short, self-contained answers to quote and cite — so even though your content was genuinely good, it was hard for them to use.
>
> **What I changed:** I led each key page with a direct, self-contained answer under a heading phrased the way people actually ask, and turned the pricing factors into a list. All the figures are your real ones — I only restructured what was already there.
>
> **Proof:** the new question heading and answer block now in the served HTML (shown above), and the answer reads correctly on its own.
>
> **The honest handoff:** these changes make your pages *citable* — well-formatted and trustworthy enough to be eligible. They **cannot** tell you whether you're *actually* being cited by AI Overviews or ChatGPT, for which questions, or how that compares to competitors and changes over time. That's **live data**: AI-citation monitoring, rank tracking, and geo/local visibility — a separate, ongoing discipline from these build-time fixes. *(This is where the rank/geo-grid data product and the done-for-you service come in — the build is free and complete; live measurement is the next step.)*

---

**Why this example matters:** it shows the pack's lead angle — formatting for the way AI search actually consumes content — done on **real content** (never invented), verified on **served HTML**, and closed with the **honest boundary** between what a build can do and what needs live data. That boundary is the product handoff, stated without paywalling anything given away for free.
