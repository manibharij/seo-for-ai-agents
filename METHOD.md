# The Visibility Ladder

*A method for getting a website to rank in search, in the dependency order that actually matters, with AI-answer visibility as the layer on top.*

---

## Why most SEO advice fails

Open almost any "SEO checklist" and you get a flat list: add meta descriptions, write alt text, get backlinks, add schema, improve Core Web Vitals, and twenty more items in no particular order. It reads like a to-do list. It behaves like a slot machine.

The problem is not that the items are wrong. The problem is that they have a **dependency order**, and the checklist hides it. Adding a beautiful meta description to a page that Google cannot render is wasted work. Writing structured data for a page that never gets crawled is wasted work. Building internal links into a page that has no readable content is wasted work.

You cannot optimise what cannot be seen. And most sites built by AI coding agents fail at the very bottom of the stack — the page looks perfect in the browser, and is nearly invisible to a crawler — while everyone busies themselves at the top.

The Visibility Ladder fixes the order. It is **five rungs that climb to the goal of every site: ranking.** The first three are strict prerequisites — a page that can't be reached can't be read, and one that can't be read can't be understood — and the top two build on that foundation rather than gating it as rigidly. Either way, a broken lower rung quietly caps everything above it, so you diagnose from the top and fix from the bottom up. Then, above the ladder, sits one further layer for the AI-answer era.

### SEO is the goal; AI search is the layer on top

Be clear about the priority, because it's easy to get backwards. **The goal is to rank in search.** That is what the ladder is for, and the fifth rung names it: Rank. Everything below the summit exists to earn it.

**AEO** (answer-engine optimisation: being cited by AI answers like AI Overviews, ChatGPT and Perplexity) is real and growing, and it's worth doing. But it is **a layer on top of the ladder, not a rung in it, and not a replacement for ranking.** SEO and AEO share a foundation, a page must be reachable, readable, understandable, well-connected and genuinely good to do anything in either. They diverge at the top: classic ranking is largely earned by your own page, whereas whether an AI answer *cites* you depends on the model, what it retrieves, and your authority across the wider web, much of which sits outside your site. So citation is never guaranteed, comes *after* you've earned ranking, and is scoped here to the **owned-media** part you can actually control. SEO first; AEO on top.

---

## The five rungs

### 1. Reach — *can a machine get to your content at all?*

Before anything else: can a crawler fetch the URL, and does the response contain your actual content? This is where AI-built sites fail most often and most silently. A single-page app renders gorgeously for a human because the browser runs the JavaScript. A crawler that does not execute that JavaScript — or executes it on a delay, or budgets it away — sees an empty shell.

Reach is also robots rules that accidentally block the wrong paths, sitemaps that list dead or wrong URLs, redirect chains, and pages that return `200 OK` while serving nothing. If a page fails Reach, **nothing above it counts.** This rung is the foundation and the most common point of total failure.

### 2. Read — *once it is reached, is there real content to read — and is the page fast and usable?*

A reached page still has to contain genuine, readable substance: a real `<title>`, a meaningful `<h1>`, body copy that answers the page's implied question, descriptive metadata, and images with text alternatives. "Read" is not about keyword density — that thinking is two decades stale. It is about whether the rendered HTML carries enough clear, well-structured language for an engine to know what the page is *about*, and whether the content genuinely matches the intent of the person who arrived.

Read also covers **page experience** — mobile-friendliness (Google indexes mobile-first) and Core Web Vitals (loading, responsiveness, visual stability). These aren't strict dependencies the way the rungs are — a slow page still gets read and indexed, just ranked lower — but they're real ranking signals and genuine build-time fixes, so they belong here rather than in a separate flat checklist.

A page can pass Reach (the HTML is served) and still fail Read (the served HTML is thin, duplicated, sluggish, or unusable on a phone). Fix that here, before you try to be clever.

### 3. Understand — *can the engine identify the entities on the page?*

Humans read a page and infer: this is a product, that is its price, this is a recipe, that is the author, this is a business with these opening hours. Engines need help making the same inferences reliably. Structured data — schema.org, expressed as JSON-LD — is how you state those facts in a machine-legible form.

