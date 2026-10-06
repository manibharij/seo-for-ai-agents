# Judging content quality, intent, and E-E-A-T

Read this to assess a page's content honestly. You are judging what's **actually on the served page**, against what a reader who arrived for that topic genuinely needs. No fabrication — you assess and recommend; you never invent quality, sources, or expertise that isn't there.

---

## Quality & depth

The test isn't word count or keyword presence — it's: **does this page comprehensively, specifically, and accurately serve its topic better than a generic page would?**

Signs of strong content:
- Specific, concrete, correct information — not generic statements that could describe any competitor.
- Genuinely answers the questions a reader on this topic has (and the obvious follow-ups).
- Original substance: real experience, real data, real examples — not a rehash of the top results.
- Clear structure that makes the substance easy to extract (ties to the Cite rung).

Signs of weak content (flag for improve/consolidate/prune):
- Thin: a few generic sentences, padding, or filler around a thin core.
- Derivative: nothing the top 10 results don't already say better.
- Mismatched: promises one thing (title/intent), delivers another.
- Outdated: stale facts on a topic where currency matters.

> You can judge and recommend, and you can *restructure/tighten real content* (via `seo-content-editing`). You **cannot** manufacture the missing substance — a page that's thin because the business has nothing specific to say needs human input (a content brief), not invented filler.

---

## Search-intent match

Every query has an intent; every page should serve one. Classify the dominant intent the page targets and check the content matches:

- **Informational** ("what is X", "how to Y") → teach clearly; depth and accuracy matter.
- **Commercial investigation** ("best X", "X vs Y", "X review") → honest comparison, criteria, evidence.
- **Transactional** ("buy X", "X pricing", "X near me") → make the action/answer immediate and clear.
- **Navigational** (brand/product names) → get them where they're going.

Mismatch is one of the most common and damaging content failures: a blog post ranking for a buying query, or a thin product page for an informational one. With a keyword tool connected, confirm the intent from the actual SERP; without, infer from the query language and the page's purpose — and say which you did.

---

## E-E-A-T (Experience, Expertise, Authoritativeness, Trust)

Assess the **genuine** trust signals present (and flag what's missing — never invent it):
- **Experience/Expertise:** is the content evidently written by someone who knows the subject (named author, real credentials, first-hand detail)? Or anonymous and surface-level?
- **Authoritativeness:** real citations/sources, accurate claims, evidence the page/author is a credible source.
- **Trust:** transparency (real about/contact/author info), accuracy, no misleading claims.

For YMYL topics (health, finance, legal — "your money or your life"), the E-E-A-T bar is higher; weak or anonymous content here is a serious flag. The recommendation when E-E-A-T is missing is always a **human task** ("attribute this to a real, credentialled author; add real sources"), never a fabricated byline or citation.

---

## Using live data here (when connected)
Detect what exists before using it (a tool, then an API with the user's credentials, then an export), as set out in `seo-orchestrator/references/live-data-integrations.md`. The pulls are defined in `decay-cannibalisation-actions.md`; the API recipes are in `seo-orchestrator/references/data/`.
- **Search Console:** which pages get impressions/clicks, at what position, and which are **declining** (decay). Strong signal for keep vs refresh vs improve. A page with impressions but low clicks/position is an improve/intent opportunity; a page with falling clicks is a refresh candidate.
- **Keyword tool:** real demand and SERP/competitor context — does the topic warrant the effort, and what does winning content look like.
- **Analytics or CRM** (`data/analytics-ga4.md`): key events or leads by landing page. A page that converts has a business purpose even with few clicks.

Without these, assess on content signals and **state the limitation** in the verdict ("no performance data connected; judged on content quality and intent match"). Don't present an inference as if it were measured.

---

## The verdict rubric

Give each judged page one verdict. Read the served page, not the CMS draft, and decide with these questions.

| Verdict | All of these hold |
|---|---|
| **strong** | Answers the main question and the obvious follow-ups; contains specifics a generic page would not (numbers, steps, first-hand detail, real examples); intent matches; claims are current and sourced where it matters |
| **adequate** | Answers the main question correctly but generically, or misses obvious follow-ups; intent matches; nothing is wrong or stale |
| **weak** | Any of: thin or padded, intent mismatch, outdated facts on a time-sensitive topic, says nothing the top results do not say better, or a YMYL page with no real author or sources |

Write the reason into the CSV's `evidence` column in one checkable line: "answers 'how to bleed a radiator' but no steps for combi systems; no images; last updated 2021".

### Measurable signals that support the verdict
These help you find pages to read. None decides a verdict alone.
- **Main-content word count** (`page_facts.py`): compare within a template. A post far below its template's median is worth reading first. Short is not weak if the question is short.
- **Duplicate title or h1** across URLs: a lead for cannibalisation, not proof (see `title_overlap.py`).
- **Visible date** older than the facts it relies on, on a time-sensitive topic.
- **Missing author or sources** on a YMYL topic: a flag for a human task.
- **Impressions with few clicks** (Search Console): the page is shown but not chosen. Check whether the title and opening match the query's intent.

### Checking intent
- **With a keyword tool or SERP data:** look at what ranks for the page's main query. If the top results are product pages and yours is an essay (or the reverse), the intent is mismatched whatever the quality.
- **Without:** infer from the query wording ("buy", "best", "how to", a brand name) and the page's purpose, and set `basis` to `content`.
- **With Search Console only:** the queries a page actually gets impressions for tell you the intent Google associates with it. If those queries differ from what the page sets out to answer, note both.

### Sampling note
On sites over 1,000 pages you judge a stratified sample (see `decay-cannibalisation-actions.md`). Read at least the sampled pages in full. Never apply a `weak` verdict to an unread page in a way that leads to prune or consolidate: those always need the page read.

---

## The output per page
For each page: a short **quality verdict** (strong / adequate / weak, with the why), the **intent** it targets and whether it matches, the **E-E-A-T** state (and any missing real signals to flag), freshness, and the **basis** (live-data-backed or content-signal inference). These fill the `verdict`, `intent`, `basis` and `evidence` columns of the inventory CSV and feed the decision rules in `decay-cannibalisation-actions.md`.
