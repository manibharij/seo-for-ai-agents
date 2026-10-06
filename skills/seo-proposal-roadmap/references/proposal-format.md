# Proposal & roadmap — format and honest outcome language

Read this for the deliverable's structure and, crucially, how to write the outcomes section without over-promising. The proposal is built from real findings; its job is to make them fundable and actionable, not to oversell.

---

## Template

```markdown
# SEO Proposal & Roadmap — <site>
_Prepared <date> · Based on audit run #N · Stack: <stack> · Profile: <type>_

## Executive summary
2 to 4 jargon-free sentences: where the site stands, the single biggest opportunity,
and the shape of the plan. Written for a decision-maker, not an SEO.

## Where the site stands today
- Visibility Ladder scorecard (Reach/Read/Understand/Connect/Rank, plus Cite on top) + the floor.
- The 3–5 most important findings, each in one line, with evidence.
  (Cite live data where connected: "1,200 impressions/mo, avg position 12 — strong upside.")

## Recommendations & roadmap
### Phase 1 — Foundations & quick wins (clear the floor + high-impact/low-effort)
| Recommendation | Why it matters | Effort | Owner |
|---|---|---|---|
| ... | ... | Low/Med/High | Agent / Human decision / Client-supplied |
### Phase 2 — Build (structural + content)
| ... |
### Phase 3 — Growth (positioning, topical authority, content briefs, AEO depth)
| ... |

## Expected outcomes (honest)
Direction and rationale per phase — NOT numeric guarantees. (See outcome language below.)

## What we need from you
- Decisions only you can make (e.g. URL-structure changes, prune approvals).
- Real inputs we won't invent (author credentials, data, sources, genuine reviews).
- Access (e.g. connect Search Console / a keyword tool for live prioritisation).

## Scope boundary
Build-time, owned-media work is in scope. Off-site authority (earned media) and ongoing
live measurement/managed optimisation are separate (your own data tools, or the managed tier).
```

Adapt length to the audience — a solo founder wants it short; an enterprise stakeholder may want detail. Save as `.seo/proposal.md` (or where the user prefers); keep it in version control.

---

## Outcome language — the dos and don'ts

This is where proposals destroy or build trust. The rule: **describe direction, mechanism, and what you'd measure — never promise a number or a position.**

**Don't:**
- "We'll get you to page 1 / position 1 for X."
- "This will increase traffic by 50%."
- "Guaranteed rankings / leads / revenue."
- Illustrative numbers presented as projections ("expect ~10k visits").

**Do:**
- "Your product pages currently aren't indexable, so they can't rank at all; fixing that makes them *eligible* to compete. How far they climb depends on competition and demand."
- "These pages get impressions but few clicks (GSC), suggesting a title/intent gap — improving them targets that gap; we'd track clicks to confirm."
- "Refreshing the decaying guides aims to recover the traffic they're losing; we'd measure against their current baseline."
- "This makes pages eligible for AI citation; whether engines cite them isn't guaranteed and we'd monitor it."

