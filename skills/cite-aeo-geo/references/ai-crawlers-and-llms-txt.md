# AI crawlers and llms.txt

Read this to understand how AI crawlers differ from classic search crawlers, how to control their access deliberately, and what `llms.txt` actually is (and isn't). Two practical truths drive everything here: many AI crawlers **render little or no JavaScript**, and whether to **allow or block** them is a **business decision** you present, not one you make for the user.

---

## How AI crawlers differ from classic crawlers

- **Often no JavaScript execution.** Classic Googlebot has a (deferred, imperfect) rendering pass; many AI crawlers fetch raw HTML and little else. **Consequence:** the served-HTML discipline from the Reach rung is *even more* important for AI citation. Content, answer blocks, and schema that only appear after client-side JS may be invisible to the very engines you want citing you.
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

### Implementation pattern (illustrative — confirm current user-agent tokens)
```
# Allow a search/citation crawler
User-agent: Googlebot
Allow: /

# Example: allow an answer-engine's retrieval bot but block its training bot
# (verify the exact, current user-agent strings before relying on them — they change)
User-agent: <answer-engine-retrieval-bot>
Allow: /

User-agent: <answer-engine-training-bot>
Disallow: /
```

> The specific user-agent tokens for AI crawlers change and new ones appear regularly. **Verify the current strings** (from each provider's official docs) before writing rules, and tell the user these need occasional review. Don't hard-code a list as if it's permanent.

Caveats to tell the user honestly:
- `robots.txt` is **honoured voluntarily.** Reputable crawlers obey it; it is not technical enforcement. Truly protecting content requires auth/paywalls, not robots rules.
- Blocking a crawler means **no citations** from that engine — that's the trade-off of blocking.
- Don't accidentally block search crawlers while trying to block training ones — that would cost you classic *and* AI search visibility. Double-check.

---

## llms.txt — what it is, and what it isn't

`llms.txt` is a **proposed** convention: a Markdown file at your site root (`/llms.txt`) that offers LLMs a curated, clean map of your most important content — links to key pages, sometimes with summaries, so a model can find the good stuff without wading through navigation and boilerplate. Think of it as a "table of contents for LLMs", analogous in spirit to a sitemap but human-readable and curated.

### Be honest about its status
- It is a **community proposal, not an established standard**, and **adoption by major AI engines is limited/unconfirmed** as of 2026. Major providers have not broadly committed to consuming it.
- So treat it as **low-cost, low-certainty**: cheap to add, possibly helpful as adoption grows, but **not** a substitute for the real work (reachable, well-formatted, trustworthy pages). Don't oversell it to the user.

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