Understand sits above Read for a reason: structured data **describes** content that must already exist and already be readable. Marking up a price that is not on the page, or an author who is not real, is at best ignored and at worst a trust violation. Schema annotates the truth; it does not manufacture it.

### 4. Connect — *is the page wired into a coherent site?*

A page is not an island. Engines learn importance and meaning from how pages link to one another: a sensible internal link graph, a clear hierarchy, descriptive anchor text, correct canonical tags so duplicates consolidate rather than compete, and a structure that signals which pages are the authorities on which topics.

Connect comes after Understand because internal linking is most powerful when the engine already knows what each page is and what entities it covers. Wire understood pages together and the whole site reinforces itself.

### 5. Rank — *is the page good enough, and trusted enough, to win?*

The summit, and the whole point. The first four rungs make a page *eligible* to rank: reachable, readable, understood, and well-connected. Rung five is whether it actually *deserves* to win the query. And here is the honest part most checklists hide: unlike the rungs below it, ranking is not a property you switch on. It is an **outcome you earn**, decided partly on your own page and partly out in the wider world. So rung five has two halves, and they are not the same kind of work.

**What you build — owned media, the agent's job.** Everything on your own page and site that earns ranking, taken as far as it can go:

- **Search intent** — does the page actually answer the query a visitor came for (informational, commercial, transactional, navigational), in their language, and in the format the results page rewards?
- **Genuine quality and depth** — is it comprehensive, specific, and more useful than what already ranks, adding something new rather than echoing it?
- **On-page E-E-A-T** — real experience, expertise, authorship and sources, *surfaced honestly* where they genuinely exist, never invented.
- **Topical authority** — does the site cover the topic deeply enough (the hub-and-spoke clusters from Connect) to read as a credible source on it? This is where Connect and Rank reinforce each other rather than strictly stack.

**What you earn — off-site, the agent only advises.** Ranking is also decided by authority you cannot code: backlinks, brand and reputation, and the sheer strength of the competition. This is earned over time through real work and trust, not built at deploy. It sits *beside* the ladder, not on it — the pack's **`seo-offsite-authority`** skill audits and strategises it (white-hat only), but the earning itself stays off-site, ongoing work. It is a major ranking factor, so it earns a place at the summit; it is simply not something a build can do for you.

Rung five is the goal of the ladder: build everything on the left as far as it will go, and advise honestly on the right.

### Above the ladder: AEO (being cited by AI answers)

Once a page can genuinely rank, the same foundations make it *eligible* to be cited by AI answer engines, AI Overviews, ChatGPT, Perplexity, Claude. This is **a layer on top of the ladder, not a sixth rung**, because it is not a prerequisite for ranking and it never substitutes for it. It is applied to a page whose fundamentals are already in place — alongside ranking, never before it, and never instead of it.

AEO is a formatting and trust discipline: self-contained answer blocks that make sense lifted out of context, question-shaped headings, consistent entity naming, genuine attribution, and an awareness of how AI crawlers differ from classic ones. It makes a page **eligible** to be quoted; it cannot guarantee a citation, because that depends on much that sits outside your site — including, increasingly, whether you already rank for the query. Worth doing, on a page whose ranking fundamentals are sound, never as a shortcut around them.

---

## The one rule

> **Diagnose top-to-bottom. Fix bottom-to-top.**

Walk the ladder downward to find the lowest rung that fails. Then fix upward from there, and re-verify each rung before climbing. The lowest broken rung is almost always the one quietly capping everything above it.

A site can have immaculate schema and a tidy link graph and still be invisible, because rung one is broken and no one looked. Start at the bottom.

---

## Run it as a lifecycle, not a one-shot

A real site is never "done." Content ships, templates get refactored, platforms get upgraded — and fixes silently revert. So the ladder isn't a checklist you run once; it's an **audit you re-run**, and it should *remember*.

