# Example 4 — Existing site: the audit lifecycle in action

A developer inherits an **existing, live** Next.js site with real traffic and points Claude Code at it: *"audit my SEO and fix what's safe."* This shows the pack working as a **system** — baseline audit → `.seo/` state → safe fixes that don't regress what ranks → a later run that catches a regression and advances. Not a new vibe-coded site; a real codebase with equity to protect.

*Stack: Next.js App Router. Profile: SaaS/marketing. Anonymised.*

---

## Run #1 — Baseline

The orchestrator checks for `.seo/` — **none exists**, so this is a first run. It detects the stack (Next.js App Router), the profile (SaaS/marketing), and that the site is **live with traffic** → the don't-regress discipline is on.

It walks the ladder top-to-bottom on a sample of templates (home, a feature page, the pricing page, a blog post), **on the served HTML**, and finds:

- **Reach** ✅ — content server-rendered, HTTPS, sitemap fine.
- **Read** 🟡 — 3 pages missing meta descriptions; the pricing page's hero image is a 2.4 MB unsized PNG (LCP + CLS).
- **Understand** 🔴 — **no schema anywhere** (the floor).
- **Connect** ✅ — links and canonicals fine.
- **Cite** 🟡 — the pricing answer is buried under "Our Approach" prose.

It writes the baseline into the project — a real `.seo/` folder the developer can read:

```
.seo/
├── audit.md      # scorecard + prioritised backlog (below)
├── state.json    # every finding with status/severity/effort
└── log.md        # run history
```

`.seo/audit.md` (excerpt):
```markdown
# SEO Audit — example.com
_Run #1 · 2026-06-03 · Next.js App Router · Profile: SaaS/marketing_

## Health scorecard
| Rung | Status |
|------|--------|
| 1. Reach | ✅ Pass |
| 2. Read | 🟡 Minor |
| 3. Understand | 🔴 Failing — the floor |
| 4. Connect | ✅ Pass |
| 5. Cite | 🟡 Minor |

Start here (floor): Understand — add Organization + SoftwareApplication schema.

## Open (prioritised)
1. [High] No structured data sitewide — effort: medium
2. [Med] 3 pages missing meta descriptions — effort: low
3. [Med] Pricing hero image 2.4 MB, unsized (LCP/CLS) — effort: low
4. [Med] Pricing answer buried — effort: low
```

### Fixes applied this run (safe + additive only)
The floor and the quick wins — all **additive**, nothing that risks existing rankings:
- Added honest `Organization` + `SoftwareApplication` JSON-LD (server-rendered; only true values).
- Wrote the 3 missing meta descriptions.
- Swapped the pricing hero to `next/image` (sized, lazy where appropriate, modern format) — LCP/CLS fixed.
- Surfaced a self-contained pricing answer under a question heading.

It did **not** touch the existing canonical strategy or URLs (they were intentional and working). Each fix verified on the served HTML; `state.json` updated to `fixed` with evidence; `log.md` gets a Run #1 entry.

> **Report to the developer:** "Your biggest gap was no structured data — added (honestly, only what's on your pages). Fixed 3 missing descriptions and a heavy pricing image hurting your Core Web Vitals, and surfaced your pricing answer for AI engines. I left your URLs and canonicals alone — they're correct. Nothing here changes what already ranks; it adds to it."

---

## Run #3 — Progression (two weeks and a deploy later)

_(Run #2, a week earlier, was a quiet check — nothing new shipped, no regressions; the lifecycle just re-verified the fixes still held and logged "no change". That's normal: most runs are uneventful, which is exactly the point of cheap, repeatable audits.)_

The developer runs it again. `.seo/` **exists**, so the orchestrator reads prior state first, then:

1. **Regression check** (before anything new): re-verifies each `fixed` item on the served HTML. The `Organization` schema is gone from several pages — a layout refactor in last week's deploy dropped it. → marked `regression`, **top priority**.
2. **New issues:** a new `/customers` section shipped client-rendered — its case-study content isn't in the served HTML (a Reach regression on new pages).
3. **Advance:** re-fixes the schema (and moves it somewhere the refactor won't drop it), flags the client-rendered `/customers` section with options.

`.seo/log.md` (excerpt):
```markdown
## 2026-06-17 — Run #3
- Regression: Organization schema dropped by the 2026-06-12 layout refactor — re-fixed.
- New: /customers section is client-rendered — content missing from served HTML (Reach). Flagged.
- Advanced: re-verified meta descriptions + pricing fixes still hold.
- Scores: Reach 🟡 (new section), Read ✅, Understand ✅, Connect ✅, Cite ✅.
```

> **Report:** "Heads up — a deploy on the 12th silently dropped the schema we added; I've restored it and made it more robust. Your new customers section is client-rendered, so crawlers can't see those case studies — here are three ways to fix it. Everything else we fixed still checks out."

---

**Why this example matters:** this is the difference between a one-shot script and a **system**. The `.seo/` folder makes every run build on the last; the regression catch is the payoff (a fix that quietly broke is worse than one never made); and the whole thing runs **conservatively on a live site** — additive fixes, URLs untouched, big changes flagged. That's what an existing site, with rankings to protect, actually needs from an AI agent.
