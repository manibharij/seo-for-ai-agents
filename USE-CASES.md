# Use cases: the ladder, tuned to your kind of site

The Visibility Ladder is the same for every site — Reach → Read → Understand → Connect → **Rank**, with Cite (AEO) as the layer on top. What changes per site type is **where sites like yours actually fail** and **which checks matter most**. The pack encodes that as [site-type profiles](skills/seo-orchestrator/references/profiles/) which the orchestrator applies automatically: it infers your site type in Step 0, so you don't have to declare it.

This page is the orientation layer: which profile fits, what it emphasises, which skills carry the weight, and a copy-paste prompt to start with. Depth lives in each profile file.

> Profiles **combine**. An international shop → `ecommerce` + `international`. A SaaS with docs → `saas-marketing` + `documentation`. Profiles tune emphasis and add checks; they never fork the method or let you skip a rung.

| Your site | Profile | The classic failure | Weight highest |
|---|---|---|---|
| SaaS / product marketing | [`saas-marketing`](skills/seo-orchestrator/references/profiles/saas-marketing.md) | Marketing site is an SPA serving crawlers an empty shell | Reach, then Read + Cite |
| Online shop | [`ecommerce`](skills/seo-orchestrator/references/profiles/ecommerce.md) | Client-rendered prices; faceted-URL sprawl; variant duplication | Reach + Understand, then Connect |
| Local business | [`local-business`](skills/seo-orchestrator/references/profiles/local-business.md) | Inconsistent NAP; doorway pages with the town name swapped | Understand + Read |
| Blog / content site | [`content-blog`](skills/seo-orchestrator/references/profiles/content-blog.md) | Orphan posts, cannibalisation, thin archives | Read + Cite, then Connect |
| Documentation / help centre | [`documentation`](skills/seo-orchestrator/references/profiles/documentation.md) | Docs SPA invisible to the AI crawlers that want it most | Reach, then Cite + Read |
| News / publisher | [`news-publisher`](skills/seo-orchestrator/references/profiles/news-publisher.md) | Slow discovery, false timestamps, anonymous articles | Reach + Understand + Rank |
| Multi-country / multilingual | [`international`](skills/seo-orchestrator/references/profiles/international.md) *(modifier — combine it)* | Missing/one-way hreflang; every locale canonicalising to English | Connect, then Read |

## Starter prompts per site type

Each prompt is **read-only**: the agent audits and reports, and changes nothing until you ask. Swap in your details.

**SaaS / product marketing**
```
Use the seo-for-ai-agents skill pack with the saas-marketing profile: audit my marketing site on the served HTML. Check first whether marketing pages and pricing are server-rendered and readable by crawlers, then intent match, comparison pages, and internal architecture. Report only, don't change any code or files yet.
```

**E-commerce**
```
Use the seo-for-ai-agents skill pack with the ecommerce profile: audit my shop on the served HTML. Check product pages render prices and stock server-side, review faceted and variant URLs for duplication, and validate Product/Offer schema for honesty. Report only, don't change any code or files yet.
```

**Local business**
```
Use the seo-for-ai-agents skill pack with the local-business profile: audit my site on the served HTML. Check NAP consistency across pages and schema, LocalBusiness markup accuracy, and whether each location page has real, distinct content. Report only, don't change any code or files yet.
```

**Blog / content site**
```
Use the seo-for-ai-agents skill pack with the content-blog profile: audit my blog on the served HTML. Map topic clusters, find orphan posts and articles cannibalising the same intent, review author schema, and flag thin archives. Report only, don't change any code or files yet.
```

**Documentation / help centre**
```
Use the seo-for-ai-agents skill pack with the documentation profile: audit my docs site on the served HTML. Check content survives client-side rendering, review version canonicals and information architecture, and assess whether pages are answer-shaped enough to be cited. Report only, don't change any code or files yet.
```

**News / publisher**
```
Use the seo-for-ai-agents skill pack with the news-publisher profile: audit my news site on the served HTML. Check article bodies render server-side, verify NewsArticle schema and timestamp honesty, review the news sitemap, and assess byline and E-E-A-T signals. Report only, don't change any code or files yet.
```

**International / multilingual (combine with your base type)**
```
Use the seo-for-ai-agents skill pack with the international profile combined with my site type: audit my site on the served HTML. Verify hreflang reciprocity and self-references, per-locale canonicals, crawlability of every locale, and genuine localisation. Report only, don't change any code or files yet.
```

## The honest boundaries, per type

Some of what drives each site type lives **outside the build** — the pack states this rather than overselling:

- **Local** — Google Business Profile, reviews, and map-pack proximity are off-site and live. The pack fixes your owned site (NAP, `LocalBusiness` schema, real location pages) and points you across the boundary.
- **News** — Top Stories / Google News inclusion is Google's editorial and algorithmic call. Done right you're *eligible*, never guaranteed.
- **E-commerce on hosted carts** (Shopify, WooCommerce…) — diagnosis works everywhere (it reads the served HTML); fixes often live in theme/platform settings, so the agent instructs precisely instead of editing code it doesn't control.
- **Everywhere** — rankings and AI citations are earned outcomes influenced by competition and off-site authority. The pack improves eligibility; nothing can promise the outcome.

These guides also exist as web pages at [seo-ai-agents.com/use-cases](https://seo-ai-agents.com/use-cases/).
