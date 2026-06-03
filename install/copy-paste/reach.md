# Reach — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the Reach skill. No setup, no references — paste it into Claude Code, Cursor, ChatGPT, Copilot Chat, or any coding agent and ask it to run through the steps on your site.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** Review every change on the *served* output and test before you publish. See the repo's `DISCLAIMER.md`.

---

You are fixing whether search engines and AI crawlers can **reach** my pages and see their content. This is the foundation of SEO: if a crawler can't reach a page and read its content in the served HTML, nothing else about SEO matters. Work in four steps and **stop to explain before any big change**.

**The one rule: verify on what is actually SERVED, not on the source code.** Editing code and saying "done" proves nothing. You must fetch the URL and confirm the content is really there. Assume my content is invisible to crawlers until you've proven otherwise by fetching it.

## Step 1 — Diagnose
1. **Find my framework** (look for `next.config`, `vite.config`, `astro.config`, `nuxt.config`, etc.). If you can't tell, ask me — don't guess.
2. **Fetch a real content page** (an article or product page, not just the homepage) and look at the **raw HTML before any JavaScript runs** (e.g. `curl -sL <url>`). Search it for a distinctive sentence of my actual body text, my real `<h1>`, and my `<title>`.
   - Content present in the raw HTML → rendering is fine.
   - Content missing from raw HTML but visible in the browser → **this is the problem**: my site is client-rendered and crawlers see an empty shell. This is the #1 reason AI-built sites don't show up.
3. **Check the gatekeepers:** does the page return `200`? Is it served over **HTTPS** with `http://` redirecting to `https://` (and no mixed-content `http://` assets)? Any stray `noindex` in the HTML `<head>` or the `X-Robots-Tag` header? Does `robots.txt` accidentally block real content? Is there a sitemap with correct production URLs?

## Step 2 — Fix (lowest problem first)
- **Make the content part of the server's HTML response, before JavaScript runs.**
  - **Next.js App Router:** fetch data in server components; push `"use client"` down to small interactive parts only — never on a whole page/layout.
  - **Next.js Pages Router:** use `getServerSideProps` / `getStaticProps` instead of fetching in `useEffect`.
  - **Vite / Create React App (pure SPA):** this serves an empty shell. The real fix is server-side rendering or pre-rendering — a significant change. **Stop and give me the options (migrate to Next/Astro/Remix, add SSR via `vike`, or pre-render routes) with trade-offs. Don't re-architect silently.**
  - **Astro / Nuxt / SvelteKit / Remix:** these render server-side by default; find the component/route that opted into client-only rendering and move its data fetching to the server.
- **Fix gatekeepers:** remove accidental `Disallow`/`noindex` on pages that should be indexed (check with me first), ensure a sitemap of canonical `200` URLs referenced from `robots.txt`, return real `404`s for missing pages, and collapse redirect chains.
- **Never** cloak, hide text for bots, or serve crawlers different content than users. The content a crawler sees must be the content I see.

## Step 3 — Verify (re-fetch — don't trust the edit)
Re-fetch the page and confirm: the previously-missing content is now in the **raw HTML**; status is `200`; no stray `noindex` in body or headers; `robots.txt` allows it; sitemap lists the correct URL. **If it's not in the served HTML, you're not done — go back to Step 1.**

## Step 4 — Explain it to me in plain English
I don't know SEO. Tell me:
1. **What was wrong** (in plain words — e.g. "crawlers were seeing empty pages because…").
2. **What you changed and why it matters** for being found.
3. **Proof** — show me the content now appearing in the raw HTML.
4. **What only I can decide** — architecture changes, which paths should be private, etc.

Note honestly: this fixes whether my site *can be found and read*. It can't tell me whether I actually *rank*, where, or against whom — that needs live ranking data, which is a separate thing.

Then tell me the next step is **Read** (making sure each page has real, readable content, correct metadata, and a fast, mobile-friendly page experience).
