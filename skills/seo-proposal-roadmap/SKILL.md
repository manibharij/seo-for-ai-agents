---
name: seo-proposal-roadmap
description: >-
  Turn an audit into a clear, client-ready SEO proposal and prioritised roadmap —
  current-state summary, recommendations grouped into phases (quick wins →
  foundational → growth), effort/impact, realistic expected outcomes, and what the
  client must provide. Use on "create an SEO proposal", "build a roadmap", "SEO
  strategy document", "what should we do and in what order", or "present this to
  stakeholders". Builds the deliverable from the .seo/ audit and content findings;
  states outcomes honestly and never guarantees rankings.
---

# Proposal & Roadmap — package the audit into a plan

A specialist skill for the consultant/agency reality: an audit is only useful if a decision-maker can act on it. This turns the findings (from the orchestrator's `.seo/` state, the content audit, and positioning work) into a **proposal and a phased roadmap** a non-technical stakeholder can read, approve, and fund.

> It **packages and prioritises real findings** into a plan. It does not invent problems to pad scope, and it does not promise rankings, traffic, or revenue it can't guarantee. Honest expected outcomes, realistic effort, clear sequence.

Work: **Gather → Prioritise into phases → Draft the deliverable → Review with the user.**

---

## Step 1 — Gather

Pull together what's already been found (don't re-audit from scratch if state exists):
- The **`.seo/` state** — rung scores, the floor, open findings with severity/effort, regressions, what's fixed.
- The **content audit** results (keep/improve/consolidate/refresh/prune/create) if run.
- **Positioning/strategy** inputs (topical gaps, competitive context) if run.
- **Live data** if connected — real traffic/opportunity to size and justify priorities (cite it; otherwise base the case on build-time findings and say so).
If no audit exists yet, run the orchestrator's audit first — the proposal is downstream of real findings, never a generic template.

## Step 2 — Prioritise into phases

Group recommendations into a sensible sequence (respecting the ladder's dependency order and impact × effort — see `seo-orchestrator/references/prioritisation.md`):
- **Phase 1 — Foundations & quick wins.** Clear the floor (e.g. fix what's not indexable) and the high-impact/low-effort wins. Visible early progress.
- **Phase 2 — Build.** The bigger structural and content work (schema, architecture, content improvements/consolidation, migrations).
- **Phase 3 — Growth.** Positioning, topical-authority expansion, content creation briefs, AEO depth — the compounding work.
Map each item to effort, impact, dependencies, and who owns it (agent-doable vs human decision vs client-supplied).

## Step 3 — Draft the deliverable

Write a clear document (template in `references/proposal-format.md`) — typically saved as `.seo/proposal.md` (or wherever the user wants):
- **Executive summary** — where the site stands and the headline opportunities, in plain language.
- **Current state** — the scorecard and the most important findings (with live-data evidence where available).
- **Recommendations, phased** — what, why it matters, effort/impact, sequence.
- **Expected outcomes — honestly framed.** Direction and rationale, **not** numeric guarantees. ("Fixing indexation should let these pages be found at all; how much traffic follows depends on competition and demand, which we'd track with live data.") See the honesty rules in the reference.
- **What we need from you** — the human decisions and the real content/trust inputs the work depends on.
- **The boundary** — build-time work vs ongoing live measurement/managed optimisation.

## Step 4 — Review

Present it for the user to review and adjust (scope, phasing, framing) before it goes to a stakeholder/client. It's a draft they own, not a finished claim. Keep it in version control.

---

## Honesty rules for proposals (non-negotiable)
- **No guarantees.** Never promise rankings, "page 1", traffic numbers, or revenue. Frame outcomes as direction + rationale + what to measure.
- **No invented problems or inflated scope.** Recommend only what the findings support; don't manufacture issues to sell more work.
- **No fabricated metrics.** Every number in the proposal is real (from connected live data or the user's own figures), cited as such — never illustrative numbers dressed as projections.
- **Realistic effort/timelines** — don't undersell the big rocks (e.g. an SPA→SSR migration) to make the proposal look easy.
- This protects the user's credibility: a proposal that over-promises is the fastest way to lose a client's trust.

## Reference files
- `references/proposal-format.md` — the deliverable template (sections, phasing, an example outcomes section framed honestly) and the dos/don'ts of outcome language.
