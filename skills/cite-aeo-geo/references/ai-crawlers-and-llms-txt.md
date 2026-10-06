# AI crawlers and llms.txt

Read this to understand how AI crawlers differ from classic search crawlers, how to control their access deliberately, and what `llms.txt` actually is (and isn't). Two practical truths drive everything here: many AI crawlers **render little or no JavaScript**, and whether to **allow or block** them is a **business decision** you present, not one you make for the user.

---

## How AI crawlers differ from classic crawlers

- **Often no JavaScript execution.** Classic Googlebot has a (deferred, imperfect) rendering pass; many AI crawlers fetch raw HTML and little else. **Consequence:** the served-HTML discipline from the Reach rung is *even more* important for AI citation. Content, answers and schema that only appear after client-side JS may be invisible to the very engines you want citing you.
- **Different purposes, different bots.** Roughly three categories, and a site can treat them differently:
  1. **Search-index crawlers** that feed AI search features (e.g. Google's, which also powers AI Overviews).
  2. **AI "answer" / retrieval crawlers** that fetch pages to answer user queries in real time and cite them (various assistant engines).
  3. **AI training crawlers** that collect data to train models (no citation benefit to you).
- **Citation vs training trade-off.** Allowing retrieval/search crawlers can earn you citations and referral traffic; allowing training crawlers gives no direct visibility benefit. Some sites allow the former and block the latter. This is exactly the kind of choice to surface to the user.

---

## Controlling AI crawler access — present the choice, don't decide it

Access is controlled in `robots.txt` by user-agent. The decision is the user's; your job is to make it informed and then implement it.

### The shape of the decision
- **Allow citation/search crawlers** if the user wants visibility in AI answers (usually yes for marketing/content sites).
- **Block training crawlers** if the user doesn't want their content used for model training with no return (a common stance).
- **Block everything** only if the user genuinely wants to stay out of AI surfaces (rare for sites doing SEO, but legitimate — e.g. paywalled/proprietary content).

### The main AI crawler tokens (verified 2026-10)

Each row was checked against the operator's own documentation. Tokens change and new ones appear, so re-check the linked page before writing rules and tell the user the list needs occasional review.

| Robots token | Operator | Purpose (operator's description) | Honours robots.txt? |
|---|---|---|---|
| `GPTBot` | OpenAI | Crawls content that may be used to train its foundation models | Yes |
| `OAI-SearchBot` | OpenAI | Surfaces websites in ChatGPT's search features | Yes |
| `ChatGPT-User` | OpenAI | Fetches pages for user actions in ChatGPT and Custom GPTs | OpenAI says robots.txt rules may not apply, as the fetch is user-initiated |
| `ClaudeBot` | Anthropic | Collects web content that could contribute to model training | Yes (also supports `Crawl-delay`) |
| `Claude-SearchBot` | Anthropic | Crawls to improve search result quality for users | Yes |
| `Claude-User` | Anthropic | Fetches pages when a Claude user asks a question | Yes, per Anthropic |
| `PerplexityBot` | Perplexity | Surfaces and links websites in Perplexity search results | Yes |
| `Perplexity-User` | Perplexity | Fetches pages to answer a user's question | Perplexity says it generally ignores robots.txt |
| `Google-Extended` | Google | Control token only, with no crawler of its own. Governs use of Google-crawled content for training Gemini models and for grounding in Gemini Apps and Vertex AI | Control token. Google says it does not affect inclusion or ranking in Google Search, and it does not control AI Overviews or AI Mode (see snippet controls below) |
| `Applebot-Extended` | Apple | Control token only: it does not crawl. Decides whether content Applebot crawled may train Apple's foundation models | Control token. Pages that disallow it can still appear in Apple's search results |
| `CCBot` | Common Crawl | Builds Common Crawl's open web crawl archive | Yes |

Sources: [OpenAI](https://developers.openai.com/api/docs/bots), [Anthropic](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler), [Perplexity](https://docs.perplexity.ai/docs/resources/perplexity-crawlers), [Google common crawlers](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers), [Apple](https://support.apple.com/en-us/119829), [Common Crawl](https://commoncrawl.org/ccbot). Each operator also publishes IP ranges for verification; they are listed in the Reach skill's `references/edge-cdn-and-bot-access.md`.

The user-triggered fetchers (`ChatGPT-User`, `Perplexity-User`) are how assistants read a page live when someone asks about it. Their operators say robots.txt may not stop them, so a robots rule is a weak lever there. Blocking them also costs visibility in those assistants.

### Implementation pattern
A common stance: keep classic search and AI search open, and opt out of training. It is only an example; the choice is the user's.
```
# Classic search: keep open
User-agent: Googlebot
User-agent: Bingbot
Allow: /

# AI search and citation crawlers
User-agent: OAI-SearchBot
User-agent: Claude-SearchBot
User-agent: PerplexityBot
Allow: /

# AI training (the user's choice)
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: CCBot
Disallow: /
```
A crawler follows only the most specific group that names it and ignores the `User-agent: *` group ([Google's robots.txt spec](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec)). If you add a named group, repeat in it any `Disallow` rules from `*` that should still apply to that crawler (admin, cart, internal search).

Caveats to tell the user honestly:
- `robots.txt` is **honoured voluntarily.** Reputable crawlers obey it; it is not technical enforcement. Truly protecting content requires auth/paywalls, not robots rules.
- Blocking a crawler means **no citations** from that engine — that's the trade-off of blocking.
- Don't accidentally block search crawlers while trying to block training ones — that would cost you classic *and* AI search visibility. Double-check.

### The WAF and CDN layer decides first
`robots.txt` states a preference; a WAF, CDN or host enforces one, and it acts before the crawler reads anything. The two layers must agree:
- **An allow in robots.txt does nothing if the edge blocks the crawler.** Cloudflare's AI bot policies can block Search, Agent or Training traffic, and count mixed-purpose crawlers as Training wherever Training is blocked. AWS WAF Bot Control's `CategoryAI` rule blocks AI bots even when they are verified. Vercel and Netlify have AI-bot rulesets and UA blockers. Any of these can silently undo a "let AI search crawlers in" decision.
- **The edge is the only real enforcement** for fetchers that may ignore robots.txt (`ChatGPT-User`, `Perplexity-User`). If the user wants them out, that is a WAF rule, with the visibility cost stated.
- **Cloudflare can rewrite robots.txt.** Its managed `robots.txt` prepends AI-crawler rules to the origin's file, so read the live file, not the repo copy.

Check both layers with the bot-UA comparison and IP verification in the Reach skill's `references/edge-cdn-and-bot-access.md`, which also lists what to change in each dashboard.

---

## Snippet controls: Google's levers for AI Overviews and AI Mode

Blocking `Google-Extended` does not keep a page out of AI Overviews or AI Mode. Google states that robots.txt rules for Googlebot control crawling for Search, AI features included, and that the way to limit what is shown is the snippet controls ([AI features and your website](https://developers.google.com/search/docs/appearance/ai-features), verified 2026-10). Per Google's [robots meta tag specification](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag):
- **`nosnippet`** (meta robots or `X-Robots-Tag`) shows no text snippet in any Google result, AI Overviews and AI Mode included, and stops the content being used as a direct input for them.
- **`max-snippet:[number]`** caps the snippet length and limits how much content may be used as a direct input for AI Overviews and AI Mode.
- **`data-nosnippet`** on a `span`, `div` or `section` keeps that part of the page out of snippets.

Google also requires a page to be indexed and eligible for a snippet to appear as a supporting link in AI features. So these controls cut both ways: they reduce how your content is used, and they reduce the chance of being cited. Present the trade-off; never add them by default.

**Search Console site-level control.** Under **Settings > Search generative AI**, a property can include its content in AI Overviews, AI Mode and generative AI features in Discover (the default), exclude it, or inherit its parent property's setting. Google rolled it out to all sites on 31 August 2026, says it is not a ranking or inclusion signal for the rest of Search, and says exclusion generally takes a few days ([Search Console Help](https://support.google.com/webmasters/answer/16908024), verified 2026-10). It is a dashboard setting, so give it to the user as an instruction and a business decision.

---

## llms.txt — what it is, and what it isn't

`llms.txt` is a **proposed** convention: a Markdown file at your site root (`/llms.txt`) that offers LLMs a curated, clean map of your most important content — links to key pages, sometimes with summaries, so a model can find the good stuff without wading through navigation and boilerplate. Think of it as a "table of contents for LLMs", analogous in spirit to a sitemap but human-readable and curated.

### Be honest about its status
- It is a **community proposal, not an established standard**. As of mid-2026, **Google has stated plainly that `llms.txt` has no effect on Search rankings or AI Overviews** (its guidance says Search doesn't use it), and adoption across top sites remains low.
- It **is** retrieved by some AI tools: Perplexity and Claude fetch it, and several coding agents (Claude Code, Cursor, Copilot and others) look for `/llms.txt` when pointed at a documentation site — so it's most defensible for **docs**.
- So treat it as **low-cost, low-certainty**: cheap to add, useful to the tools that read it, but **not** an SEO lever and **not** a substitute for the real work (reachable, well-formatted, trustworthy pages). Don't oversell it to the user.

### If you add one
Keep it a genuine, curated index of real, important pages with honest short descriptions:
```markdown
# Brand Name

> One-line description of what the site/company is.

## Core pages
- [What we do](https://example.com/services): concise, honest summary.
- [Pricing](https://example.com/pricing): how pricing works.

## Key guides
- [Guide title](https://example.com/guide): what it covers.
```
Tell the user plainly: "I've added an `llms.txt` pointing AI tools to your key pages. Support for it is still emerging, so treat it as a small bet, not a guarantee — the formatting and trust work is what actually drives citation."

---

## How this ties back to the ladder
AI-crawler reachability is **Reach, revisited for AI**: if AI crawlers can't fetch your served HTML (or you've blocked them), none of the Cite formatting matters. Confirm access and served-HTML visibility first, then format and attribute. And remember the boundary: even with all of this right, *whether you're actually cited* is live data you can't measure at build time — that's the product handoff in the SKILL.
