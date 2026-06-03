# Decay, cannibalisation, and the action decision

Read this to spot two common content problems and to assign each page a single clear action. This is the decision layer of the content audit.

---

## Content decay

**Decay** is content that used to perform and is slowly losing traffic/rankings — usually because it's gone stale, competitors improved, or the SERP/intent shifted. It's often a site's biggest, cheapest opportunity: refreshing a decaying page that already has authority beats writing a new one.

- **With Search Console:** look for pages with a downward clicks/impressions trend over 3–12 months. That's the decay signal.
- **Without GSC:** infer from outdated content on time-sensitive topics (old dates, superseded facts, "in 2022…"), and flag that you're inferring.
- **Action:** **Refresh** — genuinely update the content (new information, current examples, re-verify claims), then update `dateModified` truthfully. Never just bump the date without updating the substance.

---

## Keyword cannibalisation

**Cannibalisation** is multiple pages targeting the same intent/query, so they compete with each other — splitting signals and confusing engines about which to rank. Common on content sites that published several overlapping posts over the years.

- **Detect:** group pages by the intent/topic they target. With a keyword tool or GSC, look for multiple URLs surfacing for the same query (and trading positions). Without, spot near-duplicate topics/titles.
- **Action:** usually **Consolidate** — merge the overlapping pages into one strong, comprehensive page, and `301` the others to it (hand the redirects to `seo-migrations` so equity is preserved). Occasionally the fix is to *differentiate* them clearly (genuinely distinct intents that were blurred).
- Don't "fix" cannibalisation by `noindex`-ing one of two genuinely useful, distinct pages — only consolidate true overlaps.

---

## The action decision (one per page)

Assign exactly one:

| Action | When | Then |
|---|---|---|
| **Keep** | Performs well, good quality, right intent | Leave it; maybe add internal links to it |
| **Improve** | Good topic/bones, but thin, unclear, weak intent match, or weak E-E-A-T | Hand to `seo-content-editing` (edit real content; brief the human for missing substance/E-E-A-T) |
| **Refresh** | Decaying or outdated, but fundamentally worth keeping | Genuinely update content + truthful `dateModified` |
| **Consolidate** | Cannibalising / overlapping thin pages | Merge into one strong page; `301` the rest (`seo-migrations`) |
| **Prune** | Genuinely valueless, no traffic, no purpose | Remove or `noindex` — carefully; `301` if it has any equity (`seo-migrations`) |
| **Create** | A real, in-demand topic gap with no page | Write a **content brief** for a human; this skill briefs, it does not auto-generate articles |

### Prioritise the actions
- **With GSC:** weight by real traffic and opportunity — refresh the high-traffic decayers and improve the high-impression/low-click pages first.
- **Without:** weight by topical importance, intent value, and effort (quick wins first).
- Record each page's action and basis in `.seo/` so the lifecycle tracks the content backlog alongside the technical one.

---

## The white-hat lines (same as ever)
- **Create = brief, not generate.** The content audit identifies gaps and writes briefs for a human (or a human-supervised process). It does not silently auto-generate articles to fill the index — mass-generated thin content is exactly what engines now discount.
- **Prune carefully.** Don't delete pages with traffic or links without confirming and redirecting. On an existing site, treat removals as high-risk (see `seo-orchestrator/references/existing-site-safety.md`).
- **Refresh honestly.** Update the content, then the date — never the date alone.
- **Don't fabricate the missing substance, sources, or E-E-A-T** — flag those as human tasks.
