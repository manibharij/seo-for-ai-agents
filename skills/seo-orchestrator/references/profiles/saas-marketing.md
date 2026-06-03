# Profile: SaaS / product marketing

Use for SaaS and product marketing sites, app landing pages, and B2B sites. The classic failure mode is technical: the marketing site is a **client-rendered app** (the team are app developers), so it fails **Reach** while looking perfect. Value then concentrates in Read (clear value/intent), Connect (feature/use-case/comparison architecture), and Cite (these queries are heavily AI-answered).

## How each rung shifts
- **Reach** — the prime suspect. Marketing pages built in the same SPA as the app often serve an empty shell to crawlers. Verify content is in the served HTML; this is frequently *the floor*. Keep the marketing site server-rendered (or static) even if the app is an SPA.
- **Read** — clear articulation of what the product does, for whom, and the problem it solves — matched to real search intent (problem-aware, solution-aware, comparison, branded). Avoid vague "platform that empowers teams" copy that says nothing.
- **Understand** — `Organization`/`SoftwareApplication` where appropriate; `BreadcrumbList`; `FAQPage` for genuine FAQs (note: FAQ rich results are restricted now — value is AEO/clarity). `Product`/`Offer` only if you genuinely list pricing as products.
- **Connect** — a coherent architecture: features, use-cases, integrations, comparisons, and a real blog/resources hub, interlinked. Comparison and alternative pages need internal links and clear canonicals.
- **Cite** — strong here: buyers ask AI engines "best tool for X", "X vs Y", "how to do Z". Self-contained answers, honest comparison tables, genuine docs/expertise make you citable. Entity consistency (one clear company identity) matters.

## Type-specific checks
- **Marketing vs app rendering:** confirm the *marketing* routes are server-rendered/static even if the product app is CSR. A common, high-impact fix.
- **Pricing page:** real, crawlable pricing content (not a JS-only widget); clear, answerable.
- **Comparison / "vs" / alternatives pages:** legitimate, honest, genuinely useful — not thin competitor-bait. High citation value when real.
- **Docs:** if there's a docs site, treat it with `documentation.md`; link it into the architecture.
- **Conversion vs SEO balance:** heavy interactivity/animation can wreck Core Web Vitals and Reach — keep indexable content server-rendered.

## Common failures
- The whole marketing site is an SPA invisible to crawlers (Reach — the big one).
- Vague, benefit-free copy that matches no real query (Read).
- Heavy JS tanking LCP/INP (Read/page experience).
- Thin "alternatives" pages that add no value (Read/Cite).

## Priority tilt
Check **Reach** first and hard (rendering is the usual floor), then **Read** (intent-matched clarity) and **Cite** (comparison/answer formatting).
