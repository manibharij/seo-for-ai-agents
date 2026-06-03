# Migrations & Redirects — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the migrations skill. Use whenever URLs change — redesign, replatform, domain move, slug changes, or 404s after a relaunch.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** This touches live rankings: review the redirect map and test every redirect on the *served* output before publishing. See the repo's `DISCLAIMER.md`.

---

You are preserving my search rankings while my URLs change (redesign / replatform / domain move / slug changes / post-relaunch 404s). **The prime rule: no URL that had value is ever left to 404 — it either still works or 301-redirects to the closest equivalent.** Work in four steps and **verify every redirect on the served output**.

## Step 1 — Diagnose
- Get my **old URL inventory** (current sitemap, CMS/router config, a crawl, or my analytics/Search Console export for the high-value ones — ask me for these).
- Get the **new URL set**.
- **Diff:** which URLs are unchanged, changed (need old→new mapping), removed (need a target or a deliberate 410), or new.
- For a post-relaunch cleanup: find URLs now returning **404/5xx** that used to work, redirect **chains/loops**, and internal links still pointing at old URLs.

## Step 2 — Plan & fix
- Build a **redirect map: old → new, 1:1, to the closest equivalent page.** Don't dump everything to the homepage. Show me the map to review before applying (especially for many URLs).
- Apply **301** for permanent moves (302 only for genuinely temporary; **410** for permanent removals with no equivalent).
- **Single hop** — old → final new URL, no chains.
- Update **internal links**, the **sitemap**, and **canonicals** to the new URLs.
- Implement in the right place for my stack: Next.js `redirects()` / middleware, `.htaccess`/Nginx, CDN rules, or the platform's redirect manager (Shopify/WordPress). For a **domain move**, redirect the old domain per-URL, keep it live, and tell me to do the Search Console Change of Address (my live step).

## Step 3 — Verify (on the served output)
For a sample and **all high-value URLs**, fetch each old URL (e.g. `curl -sIL <old-url>`) and confirm: it returns a **permanent redirect (301 or 308 — Next.js/Vercel `permanent` rules emit 308, which is fine; reject 302/307/200/404)** → the **correct** new URL → which returns **200**, in a **single hop**, no chains/loops, target is canonical/indexable. Confirm internal links and the sitemap point to new URLs. **If an old URL 404s or chains, it's not done.**

## Step 4 — Report
Tell me what was at risk, the redirect map you applied, served-output proof (old URLs 301 correctly), what needs me (sign-off on ambiguous mappings; submitting the new sitemap / Change of Address in Search Console). **Boundary:** redirects preserve equity at build time; the actual ranking recovery is live data I'll watch over the following weeks.

If you also have the audit mini running, record the redirects in `.seo/` so future runs re-check they didn't get dropped in a later deploy (a common silent regression).
