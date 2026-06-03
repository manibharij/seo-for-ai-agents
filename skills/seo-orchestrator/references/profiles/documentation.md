# Profile: documentation / knowledge base

Use for developer/product docs, knowledge bases, and help centres. Docs are exceptionally strong **AEO** candidates — they're exactly what AI answer engines retrieve and cite — so Read, Connect, and Cite carry the weight. The usual technical trap is a **client-rendered docs SPA** failing Reach.

## How each rung shifts
- **Reach** — many docs frameworks are SPAs (or have search/versioning UIs) that can hide content from crawlers. Confirm doc content is in the served HTML. Versioned docs: ensure the canonical/current version is indexable and old versions handled deliberately.
- **Read** — accurate, complete, well-structured content with clear headings, code blocks, and definitions. Docs live or die on clarity and correctness. Match page to the task/question the reader has.
- **Understand** — `TechArticle`/`Article` where appropriate; `BreadcrumbList`; `FAQPage` for genuine Q&As (note: since 2023 Google restricts FAQ *rich results* to government and health authorities, so for docs the value is clarity and AEO extraction, not a SERP rich result). Often lighter on schema than other types — clarity matters more.
- **Connect** — strong information architecture: a logical tree, prev/next, "related", and a clear canonical per page. Avoid orphan pages and duplicate content across versions/locales.
- **Cite** — the headline rung for docs. Question/task-shaped headings ("How do I authenticate?"), self-contained answers, copy-pasteable code, clear definitions, accurate `dateModified`. This is what gets quoted by ChatGPT/Claude/Perplexity and AI Overviews.

## Type-specific checks
- **Search/nav SPA hiding content:** the most common docs Reach failure — verify served HTML.
- **Versioning:** canonical to the current/stable version; `noindex` or canonical old versions deliberately so they don't duplicate or outrank current.
- **Code blocks:** real text in the served HTML (not images of code); language-tagged.
- **Anchor-linkable sections:** stable heading anchors so engines (and answers) can deep-link.
- **Freshness:** genuine `dateModified`; stale docs erode trust and citation.
- **Internationalised docs:** combine with `international.md`; avoid duplicate-content traps across locales.

## Common failures
- Docs rendered only client-side → invisible to AI crawlers that don't run JS (a double miss: docs are exactly what those crawlers want).
- Old versions competing with current for the same queries.
- Walls of text with no question/task headings — hard to extract an answer from.
- Code shown as images.

## Priority tilt
Weight **Reach** (is it even served?) then **Cite** and **Read** highest — docs are the strongest AEO asset most products have. Get them reachable, clear, and answer-shaped.
