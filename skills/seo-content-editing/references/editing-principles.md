# Editing principles — improve without inventing

Read this for how to improve real copy safely, and (at the end) how to review an AI-generated draft before it is published. The whole skill rests on one split: what you can **edit now** versus what you must **flag for the human**. Get that split right and everything else follows.

---

## The split: edit vs flag

**Edit now (safe — it's expression and structure of existing truth):**
- Reordering so the answer leads.
- Tightening sentences, cutting padding, replacing jargon, fixing passive throat-clearing.
- Turning dense prose into lists, tables, definitions, question-headings where it aids clarity/extraction.
- Reframing existing material to match the reader's intent.
- Merging/splitting paragraphs and sections for a clear outline.
- Surfacing real trust signals that already exist (a real author, real sources) more prominently.

**Flag for the human (do NOT invent):**
- Missing facts, data, statistics, or research.
- Missing real examples, case studies, or first-hand experience.
- Missing or anonymous authorship and credentials (E-E-A-T).
- Citations/sources that aren't there.
- Any claim you can't verify from the existing content or what the user gave you.

The output for flagged items is a **brief**: "this section needs a real figure for X / a named expert author / a source for this claim — please provide, and I'll weave it in."

---

## The editing techniques

### Answer-first
Where readers arrive with a question, open the section with a direct, self-contained answer to it, then the nuance and depth. Read the opening passage in isolation: if it does not answer the question on its own, it is not done. This is ordinary good writing, and the same discipline Cite uses (`cite-aeo-geo/references/answer-block-formatting.md`). It is not a special format for AI: never split a good page into fragments or bolt on FAQs to create quotable lines.

### Clarity
- One idea per paragraph; short paragraphs.
- Prefer plain words and active voice; cut filler ("in order to" → "to"; "it is important to note that" → delete).
- Front-load the point; don't bury it under preamble or SEO throat-clearing ("In this article we'll explore…").
- Use concrete language over vague abstraction.

### Structure for extraction
- Descriptive, often question-shaped headings that map the page's outline.
- Lists for steps/options; tables for comparisons; one-line definitions for key terms.
- A genuine, accurate summary near the top of long pages.

### Intent
Make sure the content actually serves the reader's intent (informational/commercial/transactional/navigational). Move, cut, or reframe material that doesn't. Don't pad a transactional page with essay content, or strip a how-to down to a sales pitch.

---

## Preserve voice and meaning

You are an editor, not a ghostwriter replacing the author:
- Keep the **author's tone** and register — don't flatten a distinctive voice into generic web copy.
- Keep the **factual claims and positions** intact — clarify how they're said, never change what's said.
- Don't introduce a confident new claim the source didn't make. Improving readability must not drift the meaning.

When in doubt, edit conservatively and show the user the before/after so they can confirm you preserved intent.

---

## The anti-patterns this skill refuses
- **Fabrication:** inventing stats, quotes, sources, results, testimonials, or expertise. (Both dishonest and increasingly self-defeating — engines discount it.)
- **Keyword-stuffing / "SEO writing":** robotic copy written for crawlers. Write for the reader; the search benefit follows.
- **Mass generation / spinning:** producing or rewriting at volume to fill the index. Out of scope, on purpose.
- **Meaning drift:** "improving" a sentence into a stronger claim than the source supports.
- **Date-faking on refreshes:** never bump `dateModified` without genuinely updating the content.

---

## Verify the edit honestly
After editing, confirm on the **served output** that the improved copy is live, and run the **truth check**: every fact/figure/quote/source is real and the user's meaning is intact. Anything you can't verify, you remove. Then report the before/after and, explicitly, the briefs for what only the human can supply.

---

## Voice and banned claims come from the context file

`.seo/context.md` (written by `seo-context-gathering`) settles two questions before you edit:

- **Whose voice?** The Voice section quotes real lines from the business's own copy, with its tone, person, reading level, and the words it uses and avoids. Edit towards those quoted lines. If the page you are editing already drifts from them (an agency rewrite, say), bring it back towards the house voice and say so in the report.
- **What may not be said?** Claims and constraints lists superlatives, regulated or YMYL claims, competitor-naming rules, and anything that needs sign-off. Treat each as a hard rule. An existing sentence that breaks one is a finding: remove it, or flag it for the business when removing it would change a position they hold. Never reword a banned claim into a softer version of itself ("the best in Britain" into "among the very best").

Only `[established]` facts may enter the copy. An `[inferred]` fact can guide how you structure the page, never what it asserts. If the file is missing, infer the voice from the page in front of you for a single quick edit, and recommend running `seo-context-gathering` before any wider content work.

---

## Worked example: before and after

The business is Northfield Tool Company from `seo-context-gathering/references/context-pack-format.md`. Its context file records a plain, second-person voice with short sentences, the quoted line "The iron arrives sharp. You will still want to hone it before the first cut.", and a constraint against superlatives such as "the best in Britain". The `[established]` differentiators are in-house forging in Sheffield, a lifetime sharpening guarantee, and a steel specification published for every tool.

The section below is illustrative: an imagined weak draft of the bevel-up plane page, used to show the method.

**Before**

> ## Our Approach
> At Northfield Tool Company, we are passionate about craftsmanship and have been dedicated to excellence since 2009. In this article we'll explore everything you need to know about our bevel-up plane. It is important to note that our planes are the best in Britain and are loved by professionals everywhere! The plane is made from high-quality steel. A bevel-up plane copes well with end grain and difficult grain, and you can change the cutting angle by honing a different bevel on the iron, which many woodworkers find useful. The iron arrives sharp, though honing is recommended.

**Diagnosis**
- The heading answers no question, and the useful answer is in the fifth sentence.
- "the best in Britain" breaks Claims and constraints. "loved by professionals everywhere" has no proof behind it.
- "high-quality steel" is vague when the real steel specification is published on the page.
- "passionate about craftsmanship", "In this article we'll explore" and "It is important to note" are padding, and the exclamation mark is a habit the voice section says the business avoids.

**After**

> ## What is a bevel-up plane good for?
> A bevel-up plane copes well with end grain and difficult grain. You can change its cutting angle by honing a different bevel on the iron.
>
> The iron arrives sharp. You will still want to hone it before the first cut.
>
> We forge every plane in our Sheffield workshop, and the steel specification is in the table below. Our lifetime sharpening guarantee is explained on the [guarantee page](/guarantee).

**What changed and why**
- The heading is now the question a buyer asks, and the answer leads, so a reader or an answer engine can lift it whole.
- The superlative and the unsupported praise are gone. Nothing replaced them, because nothing established could.
- "high-quality steel" became a pointer to the specification the business already publishes.
- The honing advice now uses the house line from the Voice section, word for word.
- "Since 2009" moved out of this section: it is true, but it does not answer the question. It stays on `/about`.
- The guarantee gets a link, so its terms stay in the business's own words on `/guarantee`.

**Flagged for the business, not invented**
- "Loved by professionals": the site has 340 named reviews. If any are from professional joiners and the reviewers agreed to be quoted, one real quote could go here. Please choose one, or leave it out.

---

## Diff-style output

Use a diff when you have no write access, when the page lives in a CMS, or when the user wants to approve each change before it lands. It shows exactly what moves and why, and nothing changes until a person applies it.

**For a file in a repository**, make the edit on a branch and show the unified diff, or diff two copies outside the repo. `git diff --no-index` works the same in bash and PowerShell:

```bash
git diff --no-index --word-diff before.md after.md
```
```powershell
git diff --no-index --word-diff before.md after.md
```

Use `--word-diff` for prose, where a line-based diff turns one changed word into a whole replaced paragraph.

**For CMS copy**, give a readable diff with a reason for each change, so an editor can apply it by hand:

```diff
--- /products/bevel-up-plane (served 2026-08-18)
+++ /products/bevel-up-plane (proposed)
@@ change 1: heading answers the buyer's question @@
-## Our Approach
+## What is a bevel-up plane good for?
@@ change 2: remove a banned superlative and unsupported praise (Claims and constraints) @@
-It is important to note that our planes are the best in Britain and are loved by professionals everywhere!
@@ change 3: replace a vague claim with the published specification @@
-The plane is made from high-quality steel.
+We forge every plane in our Sheffield workshop, and the steel specification is in the table below.
```

Each hunk header names the reason. Keep hunks small and in page order, so the editor can accept some and reject others. After the changes are applied, re-fetch the served page and run the truth check as usual.

---

## Reviewing an AI draft

A generated draft is reviewed before anything else happens to it. The review answers one question: is this safe and worth publishing? It does not polish prose that may be wrong. Run the five checks in order, because a draft that fails on accuracy is not worth a voice edit.

Google's position, which the checks follow (verified 2026-10):
- Generative AI outputs "may contain inaccuracies", so fact-check before publishing, including metadata, structured data and alt text ([Google Search's guidance on using generative AI content](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content)).
- Generating many pages without adding value for users can breach the scaled content abuse policy ([spam policies](https://developers.google.com/search/docs/essentials/spam-policies)).
- Its self-assessment questions ask whether content provides original information, reporting, research or analysis; whether it provides substantial value compared with other pages in search results; whether it demonstrates first-hand expertise; and whether it is made with extensive automation across many topics ([Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)).

### 1. The claims table

List every checkable statement. Opinions and plain advice that follow from sourced facts do not need rows; numbers, names, dates, quotes, product details, legal or medical statements, and anything presented as a finding do. The rows below are illustrative, showing the format, not facts to reuse.

| # | Claim (as written) | Type | Source | Status |
|---|---|---|---|---|
| 1 | "Combi boilers should sit between 1 and 1.5 bar when cold" | figure | Manufacturer manual, URL, page 12 | verified |
| 2 | "A 2024 study found 40% of boilers are under-pressurised" | statistic | none given | unsupported |
| 3 | "We've serviced over 3,000 boilers" | experience | `.seo/context.md`, Proof assets, `[established]` | verified |
| 4 | "Gas Safe recommends annual bleeding" | attributed claim | cited URL says nothing about bleeding | wrong source |

Statuses: `verified` (source opened and it says the same thing, or a matching `[established]` fact), `unsupported` (no source), `wrong source` (the source exists but does not support the claim), `false` (a reliable source contradicts it), `invented` (the source, study, quote or person does not exist). Open every URL the draft cites. Made-up references, plausible but non-existent page paths and quotes attributed to real people are common in generated text, and each one is a high-severity finding.

An `[inferred]` fact in the context file does not count as a source. Neither does another AI tool's answer.

### 2. First-hand experience

Mark the places where a reader would expect someone to have actually done the thing: used the product, carried out the repair, visited the place, run the numbers. For each, write a question the person can answer in a sentence or two: "What pressure do you usually find on a cold combi boiler when you arrive for a service?" Their answer, in their words, goes into the draft; a paraphrase that changes the meaning does not.

Experience claims already in the draft ("we tested", "in my experience", "our customers tell us") must match the context file or be confirmed by the person. If neither, remove them and ask.

### 3. Information gain

Compare the draft with what already ranks for its main query:
- **With a SERP capability** (a provider on the user's own key), take the top results for one representative query, fixed to the audience's country and language, and record the provider and date. Do not scrape Google's results pages: the spam policies prohibit automated queries to Google.
- **Without one**, fetch the competitor pages the user names, or those in the context file's Competitors section, and label them "named competitors, not necessarily who ranks".

Fetch politely, read them for comparison only, and never copy their wording. Then write two short lists: what the draft adds that none of them has, and what it only restates. Things that count as gain: original data, a worked example from the business, a method or tool they lack, a clearer answer to a question they skip, a current fact they have wrong. Length, more headings and synonyms do not.

If the draft adds nothing, the fix is new material from the person, or no page at all. Never pad to look different.

### 4. Signs of mass production

Each sign is a reason to look harder, not proof on its own:
- sentences that would fit any business's site with the name swapped;
- an outline that mirrors the ranking pages heading for heading;
- specifics that look invented: round percentages, "experts say", "studies show", unnamed customers;
- boilerplate openings and closings ("In today's fast-paced world", "In conclusion");
- leftover prompt or model text, placeholder brackets, or a sign-off addressed to the person who asked for it;
- the draft being one of many on unrelated topics made the same way, with no named person reviewing them.

If the user mentions a batch (dozens of location or product pages from one prompt), say plainly that publishing it at scale without added value is what the scaled content abuse policy describes, and hand programmatic work to `seo-programmatic`.

### 5. Voice

Use the Voice section and Claims and constraints exactly as for an existing page (above). Generated drafts often drift towards generic marketing copy, superlatives and exclamation marks; banned claims are findings whether a person or a model wrote them.

### The verdict

| Verdict | When |
|---|---|
| **Publish** | Every row in the claims table is `verified`; no invented experience; experience present where the topic needs it; at least one real gain over the ranking or named pages; voice fits. Minor edits may be listed. |
| **Revise** | The problems can be fixed by cuts or by material the person can supply: `unsupported` claims to source or remove, experience to add, a gain the business can provide, voice drift. |
| **Do not publish** | A core claim is `false` or `invented`, or the draft is built on invented experience or sources; or it adds nothing and the business has nothing to add; or it is part of a batch that looks like scaled content. |

Start the report with the verdict and one sentence of reason, then the claims table, the experience questions, the information-gain lists, the mass-production signs seen, and voice notes. In `fix` mode, apply only approved findings to the draft file: cuts, re-ordering, voice corrections and material the person has supplied. Never fill a gap with a guess. After the page goes live, re-fetch it and run the truth check on the served output.

Google also suggests telling readers how content was made where they would reasonably want to know ("Who, How, Why" in its helpful content guidance). Whether to add a disclosure is the publisher's decision; raise it, do not write it in unasked.
