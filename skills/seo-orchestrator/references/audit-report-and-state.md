# The `.seo/` folder: audit report & persistent state

Read this for the exact files the lifecycle reads and writes. The agent creates a **`.seo/` folder in the user's project** (not in this pack) so progress survives across sessions and runs. It is committed alongside the user's code — visible, version-controlled, and diff-able.

```
<user-project>/.seo/
├── audit.md      # human-readable health report (read this first as a person)
├── state.json    # machine-readable issue tracker (the source of truth for status)
└── log.md        # dated history of runs (what changed each time)
```

> Tell the user the `.seo/` folder exists and what it's for. It's theirs — they can read `audit.md` any time to see where their SEO stands. Add it to version control; do **not** add it to `.gitignore` (its whole value is persisting and showing history).

---

## `state.json` — the source of truth

The machine state the agent updates each run. Keep it valid JSON. Suggested shape:

```json
{
  "version": 1,
  "site": { "url": "https://example.com", "stack": "next-app-router", "platform": "code", "profile": "saas-marketing" },
  "lastRun": "2026-06-03",
  "runs": 4,
  "scores": { "reach": "pass", "read": "minor", "understand": "fail", "connect": "pass", "cite": "minor" },
  "findings": [
    {
      "id": "understand-product-schema-missing",
      "rung": "understand",
      "title": "Product pages have no Product/Offer schema",
      "page": "/products/* (template)",
      "severity": "high",
      "effort": "medium",
      "priority": 8.5,
      "status": "open",
      "evidence": "No application/ld+json in served HTML on /products/widget",
      "firstSeen": "2026-05-20",
      "updated": "2026-06-03",
      "notes": ""
    }
  ]
}
```

Field notes:
- **`status`**: `open` | `fixed` | `needs-human` | `deferred` | `wontfix` | `regression`.
- **`severity`**: `critical` | `high` | `medium` | `low`. **`effort`**: `low` | `medium` | `high`.
- **`priority`**: the computed score (see `prioritisation.md`) used to sequence work.
- **`id`**: stable, human-readable slug — reused across runs so the same issue is tracked, not duplicated.
- **`evidence`**: what you observed in the **served HTML** (the proof, not an assumption).
- Dates as ISO `YYYY-MM-DD`. (Don't invent timestamps — use the date the user/agent is running.)

Rules:
- One finding per real issue; **reuse the `id`** on later runs rather than creating duplicates.
- When you fix something, set `status: fixed` and record the proof in `notes`/`evidence`. On the next run's regression check, if it broke, set `status: regression` (then back to `fixed` once re-fixed).
- Never delete history silently — `wontfix`/`deferred` stay in the file with a reason.

---

## `audit.md` — the human-readable report

What a person reads. Generated/updated from `state.json`. Suggested template:

```markdown
# SEO Audit — example.com
_Last run: 2026-06-03 · Run #4 · Stack: Next.js App Router · Profile: SaaS/marketing_

## Health scorecard (the Visibility Ladder)
| Rung | Status | Notes |
|------|--------|-------|
| 1. Reach | ✅ Pass | Content in served HTML; HTTPS; sitemap correct |
| 2. Read | 🟡 Minor | 3 pages missing meta descriptions; LCP image unoptimised |
| 3. Understand | 🔴 Failing | Product pages have no schema — **the floor** |
| 4. Connect | ✅ Pass | — |
| 5. Cite | 🟡 Minor | Answers buried on 2 key pages |

**Start here (the floor):** Understand — add honest Product/Offer schema to product pages.

## Open items (prioritised)
1. **[High]** Product pages have no schema — `/products/*` · effort: medium
2. **[Medium]** 3 pages missing meta descriptions — effort: low
3. **[Medium]** Buried answers on pricing & docs — effort: low
...

## Fixed (this run)
- ✅ Added self-referential canonicals to blog templates (verified in served HTML)

## Needs you (human decisions)
- Product pages have no real reviews — supply genuine ones and I'll mark them up (I won't invent them).

## Deferred / won't-fix
- Full responsive redesign of the legacy pricing table — deferred (large change), tracked.

## The boundary
These are build-time fixes. Actual rankings/citations need live measurement — not tracked here.
```

Keep it scannable: scorecard, the floor, prioritised open items, what was fixed (with proof), what needs the human, what's deferred, the boundary.

---

## `log.md` — the run history

A dated, append-only narrative so the trend is visible. Suggested entry:

```markdown
## 2026-06-03 — Run #4
- **Regressions caught:** 1 — blog canonicals had reverted after a template refactor; re-fixed.
- **New issues:** product pages shipped with no schema (new product section added).
- **Advanced:** added meta descriptions to 3 pages; surfaced buried answers on pricing.
- **Scores:** Reach ✅, Read 🟡, Understand 🔴 (was ✅ — new section), Connect ✅, Cite 🟡.
- **Next:** product schema (the floor); then the buried-answer formatting.
```

The log is where progression becomes legible — a reader can see the site getting healthier (or where a deploy set it back) run over run.

---

## Discipline
- **Read before you write.** On a progression run, load `state.json` and `log.md` before doing anything.
- **State reflects the served output.** A finding is only `fixed` if you verified it on what's actually served — not because you edited the source.
- **Don't fabricate progress.** If you didn't verify it, don't mark it fixed. The honesty rule applies to your own audit trail too.
