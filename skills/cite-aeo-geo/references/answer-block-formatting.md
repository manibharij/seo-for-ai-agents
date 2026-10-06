# Clear, self-contained writing

Read this for the writing craft of the Cite layer. The file keeps its old name (`answer-block-formatting.md`) so links still work, but the idea has changed: there is no special "answer block" format to add. The aim is writing that a reader can use quickly and that still makes sense when a passage is quoted on its own. Pages written that way serve people first, and they also happen to be easy for AI answers to use.

It only works on content that is already real and substantive (the Read rung). No amount of restructuring makes an empty page worth citing.

---

## What Google says you do not need

Google's guide to its generative AI features (verified 2026-10, [Optimizing your website for generative AI features on Google Search](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)) says SEO best practices still apply, because AI Overviews and AI Mode use its core ranking systems, and lists these as unnecessary:
- breaking content into tiny pieces ("chunking") for AI to understand it;
- new machine-readable files, AI text files, markup or Markdown, `llms.txt` included;
- writing in a specific way just for generative AI search;
- special schema.org markup for AI features;
- chasing inauthentic mentions across the web.

What it asks for instead: unique, useful, non-commodity content with a real point of view, semantic HTML, crawlable and indexable pages that are eligible for a snippet, and less duplicate content. Treat that as the brief for this file.

Other engines (ChatGPT, Perplexity, Claude, Copilot) do not publish an equivalent guide in this detail. Nothing they document rewards fragmented or padded content, so the same approach is the safe one for all of them. That last point is judgement.

---

## The pattern: answer, then explain

Where a reader arrives with a question, answer it near the top of the section, then give the detail, caveats and examples. That is ordinary good editing: a skimming reader gets the point at once, and a careful reader gets the depth.

Write the opening so it stands on its own:
- **Name the subject.** "Professional carpet cleaning costs..." rather than "It costs...".
- **Keep the fact and its condition together.** "£25 to £50 per room, depending on size and how soiled it is", not the figure here and the conditions three paragraphs later.
- **Define a term where it first appears**, briefly.
- **No back-references** such as "as mentioned above" in the sentences that carry the answer.

### The stand-alone test
Read the opening passage of a section in isolation. Would a reader who saw only that passage be correctly informed? If not, rewrite it so it would. This is a test of clarity, not a template: many sections (a story, an argument, a walkthrough) do not open with a one-line answer, and should not be forced to.

### Example (shape, not copy to paste)
- **Heading:** "How much does professional carpet cleaning cost?"
- **Opening:** "Professional carpet cleaning in the UK typically costs £25 to £50 per room, or £100 to £200 for a whole house, depending on room size, carpet type and how soiled it is."
- **Then:** the breakdown by room, what affects the price, and when it is worth it.

The figures must come from the business or a cited source. If they do not exist, the section needs real data from a person, not a confident-sounding estimate.

---

## Headings that say what the section answers

A heading should tell the reader what they will learn. Phrase it as a question where that is how readers ask ("How much does X cost?"), and as a plain label where it is not ("Delivery and returns"). Turning every heading into a question reads oddly and helps no one.

- "Pricing" can become "How much does X cost?" when the section answers that.
- "Our approach" can stay if the section really describes an approach; otherwise name what it covers.

Use the audience's own words (from `.seo/context.md` or real queries), not a keyword list.

---

## Structure that helps a reader

Use structure because it makes the content easier to follow, and use the semantic HTML element for it, so that both readers and parsers see the same thing:
- **Short paragraphs**, one idea each.
- **Ordered lists** for steps, **unordered lists** for options or criteria.
- **Tables** for real comparisons: specs, tiers, "X vs Y".
- **A short, accurate summary** near the top of a long page, where readers benefit.
- **Definitions** of key terms in a sentence.

All of it must be in the **served HTML**. A table rendered only in the browser may be invisible to crawlers that do not run JavaScript.

### FAQs
Add a FAQ section only when readers genuinely ask several short, repeated questions about that page's subject, such as delivery or sizing questions on a product page. Never add one to every page, and never write questions nobody asks. `FAQPage` markup is optional context: Google stopped showing FAQ rich results in May 2026 (verified 2026-10, [Search Central documentation updates](https://developers.google.com/search/updates)), and it says no special schema is needed for AI features.

---

## Freshness
- Show a genuine "last updated" date where recency matters, and change it only when the content changes.
- Keep time-sensitive facts current; stale facts erode trust.

---

## Anti-patterns: do not do these

- **Fragmenting a good page.** Splitting one coherent guide into many thin pages, or chopping prose into disconnected one-line snippets, makes it worse for readers. Google says chunking is not required.
- **Variations for AI.** Writing several versions of a page to catch different phrasings. Google treats separate content variations made to manipulate rankings as scaled content abuse.
- **FAQ bolt-ons** on every page, or invented questions written to create quotable lines.
- **Answer bait:** keyword-stuffed "answers" written for machines.
- **Padding for length.** A complete, concise answer beats a long, hedged one.
- **Burying the point** under preamble ("In this article we'll explore...").
- **Hidden or client-only content** that is not in the served HTML.
- **Unsupported figures** in the opening line to make it sound authoritative.

---

## How this builds on the lower rungs

You are improving the clarity of real, substantive content (Read) about clear entities (Understand) in a coherent site (Connect). If the content is thin or generic, the fix is at Read or with `seo-content-editing`, and missing expertise is a human task. Clear writing makes good content easier to use; it never stands in for it.