Every claim ties to a **mechanism** (why it should help) and a **measurement** (how we'll know), with honest uncertainty. If live data is connected, you can quote real *current* figures as the baseline — but current data is never a promise of future results.

---

## Keep it real
- Build only from findings that exist; cite their basis (served-output evidence or connected live data).
- Don't manufacture problems to inflate scope, or hide the big rocks to look cheap.
- Flag the human-decision and client-supplied items honestly — a plan that pretends the agent can do everything alone sets up failure.
- The proposal is the user's deliverable to review and own before it reaches a client.

---

## Output variants

The proposal document above is the default. The same plan often needs another shape: for the team that does the work, or for the meeting that approves it. Build every variant from the findings in `.seo/state.json`, which use the shared schema in `seo-orchestrator/references/audit-report-and-state.md` (Specialist findings). Keep each finding's `id`, so anyone can trace a ticket, a row or a slide back to its evidence. The ticket, CSV and PR formats below extend the base exports in that file (Exports) with what a roadmap adds: a phase, an effort and an owner. The honesty rules do not relax because the format is shorter.

### Ticket list (Linear or Jira)

One ticket per recommendation, or one per template when a single fix covers many URLs, written so an engineer can pick it up cold. Save as `.seo/tickets.md`. Create the issues in the tracker only when the user has connected it and asked you to.

```markdown
### [Phase 1 · High] Server-render the /customers case studies

**Labels:** seo, reach · **Estimate:** medium · **Owner:** engineering
**Blocked by:** none · **Finding id:** `reach-customers-csr`

**Why**
The case-study text is not in the served HTML, so crawlers that do not run JavaScript see an empty page, and those pages cannot rank or be cited.

**Evidence**
`curl -sL https://example.com/customers/acme | grep -c "<p"` returns 0 (2026-06-17). The text appears only after hydration.

**Change**
Fetch the case-study data in the server component for `app/customers/[slug]/page.tsx` instead of in a client `useEffect`.

**Acceptance (checked on the served output)**
- [ ] The case-study body text appears in `curl` output for three customer pages.
- [ ] Titles, canonicals and URLs for `/customers/*` are unchanged.

**Risk and rollback**
Low: same URLs and content, rendered earlier. Revert the PR to roll back.
```

Map `severity` to the tracker's own priority field rather than inventing levels. Linear's documented importers bring issues in from other trackers or through a CLI, not from an arbitrary CSV (verified 2026-10, [Linear import docs](https://linear.app/docs/import-issues)), so for Linear use this Markdown, or the tracker's API or MCP if the user has connected one. For Jira, the CSV below imports directly.

### CSV

For spreadsheets and Jira's CSV importer. Jira requires a column for Summary data and advises a header row without punctuation (verified 2026-10, [Jira Cloud CSV import](https://support.atlassian.com/jira-cloud-administration/docs/import-data-from-a-csv-file/)), so this variant adds `summary`, `phase`, `effort`, `owner` and `depends` to the base columns. Quote any field that contains a comma, quote or line break, and double any quote inside it. Save as `.seo/roadmap.csv`.

```csv
phase,summary,id,skill,area,target,severity,effort,owner,depends,evidence,fix,risk,status,verified,notes
1,Server-render the customers case studies,reach-customers-csr,1-reach-indexation,reach,/customers/*,high,medium,engineering,,"curl: no case-study text in served HTML on /customers/acme","Fetch data in the server component, not useEffect","Low: same URLs and content",open,2026-06-17,
```

`status` uses the shared values: `open`, `fixed`, `regression`, `needs-human`, `wont-fix`.

### PR description

Use the base PR template in `audit-report-and-state.md` (Exports), and add two lines a roadmap reader needs:

```markdown
**Roadmap:** Phase 1 of 3 · items <ids> · next: Phase 2 (<one line>)
**Not promised:** these changes make the pages eligible to be indexed and cited; they do not guarantee rankings or citations.
```

### Slide outline

For a meeting. One idea per slide, the evidence on the slide, the detail in the speaker notes. Save as `.seo/slides.md`.

```markdown
1. **Where the site stands:** the ladder scorecard and the floor in one line.
2. **What is holding it back most:** the floor finding, with an excerpt of the served output.
3. **Phase 1, foundations and quick wins:** three to five items, each with effort and owner.
4. **Phase 2, build:** the structural and content work, with the big rocks named honestly.
5. **Phase 3, growth:** positioning, topical authority, content briefs, AEO depth.
6. **What we expect and how we will know:** direction and mechanism per phase, and the measure for each. No promised numbers.
7. **What we need from you:** decisions, real inputs, access.
8. **Scope and the decision today:** build-time work versus live data and earned media, and the approval being asked for.
```

### Executive summary

For a decision-maker with five minutes: 150 to 250 words, no jargon, no table. Save as `.seo/summary.md`.

```markdown
# <Site>: SEO summary, <date>

**Where it stands.** <One or two sentences on the floor and what it costs the business.>
**What we recommend first.** <Phase 1 in one sentence, and why it comes first.>
**What follows.** <Phases 2 and 3, one sentence each.>
**What we need from you.** <The two or three decisions or inputs that gate the work.>
**What to expect.** <Direction and mechanism, and how progress will be measured. No guaranteed numbers.>
```

---

## Worked example: a phased roadmap

The site is the one in `examples/04-existing-site-audit-lifecycle.md`: a live Next.js App Router SaaS site, anonymised. The proposal is built after Run #3 from the findings in `.seo/state.json`. No live data is connected, so the case rests on served-output evidence, and the proposal says so.

**Findings in state (abridged)**

| id | area | target | severity | status | evidence |
|---|---|---|---|---|---|
| `understand-no-schema` | understand | sitewide | high | fixed | no JSON-LD in Run #1; dropped by the 2026-06-12 layout refactor and marked `regression`; restored in Run #3 |
| `read-missing-descriptions` | read | 3 pages | medium | fixed | no meta description in served HTML |
| `read-pricing-hero` | read | /pricing | medium | fixed | hero PNG 2.4 MB with no dimensions |
| `cite-pricing-buried` | cite | /pricing | medium | fixed | pricing answer under "Our Approach" prose |
| `reach-customers-csr` | reach | /customers/* | high | open | case-study text absent from served HTML |
| `rank-blog-no-author` | rank | /blog/* | medium | needs-human | no named author on any post (an illustrative addition to the example) |

**Roadmap**

| Phase | Item | Why it matters | Effort | Owner |
|---|---|---|---|---|
| 1. Foundations | `reach-customers-csr`: server-render `/customers` | Crawlers cannot see the case studies, so those pages cannot rank or be cited. | Medium | Engineering, agent drafts the change |
| 1. Foundations | Regression gate for schema | The schema fix already broke once in a refactor; a CI check stops a silent repeat (`seo-automations`). | Low | Agent |
| 2. Build | `rank-blog-no-author`: real bylines on the blog | Posts with no named author are weaker candidates where readers look for expertise. | Low once the names exist | Client supplies names and roles |
| 2. Build | Content audit of `/blog` | Decide keep, improve, consolidate or prune before writing more. | Medium | Agent, with your approval on any prune |
| 3. Growth | Topical map (`seo-positioning-strategy`) | Concentrate new content where the business has standing. | Medium | Agent drafts, you decide |

The four fixed items appear under "Where the site stands today" as progress already made, not as new scope.

**Expected outcomes, worded honestly**
- Phase 1: "Your customer stories are invisible to search engines today. Server-rendering them makes them eligible to be indexed and cited. We will confirm the text is in the served HTML straight away, and watch indexation in Search Console once you connect it."
- Phase 2: "Real, named authors strengthen the blog on topics where readers look for expertise. We cannot say how far that moves rankings; we will compare the posts before and after."

**What we need from you:** the names and roles of the people who actually write the blog; approval before any post is pruned or merged; Search Console access, so progress is measured rather than asserted.

**One plan, several shapes.** The ticket list carries `reach-customers-csr` and the regression gate into the sprint. The CSV feeds the stakeholder's spreadsheet. The PR description goes with the `/customers` change. The executive summary leads with the customer pages because they are the floor.
