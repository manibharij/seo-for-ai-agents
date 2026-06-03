---
name: seo-measurement-setup
description: >-
  Set up the build-time PLUMBING for measuring SEO — install analytics (GA4)
  correctly, verify the site in Google Search Console, ensure the sitemap is
  submittable, and add structured-data/Core-Web-Vitals measurement hooks. Use on
  "set up analytics", "install GA4", "verify Search Console", "add tracking", "is my
  analytics working", or "how do I measure SEO" tasks. This wires up measurement so
  you CAN see results — it does not analyse them (that's live data, on the other side
  of the boundary). Verifies tags fire correctly on the served output.
---

# Measurement Setup — wire up the instruments (don't read them)

A specialist skill that installs the **plumbing** so a site's SEO can be measured: analytics that actually fire, Search Console verified, the sitemap submittable, and the hooks for ongoing monitoring. It deliberately stops at *setup* — **reading and acting on the data is live-data analysis**, the separate ongoing discipline beyond build-time fixes. This skill makes measurement *possible*; it doesn't pretend the build can tell you how you're performing.

> Why it's in the pack: an audit's value compounds when you can see the effect of fixes over time — but only if the instruments are installed correctly. Broken or missing analytics (a duplicate GA4 tag, an unverified property, no submitted sitemap) is extremely common, especially on AI-built and hastily-relaunched sites.

Work the four steps: **Diagnose → Fix → Verify (on served output) → Report (+ boundary).**

---

## Step 1 — Diagnose

On the **served output** and config:
- **Analytics present and correct?** Is a GA4 (or chosen analytics) tag in the served HTML, firing once (not duplicated), and not blocked by a missing consent path? Watch for: no analytics at all, two copies (double-counting), a tag added client-side that never loads, or a leftover Universal Analytics tag (GA4's predecessor, now defunct).
- **Search Console verifiable/verified?** Is there a verification token (meta tag, DNS record, or HTML file) for Google Search Console? (Verification + submission are live steps the user completes — you prepare the plumbing.)
- **Sitemap submittable?** Does a valid sitemap exist at a stable URL, referenced in `robots.txt`, ready to submit? (Reach owns sitemap correctness; here, ensure it's measurement-ready.)
- **Core Web Vitals measurement?** Is there any field-data path (the user's GA4/CrUX) — note that real-user CWV is live data; the build can add a `web-vitals` reporting hook but can't produce the field score.
- **Consent / privacy** present where required (cookie/consent for analytics in applicable regions)? Flag if missing — it's a legal/UX matter for the user.

---

## Step 2 — Fix (install the plumbing correctly)

- **GA4** — install once, correctly. **Next.js:** use `@next/third-parties` (`GoogleAnalytics`) or `next/script` with `strategy="afterInteractive"`; place it once in the root layout so it loads on every route and isn't duplicated. Remove any duplicate/legacy tags. See `references/analytics-and-search-console.md`.
- **Search Console verification** — add the verification meta tag (Next.js: via the Metadata API `verification.google`) or the HTML-file/DNS method the user prefers. Then the **user** completes verification in GSC (their account — a live step).
- **Sitemap for submission** — confirm a valid sitemap URL and `robots.txt` reference; the user submits it in GSC (live step).
- **Core Web Vitals reporting (optional)** — wire a `web-vitals` hook (Next.js: `useReportWebVitals`) to send field metrics to analytics, so real-user CWV becomes visible *to the user over time*.
- **Respect privacy** — don't add tracking that bypasses a required consent mechanism; if consent isn't handled, flag it as a human/legal task rather than installing tracking that may be non-compliant.

> Don't double-install. The most common failure is two analytics tags double-counting — check before adding.

---

## Step 3 — Verify (on the served output)

- **Tag present once:** fetch the served HTML and confirm exactly one analytics snippet; confirm the GA4 Measurement ID is the right one.
- **It fires:** if a render/network MCP or browser is available, confirm the analytics request actually sends on page load (network call to the analytics endpoint) and isn't duplicated. Otherwise confirm the snippet is correctly placed and not obviously blocked.
- **Verification token present** in the served HTML/headers (or DNS/file in place).
- **Sitemap** reachable and referenced in `robots.txt`.
- Confirm no legacy/duplicate tags remain.

**If the tag isn't in the served output or fires twice, it isn't done.**

---

## Step 4 — Report (plain English) + the boundary

1. **What was wrong** — e.g. "You had two analytics tags double-counting every visit, and the site wasn't verified in Search Console, so you had no real indexing data."
2. **What I set up** — analytics installed once and firing, GSC verification in place, sitemap ready to submit, CWV reporting wired.
3. **Proof** — the single tag in the served output (and the network call firing, if checked).
4. **What only you can do (live steps):** complete Search Console verification and submit the sitemap in your GSC account; connect and review the analytics dashboards.
5. **The boundary (state it plainly):** this skill installed the *instruments*. **Reading them — whether you rank, where, traffic trends, which pages get cited — is live-data analysis, the separate ongoing discipline beyond build-time fixes.** Setup ≠ insight. Point the user to where that live measurement/monitoring lives.

---

## Reference files
- `references/analytics-and-search-console.md` — GA4 install patterns (Next.js and generic), GSC verification methods, web-vitals reporting, the common double-tag/legacy-tag failures, and exact verification steps.
