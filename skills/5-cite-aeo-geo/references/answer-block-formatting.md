# Answer-block formatting

Read this for the core formatting craft of the Cite rung: shaping content so an answer engine can lift a clean, self-contained, attributable answer from it. The discipline is **extraction-friendliness** — and it must work on content that is already real and substantive (the Read rung), never on padded filler.

---

## The self-contained answer block — the central pattern

An answer engine often quotes a *passage*, not a whole page. That passage must make sense **on its own**, lifted out of context. So:

> **Lead each section with a direct, self-contained answer to the question it addresses, then expand.**

### The shape
1. **A question-shaped heading** — phrased the way a user would ask.
2. **A direct answer in the first 1–3 sentences** — complete and standalone, with the key facts in it. No "as mentioned above", no "it depends" without immediately saying on what.
3. **Then the supporting detail** — nuance, caveats, examples, depth.

### The self-containment test
Read the opening passage of a section *in isolation*. Does it answer the question without needing the rest of the page? If a reader (or an engine) saw only that, would they be correctly informed? If not, rewrite it to stand alone.

### Example (shape, not copy to paste)
- **Heading:** "How much does professional carpet cleaning cost?"
- **Direct answer:** "Professional carpet cleaning in the UK typically costs £25–£50 per room, or £100–£200 for a whole house, depending on room size, carpet type, and how soiled it is."
- **Then:** the breakdown by room, what affects price, when it's worth it.

The direct answer is quotable verbatim and stands alone. That's the target.

---

## Question-shaped headings

Engines (and users) match questions. Convert vague or clever headings into the real questions people ask:

- "Pricing" → "How much does X cost?"
- "About the process" → "How does X work?"
- "Overview" → "What is X?"
- "Our approach" → keep only if the question is genuinely "What's your approach?" — otherwise name the question.

Use real question phrasings (the ones in your domain, in your audience's words), and put the answer immediately beneath. Don't stuff every heading into a question if it's unnatural — match genuine user intent.

---

## Extractable structures

Give engines clean units to quote:

- **Direct definitions** for key terms: "X is …" — a single, clear sentence. (These are prime for "what is" answers.)
- **Short paragraphs** — one idea each; walls of text are hard to extract from.
- **Ordered lists** for steps/processes; **unordered lists** for options/criteria.
- **Comparison tables** for "X vs Y", specs, pricing tiers — highly extractable for comparison queries.
- **A concise summary** near the top for long pages (a "key takeaways" that's genuinely accurate).
- **Real FAQs** where users genuinely have repeated questions — and mark them up with `FAQPage` schema (rung 3), but only if they're real (never invent FAQs for markup's sake). The point here is AEO extraction and entity clarity, not a Google FAQ rich result (those are now restricted to government/health sites).

All of this must be in the **served HTML** — a table or list rendered only client-side may be invisible to AI crawlers that don't run JS.

---

## Freshness

- Show a genuine "last updated" date where recency matters (and keep it honest — don't bump the date without updating the content).
- Keep time-sensitive answers current; stale facts get discounted and erode trust.

---

## Anti-patterns — don't do these

- **Answer bait / keyword-stuffed "answers"** that read as written-for-machines. Engines (and users) discount them. Write genuinely useful, direct answers.
- **Padding for length.** Length is not the goal; a complete, concise answer beats a long hedged one.
- **Manufacturing FAQs or "answers" to questions no one asks** just to create extractable blocks. Format real content; don't invent content to format.
- **Burying the answer** under preamble, SEO throat-clearing, or "in this article we'll explore…". Lead with the answer.
- **Hidden or client-only answer blocks** that aren't in the served HTML.

---

## How this builds on the lower rungs

You are **reformatting real, substantive content** (Read) about **clear entities** (Understand) within a **coherent site** (Connect) so it's extractable and attributable. If the content is thin, the fix is at Read, not here — no amount of answer-block formatting makes empty content citable. Format substance; never substitute formatting for substance.
