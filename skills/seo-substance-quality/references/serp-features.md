# SERP features: what can be earned, and what cannot be requested

Read this when someone asks how to "get the featured snippet", or when a report needs to
explain why a competitor occupies more of the result page than their position suggests.

The honest position, stated first because the whole file follows from it: **SERP features
are selected, not requested.** There is no markup that asks for a featured snippet and no
setting that opts a page in. What you control is whether your page is a plausible candidate,
and that is ordinary Substance work with a particular shape.

Google facts verified 2026-11 against
https://developers.google.com/search/docs/appearance/featured-snippets.

## Featured snippets

Google's own answer to "how do I mark my page as a featured snippet" is **"You can't."**
Its systems "determine whether a page would make a good featured snippet for a user's search
request, and if so, elevates it".

So the work is the preconditions, all of which are worth doing anyway:

- **Rank on page one first.** Snippets are drawn from results that already compete. A page
  at position 30 is not a snippet candidate, and snippet work on it is premature.
- **Answer the question in a self-contained passage**, near the heading that asks it, in
  roughly the shape the answer wants: a sentence or two for a definition, an ordered list for
  a process, a table for a comparison. The shape follows the question, not a template.
- **Put the answer before the context.** A page that spends three paragraphs establishing
  why the question matters has buried the only part that can be lifted.
- **Be unambiguous.** Hedged, heavily qualified prose gives a selector nothing clean to take.

What does not work, and gets sold anyway: fragmenting the page into question headings for
their own sake, adding `FAQPage` markup expecting a snippet (different feature, and FAQ rich
results were retired in May 2026), or restating the same answer in several formats hoping
one is picked.

**Opting out** is the part you genuinely control, and it is a commercial decision, not a
default: `nosnippet` blocks all snippets, `data-nosnippet` excludes marked text, and a low
`max-snippet` reduces length, though Google says a low `max-snippet` "doesn't guarantee that
Google will stop showing featured snippets for your page". See
`seo-access-read/references/titles-and-snippets.md`.

### The zero-click question, answered honestly

Holding a featured snippet can reduce clicks, because the searcher got their answer. That is
a real trade and the honest framing is: for a query whose whole value is the answer, the
snippet captures the brand impression and little else; for a query that is the start of a
task, it tends to earn the visit.

Never promise a traffic increase from winning a snippet. Report it as what it is, a position
on the page, and measure clicks for that query rather than assuming.

## People Also Ask

An expandable set of related questions, drawn from pages that answer them. The same logic as
featured snippets applies: being a candidate means ranking for the underlying question and
answering it plainly.

Its practical value is less about occupying it and more about **reading it**. The questions
shown are a free, live map of what the engine believes the sub-questions are, which is the
closest thing to a content brief Google publishes. Use it in `references/search-intent.md`
and when scoping a page's coverage.

Google does not document a mechanism for inclusion, so do not assert one.

## Sitelinks

The indented links beneath a result for a brand or a major page. Automated, not requested,
and influenced by site structure and internal linking rather than by markup.

The useful work is therefore ordinary Connect-rung work: a clear hierarchy, descriptive
internal anchor text, and pages that are genuinely distinct from one another. A site whose
navigation is ambiguous gives the generator nothing coherent to choose.

There is no way to specify sitelinks. Treat any claim to control them as a sign the source
is not reliable.

## Rich results, which are the ones you do influence

Distinct from the features above: rich results are driven by structured data, so eligibility
genuinely is in your hands, and this is where `seo-access-understand` does the work.

The rules that keep it honest are unchanged and absolute: mark up only what is real and
visible on the page, never fabricate ratings, reviews, authors or availability, and validate
against the current requirements rather than against a blog post.

What is gone is as important as what remains. **FAQ rich results were retired entirely in
May 2026** (restricted to government and health sites from 2023, then removed), so
`FAQPage` markup no longer produces a SERP feature. It remains valid schema and is still
worth having where the Q&As are genuine, for clarity and clean extraction, but never add it
expecting a rich result. Check the current status of any feature before promising it; this
category changes more often than any other in search.

## What to actually do with all this

In a report, SERP features belong in two places and neither is a promise:

1. **As a diagnosis.** "A competitor holds the featured snippet for this query, which is why
   our position 3 earns less than position 3 usually does." That explains a number somebody
   is confused by, and it is evidenced by looking at the SERP.
2. **As a consequence of doing the work.** Answer the question better and more plainly than
   the page currently holding the feature, and you become a candidate. That is the whole
   mechanism, and it is the same work as being worth choosing.

What never belongs in a report: a plan to "win N featured snippets", a timeline, or a
feature count presented as a deliverable. The claimable outcome is candidacy, and the
measurable outcome is position and clicks.
