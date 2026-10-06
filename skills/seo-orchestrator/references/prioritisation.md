# Prioritising findings

Read this to turn a pile of findings into a sensible order of work. An audit that lists twenty issues with no priority is the flat-checklist failure all over again. Two forces decide order: **the ladder's dependency rule** (hard constraint) and a **priority score** (soft ranking within what the ladder allows).

The order serves all three modes (`operating-modes.md`). `audit` presents findings in this order, with a `ref` each, so the user can approve from the top. `fix` applies the approved ones in this order. `re-check` reports regressions first.

---

## The hard constraint: ladder order wins

You may not fix a higher rung while a lower one fails for the same page. So **rung order is the outer sort**: clear the floor first. A "critical" Cite issue does not jump ahead of a failing Reach issue on the same page — an answer engine can't cite a page it can't reach. Within what the ladder permits, use the score below.

Exception that overrides even a tidy score: **regressions** (something previously fixed that broke again, recorded as `status: regression`) go to the front of their rung. A reverted fix signals active breakage.

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

## Use data when it is there

Without live data, impact is a judgement from the rung, the template's size and the page's role. With a data capability (`live-data-integrations.md`), weight impact by what the pages actually earn, and cite the source and date range in `evidence`:

- **Search performance:** clicks and impressions by page. A Reach failure on a template with 40,000 impressions a month outranks the same failure on a template with 200. A striking-distance query (roughly position 8 to 20, judgement) on a page with real impressions is a strong Rank candidate.
- **Revenue or leads by landing page:** when analytics or a CRM is connected, a page that earns money outranks one that only earns visits.
- **Field data:** a Core Web Vitals failure in real-user data outranks a lab-only warning.
- **Third-party estimates:** use keyword demand to size gaps, labelled as estimates; never let an estimate outrank observed clicks.

Data reorders findings within what the ladder allows. It never lets a high-traffic Cite item jump a failing Reach item on the same page. With no data, say the order is judgement and name the capability that would sharpen it.

## Protect pages that earn traffic

The pages with the most clicks or revenue are the ones a careless change can hurt most. Ranking them high for attention is right; ranking a change to them as a quick win is wrong.

- **Additive fixes** on these pages (missing schema, alt text, a sized image) keep their normal priority.
- **Changes to the title, `h1`, copy or URL** of a page that earns meaningful traffic are never quick wins, whatever their effort. Record the risk as "High: page earns traffic", present the page's numbers with the proposed change, and leave `approved: false` until the user signs off for that page (`existing-site-safety.md`).
- **Without data**, treat the homepage, main hubs and any page the user or `.seo/context.md` names as important as earning traffic, and say that is an assumption.

---

## Practical sequencing

Work in this order:
1. **Regressions** (previously fixed, now broken, `status: regression`): front of the queue.
2. **The floor** — the lowest failing rung; clear it before climbing.
3. **High-impact, low-effort wins** within the allowed rungs — the "quick wins" that move the score fast and build trust with the user.
4. **High-impact, high-effort** items — schedule these deliberately; they often need a human decision (e.g. re-architecture). Flag, don't force.
5. **Low-impact items** — batch them; don't let them crowd out the above.

## Quick wins vs big rocks
Call these out separately in the report:
- **Quick wins** (high impact, low effort, low risk): meta descriptions on pages that lack them, alt text, a missing canonical on a new page, sizing images. These are the natural candidates for "approve all low-risk". A stray `noindex` is high impact and low effort, but on a live site it may be deliberate: confirm before calling it a quick win.
- **Big rocks** (high impact, high effort): SPA→SSR, a content overhaul, an information-architecture change, a site migration. These usually carry risk and need the user's sign-off — present options and trade-offs (see `existing-site-safety.md`).

## Don't over-fix in one run
Especially on a large or established site, recommend approving the floor and the quick wins first, then leave a clear, prioritised backlog in `.seo/` for the next run. Progress compounds; doing too much at once raises regression risk and makes a dated change impossible to measure on its own.

## Top-N: working to a budget

When the user sets a budget, honour it exactly and stop when it is spent (`operating-modes.md`, Scope budgets).

**Picking N.**
- **A count** ("top 3 fixes", "five quick wins"): N is that number. Do not round up because the next item looks easy.
- **A time budget** ("30 minutes", "a quick look"): estimate each item's effort, keep roughly a fifth of the time for verifying and reporting (a judgement call), and set N to what fits in the rest. Verification is part of the fix, so an item you cannot verify in time does not count.
- **A vague budget** ("the main things", "quick wins"): take N = 5 and say so. That default is judgement; the user can widen it.
- **No budget:** there is no N. Follow "Don't over-fix in one run" below.

**Choosing the N.** Take them from the order in "Practical sequencing": regressions, then the floor, then quick wins. A template-level fix counts once however many URLs it covers. If the top item is a big rock that needs sign-off, report it first as `needs-human`, count it, and continue with the next fixable items: the user should never get three quick wins while the floor stays hidden. In `audit`, the N are findings with proposed fixes; in `fix`, they are the first N approved findings; without write access they are instructions, not edits.

**Stopping.** After the Nth item, stop. End the report with **What remains**: every other open finding by `id`, severity and one line, in priority order, so the next run or the next person starts there. Where `.seo/` is writable, the remaining items stay `open` (or `deferred`) in `.seo/state.json`.

## Profile and stack tilt the weights
The active **profile** changes impact weighting — e.g. on e-commerce, Product schema and faceted-URL control are high-impact; on a content site, clear self-contained answers and internal linking matter more. The **stack/platform** changes effort — a fix that's trivial in Next.js may be awkward on a hosted CMS. Let `references/profiles/<type>.md` and `references/stack-and-platform-adapters.md` adjust the ranking.
