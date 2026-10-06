# Profile: documentation / knowledge base

Use for developer/product docs, knowledge bases, and help centres. Docs are exceptionally strong **AEO** candidates — they're exactly what AI answer engines retrieve and cite — so Read, Connect, and Cite carry the weight. The usual technical trap is a **client-rendered docs SPA** failing Reach.

## How each rung shifts
- **Reach** — many docs frameworks are SPAs (or have search/versioning UIs) that can hide content from crawlers. Confirm doc content is in the served HTML. Versioned docs: ensure the canonical/current version is indexable and old versions handled deliberately.
- **Read** — accurate, complete, well-structured content with clear headings, code blocks, and definitions. Docs live or die on clarity and correctness. Match page to the task/question the reader has.
- **Understand** — `TechArticle`/`Article` where appropriate; `BreadcrumbList`; `FAQPage` for genuine Q&As (note: Google retired FAQ *rich results* entirely in May 2026, so for docs the value is clarity and AEO extraction, not a SERP rich result). Often lighter on schema than other types — clarity matters more.
- **Connect** — strong information architecture: a logical tree, prev/next, "related", and a clear canonical per page. Avoid orphan pages and duplicate content across versions/locales.
- **Cite** — the headline rung for docs. Question/task-shaped headings ("How do I authenticate?"), self-contained answers, copy-pasteable code, clear definitions, accurate `dateModified`. This is what gets quoted by ChatGPT/Claude/Perplexity and AI Overviews.

## Type-specific checks
- **Search/nav SPA hiding content:** the most common docs Reach failure — verify served HTML.
- **Versioning:** canonical to the current/stable version; `noindex` or canonical old versions deliberately so they don't duplicate or outrank current.
- **Code blocks:** real text in the served HTML (not images of code); language-tagged.
- **Anchor-linkable sections:** stable heading anchors so engines (and answers) can deep-link.
- **Freshness:** genuine `dateModified`; stale docs erode trust and citation.
- **Internationalised docs:** combine with `international.md`; avoid duplicate-content traps across locales.

## Docs generators: defaults to check

Most docs sites run on a generator, and its defaults decide Reach and Connect before anyone writes a page. Identify it from `package.json` or the config file, then check these on the **served** site. Details below were checked against each project's docs in October 2026 (verified 2026-10); defaults change between major versions, so confirm against the version in use.

| Generator | Rendering | Sitemap | Versions and canonicals |
|---|---|---|---|
| **Docusaurus** | Static site generator: pages are pre-rendered to HTML at build, then hydrate. | Built into `preset-classic`; generated only by a production build. Options include `lastmod`, `changefreq`, `ignorePatterns`. | Latest version at `/docs/`, the unreleased `current` at `/docs/next/`, older ones at `/docs/<version>/`. `lastVersion` chooses which version `/docs/` serves. Each version can set `noIndex: true` in the docs plugin's `versions` option. |
| **VitePress** | Static site generator. | Off until you set `sitemap: { hostname: 'https://example.com' }` in `.vitepress/config`. Append the `base` path to `hostname` if the site lives under one. | No versioning model of its own: versions are usually separate builds or branches. Check how the site does it. |
| **Starlight** (Astro) | Static HTML by default. | Generated once `site` is set in `astro.config.mjs`; nothing without it. | No versioning model of its own; check for a plugin or separate deployments. |
| **Mintlify** (hosted) | Hosted; check the served HTML yourself rather than trusting the platform's claim. | Generates `sitemap.xml` and `robots.txt` automatically. | Canonical is built from the page URL and can be overridden globally or per page; `noindex: true` in a page's frontmatter keeps it out of the index. |

Sources: https://docusaurus.io/docs/api/plugins/@docusaurus/plugin-sitemap, https://docusaurus.io/docs/versioning, https://docusaurus.io/docs/api/plugins/@docusaurus/plugin-content-docs, https://vitepress.dev/guide/sitemap-generation, https://starlight.astro.build/guides/customization/, https://www.mintlify.com/docs/optimize/seo.

What to do with versions, whatever the generator:
- **One indexable version per page:** the current stable release. It self-canonicalises.
- **Old versions people still use** (supported releases): keep them reachable for readers, and either `noindex` them (Docusaurus `noIndex: true`, Mintlify `noindex: true`) or canonicalise each page to its equivalent in the current version **only when the content is substantially the same**. A canonical to a page that says something different is a hint Google may ignore, and it hides the old version from people who need it.
- **The `next` or unreleased version:** `noindex` it, or keep it off the public build, so it does not compete with stable.
- **Sitemap:** list only the indexable version. Use the generator's ignore option (Docusaurus `ignorePatterns`, VitePress `transformItems`) to drop old and `next` paths.
- **Version banners:** a visible "you are reading an old version" banner with a link to the current page helps readers and makes the relationship clear.
- On an existing docs site, check Search Console before de-indexing a version: an old version may be what people search for. Flag it for sign-off.

## `llms.txt` for docs (optional, low certainty)

`llms.txt` is a proposed plain-text index of a site's pages for language models. Google says you do not need AI text files or special markup to appear in AI Overviews or AI Mode (verified 2026-10, https://developers.google.com/search/docs/appearance/ai-features), so do not expect it to help in Google Search. The pack's Cite reference records that some AI tools and coding agents fetch it, which makes docs the most defensible place for one (see `cite-aeo-geo/references/ai-crawlers-and-llms-txt.md`). Mintlify generates `/llms.txt` and `/llms-full.txt` automatically; for other generators, community plugins exist.

Treat it as optional and low certainty: it is cheap to add, Google does not need it, and its benefit elsewhere is not measured. Never let it replace the work that does matter here: content in the served HTML, a clean version strategy, and answer-shaped pages. If you add one, list only current, indexable pages, keep it generated from the same source as the sitemap so it cannot go stale, and do not put anything in it that is not on the site.

## Common failures
- Docs rendered only client-side → invisible to AI crawlers that don't run JS (a double miss: docs are exactly what those crawlers want).
- Old versions competing with current for the same queries.
- Walls of text with no question/task headings — hard to extract an answer from.
- Code shown as images.

## Priority tilt
Weight **Reach** (is it even served?) then **Cite** and **Read** highest — docs are the strongest AEO asset most products have. Get them reachable, clear, and answer-shaped.