- **Baseline.** The first pass takes the site's vitals across all five rungs, records where it stands, and fixes the safe wins.
- **Progress.** Each later pass reads what happened before, re-verifies that past fixes still hold on the served output (**catching regressions** — the fix that quietly broke in a deploy), finds what's new, and advances the backlog by priority.
- **Maintain.** Over time this keeps a site healthy rather than letting it drift.

This is what makes the method serve an *existing* site as well as a new one. A freshly built site needs the baseline; an established site needs the ongoing audit — the same ladder, run with memory. (In this pack, that memory is a `.seo/` folder written into the project: a readable report, a machine-readable issue tracker, and a dated history.)

---

## Four principles that keep the method honest

**Work it out yourself; don't interrogate the user.** The person running this should not have to know SEO, describe their site, or fill in a questionnaire. Before doing anything, the agent **reads the codebase and the served pages and works out the context on its own**: what the site is, who it's for, what each page is trying to do, the stack, the platform, and the sector. It forms a working model, acts on sensible defaults, and only pauses for the handful of decisions a human genuinely must make, and even then it proposes a default rather than blocking. Inferring beats asking. A good audit should feel like handing the keys to an expert who looks around and gets to work, not one who hands you a form.

**Verify on the rendered output, not the source.** An agent that edits some JSX and announces "meta tags added" has proven nothing — it has changed the *source*. What matters is what is actually *served* to a crawler. Every rung in this pack is verified by inspecting fetched, rendered HTML, not by trusting that the code change had the intended effect. Client-rendered content that is invisible to crawlers is the single most common failure of AI-built sites, and the only way to catch it is to look at what comes down the wire.

**Never fabricate trust.** Authors, credentials, reviews, experience, expertise — these are either real or they are a liability. Where a genuine trust signal is missing, the right move is to flag it as a human decision, never to invent it. White-hat is not a constraint on the method; it is part of what makes the method work, because answer engines are increasingly built to detect and discount manufactured authority.

**On an existing site, first do no harm.** A new site has nothing to lose; an established one has rankings, traffic, and *intentional* past decisions. A `noindex`, a canonical, a redirect, a blocked path that looks "wrong" may be load-bearing. So on a live site the method is conservative: understand what's working and what's deliberate before changing it, never break a URL that has value without a `301` to its closest equivalent, prefer additive and reversible fixes, and put the big, risky changes in front of a human before applying them. Improving a site is not licence to regress what already earns its place.

---

## The boundary: what a build can and cannot fix

This method, and the skills built on it, fix **build-time** problems on your **owned media** — the structural, code-level decisions baked into how *your own site* is rendered, written, marked up, linked and formatted. Those are fixable once, correctly, by an agent that knows what to look for.

Two things sit outside that line, honestly:

**Earned media — the off-site half of SEO.** Backlinks, digital PR, brand mentions and third-party reviews build off-site authority that genuinely affects ranking. It has a named place at the summit (rung five's *what you earn*), but the ladder can't *build* it, because authority is **earned** through outreach and reputation over time, not written into your code, and faking it (bought links, fake reviews) is the black-hat behaviour this method refuses. But it is half of SEO, so the pack includes an **off-site authority skill (`seo-offsite-authority`), beside the ladder**, that *audits* your backlink profile (toxic links, a disavow file, the competitor gap) and *strategises* white-hat link-building and digital PR. It advises and audits; it never executes outreach or buys links. The earning itself stays off-site, ongoing work, yours or a managed service's.

**Live measurement.** A build, by itself, can't tell you what's happening out in the live world: whether you actually rank, where, against whom, or whether AI engines are citing you over time. That's **live data** — rank tracking, AI-citation monitoring, real-user Core Web Vitals, geo-grid visibility. The method treats it as **optional enrichment, never a requirement**: connect your own data tools (Search Console, DataForSEO, Ahrefs) with your own keys and the audit gets sharper — real indexation, traffic-weighted priorities, real demand. Don't want to wire that up, or want it managed and ongoing? That's the done-for-you tier. Either way, the free build-time work never depends on it, and current data is never a guarantee of future results.

The ladder gets your site built right; live data tells you how it's doing. Earning off-site authority remains its own discipline. None of it is paywalled at the build-time layer — that's the honest line.
