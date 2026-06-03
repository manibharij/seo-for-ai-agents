# Measurement Setup — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the measurement-setup skill. Wires up the instruments (analytics, Search Console, sitemap submission, web-vitals) so SEO CAN be measured. It does not analyse the data — that's live-data work.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** Confirm the tag fires once on the *served* output before trusting it. See the repo's `DISCLAIMER.md`.

---

You are setting up the **build-time plumbing** so my SEO can be measured — not analysing results (that's separate, live-data work). Work in four steps and **verify on the served output**.

## Step 1 — Diagnose
- **Analytics:** is a GA4 tag (`G-XXXXXXX`) in the served HTML, firing **once** (not duplicated)? Any leftover **Universal Analytics** (defunct) or a second tag double-counting? Any analytics added client-side that never loads?
- **Search Console:** is there a verification token (meta tag / DNS / HTML file)?
- **Sitemap:** valid, at a stable URL, referenced in `robots.txt`, ready to submit?
- **Consent:** is analytics gated behind a required cookie/consent mechanism where applicable?

## Step 2 — Fix (install correctly, once)
- **GA4 — once, site-wide.** Next.js: `@next/third-parties` `GoogleAnalytics`, or `next/script` with `strategy="afterInteractive"` in the root layout. Remove duplicates and any legacy UA tag.
- **Search Console:** add the verification meta tag (Next.js: Metadata API `verification.google`) or HTML-file/DNS method. I then complete verification in my GSC account (my live step).
- **Sitemap:** confirm it's reachable and referenced in `robots.txt`, ready for me to submit in GSC.
- **Core Web Vitals (optional):** wire a `web-vitals` reporting hook (Next.js: `useReportWebVitals`) to send real-user LCP/INP/CLS to analytics.
- **Don't** add tracking that bypasses a required consent mechanism — flag consent gaps to me instead.

## Step 3 — Verify (served output)
Confirm exactly **one** GA4 snippet with the correct `G-` ID (no duplicates, no UA); if you can check the network, confirm the analytics request fires once on load; confirm the GSC verification token is present and the sitemap is reachable. **If the tag is missing or fires twice, it's not done.**

## Step 4 — Report + boundary
Tell me what was wrong (e.g. "two tags double-counting; site unverified in Search Console"), what you set up (with served-output proof), and my **live steps** (verify + submit sitemap in GSC; review the dashboards). **Boundary, stated plainly:** you installed the *instruments* — **reading them (do I rank, where, traffic trends, AI citations) is live-data analysis, the separate ongoing discipline, not the build.**
