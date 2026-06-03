# Prioritising findings

Read this to turn a pile of findings into a sensible order of work. An audit that lists twenty issues with no priority is the flat-checklist failure all over again. Two forces decide order: **the ladder's dependency rule** (hard constraint) and a **priority score** (soft ranking within what the ladder allows).

---

## The hard constraint: ladder order wins

You may not fix a higher rung while a lower one fails for the same page. So **rung order is the outer sort**: clear the floor first. A "critical" Cite issue does not jump ahead of a failing Reach issue on the same page — an answer engine can't cite a page it can't reach. Within what the ladder permits, use the score below.

Exception that overrides even a tidy score: **regressions** (something previously fixed that broke again) go to the front of their rung. A reverted fix signals active breakage.

---

## The priority score: impact × effort × confidence

For each finding, weigh three things:

- **Impact** — how much it affects being found/read/understood/cited. A page invisible to crawlers (Reach) is near-maximal impact; a missing Open Graph tag is low. Weight by *reach of the issue* too: a problem in a template that affects 500 pages outranks the same problem on one page.
- **Effort** — how much work to fix. A missing meta description (low) beats a full SPA→SSR re-architecture (high) for quick wins.
- **Confidence** — how sure you are it's real and that the fix will help. Verified-on-served-HTML findings are high confidence; hunches are low. Don't spend effort on low-confidence items before confirming them.

A simple, transparent way to combine them (use whatever keeps the ordering sensible — the number is a tool, not a fetish):

```
priority ≈ (impact × confidence) / effort
```
Higher = do sooner. Severity (`critical`/`high`/`medium`/`low`) is a useful shorthand for impact × reach; record both the score and the severity in `state.json`.

---

## Practical sequencing

Work in this order:
1. **Regressions** (previously fixed, now broken) — front of the queue.
2. **The floor** — the lowest failing rung; clear it before climbing.
3. **High-impact, low-effort wins** within the allowed rungs — the "quick wins" that move the score fast and build trust with the user.
4. **High-impact, high-effort** items — schedule these deliberately; they often need a human decision (e.g. re-architecture). Flag, don't force.
5. **Low-impact items** — batch them; don't let them crowd out the above.

## Quick wins vs big rocks
Call these out separately in the report:
- **Quick wins** (high impact, low effort): meta descriptions, alt text, a stray `noindex`, a missing canonical, sizing images. Do these early — visible progress, low risk.
- **Big rocks** (high impact, high effort): SPA→SSR, a content overhaul, an information-architecture change, a site migration. These usually carry risk and need the user's sign-off — present options and trade-offs (see `existing-site-safety.md`).

## Don't over-fix in one run
Especially on a large or established site, it's fine to clear the floor and the quick wins, then leave a clear, prioritised backlog in `.seo/` for the next run. Progress compounds; you don't have to do everything at once, and doing too much at once raises regression risk.

## Profile and stack tilt the weights
The active **profile** changes impact weighting — e.g. on e-commerce, Product schema and faceted-URL control are high-impact; on a content site, answer-block formatting and internal linking matter more. The **stack/platform** changes effort — a fix that's trivial in Next.js may be awkward on a hosted CMS. Let `references/profiles/<type>.md` and `references/stack-and-platform-adapters.md` adjust the ranking.
