# Profile: SaaS / product marketing

Use for SaaS and product marketing sites, app landing pages, and B2B sites. The classic failure mode is technical: the marketing site is a **client-rendered app** (the team are app developers), so it fails **Access** while looking perfect. Value then concentrates in Substance (clear value and real intent match), Identity (one provable company entity), and the Connect rung of Access (feature, use-case and comparison architecture).

## How the five systems shift

- **Demand** (observed). Buyers ask in distinct shapes: problem-aware, solution-aware, comparison ("X vs Y", "best tool for X"), and branded. Read which of those this product could credibly hold before planning a single page. Never invent the list.
- **Identity** (built). One resolvable company entity across the site, the docs, the profiles and the directories buyers check, with provable differentiators and real proof rather than "platform that empowers teams". An engine that cannot work out who you are has nothing to recommend.
- **Substance** (built). Clear articulation of what the product does, for whom, and the problem it solves, matched to real search intent. Honest comparison pages that genuinely help a buyer decide. Thin competitor-bait "alternatives" pages are a finding, not an output.
- **Access** (built). The Visibility Ladder, in dependency order. Diagnose top to bottom, fix bottom to top.
  1. **Reach.** The prime suspect. Marketing pages built in the same SPA as the app often serve an empty shell to crawlers. Verify content is in the served HTML; this is frequently *the floor*. Keep the marketing site server-rendered (or static) even if the app is an SPA.
  2. **Read.** Real titles, headings and body copy in the served HTML, pricing readable rather than locked inside a JS-only widget, and Core Web Vitals that survive heavy interactivity and animation.
  3. **Understand.** `Organization`/`SoftwareApplication` where appropriate; `BreadcrumbList`; `FAQPage` for genuine FAQs (note: FAQ rich results were retired in May 2026, so the value is clarity). `Product`/`Offer` only if you genuinely list pricing as products.
  4. **Connect.** A coherent architecture: features, use-cases, integrations, comparisons, and a real blog or resources hub, interlinked. Comparison and alternative pages need internal links and clear canonicals.
- **Distribution** (earned, advisory). Review sites, software directories, integration marketplaces and developer communities shape what a buyer sees before they ever reach the site. Audit the gap and write the strategy. Never execute outreach, arrange placement or buy anything.

**On assistant surfaces.** Buyers put exactly these questions to an assistant: "best tool for X", "X vs Y", "how do I do Z". Self-contained answers, honest comparison tables and one consistent company entity improve **eligibility** to be named, and eligibility is the only outcome that may ever be claimed. Presence can be sampled across a few prompts; it cannot be measured like a ranking, and it cannot be guaranteed. See `surfaces/` and `seo-surface-assistants`.

## Type-specific checks
- **Marketing vs app rendering:** confirm the *marketing* routes are server-rendered/static even if the product app is CSR. A common, high-impact fix.
- **Pricing page:** real, crawlable pricing content (not a JS-only widget); clear, answerable.
- **Comparison / "vs" / alternatives pages:** legitimate, honest, genuinely useful — not thin competitor-bait. High citation value when real.
- **Docs:** if there's a docs site, treat it with `documentation.md`; link it into the architecture.
- **Conversion vs SEO balance:** heavy interactivity/animation can wreck Core Web Vitals and Reach — keep indexable content server-rendered.

## Common failures
- The whole marketing site is an SPA invisible to crawlers (Access at Reach, the big one).
- Vague, benefit-free copy that matches no real query (Substance).
- Heavy JS tanking LCP/INP (Access, at the Read rung).
- Thin "alternatives" pages that add no value (Substance).

## Priority tilt
Check **Access** first and hard, because rendering is the usual floor. Then **Substance** (intent-matched clarity) and **Identity** (one provable company entity), which together are also what carries eligibility on assistant surfaces.
