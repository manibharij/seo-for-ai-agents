---
name: seo-access-international
description: >-
  Multi-country and multilingual sites: hreflang, per-locale canonicals, URL
  strategy, geo-targeting and genuine localisation. Use on any "hreflang",
  "international SEO", "multilingual", "multiple countries", "locales",
  "translation", "ccTLD vs subdirectory", "wrong language version is ranking",
  "geo-targeting", or "we're launching in another country" request. Validates on
  the served output, because hreflang fails silently and a half-built cluster is
  worse than none.
---

# International — hreflang, locales, and failing silently

International is the Access work with the worst failure mode in this pack: **when it is
wrong, nothing happens.** No error, no warning, no drop in a dashboard. Google simply
ignores annotations it cannot reconcile, and the wrong locale keeps ranking in the wrong
market until someone looks.

That is why this is a skill and not a checklist item. The work is validation on the served
output, at scale, across a relationship between pages rather than on any one page.

Depth lives in `seo-orchestrator/references/profiles/international.md`, including the full
hreflang mechanism and the Google sources behind it. This skill is the workflow.

Work the four steps: **Diagnose → Fix → Verify (on served output) → Report.**

---

## When this fires
- Any site with more than one language or country version.
- "The French page ranks in the UK" or the reverse.
- Planning a launch into a new market.
- A migration that touched locales, which is where clusters usually break.
- Machine-translated content being passed off as localisation.

## Inputs and modes

Infer these before Step 1. Ask only if a wrong guess would be costly (see `seo-orchestrator/references/operating-modes.md`).
- **Access:** URL only, read-only repo, or write access. Without write access, every fix becomes a precise instruction instead of an edit.
- **Mode:** `audit` (default) never changes the site. `fix` applies approved findings on a branch, verified on served output. `re-check` re-tests.
- **Scope:** one template across all locales is usually the right unit, because the faults are structural rather than per page.
- **Safety:** on an established international site, treat existing hreflang clusters and locale canonicals as **intentional** until the history says otherwise. Never bulk-rewrite locale wiring without sign-off. See `seo-orchestrator/references/existing-site-safety.md`.
- **Record findings** with `skill: seo-access-international`, `system: access`.

---

## Step 1 — Diagnose, on the served output

**hreflang, which is where most of the faults are:**
- **Self-reference.** Every page lists itself among its alternates. A cluster without self-references is commonly ignored.
- **Reciprocity.** If A points to B, B points back to A. Non-reciprocal annotations are
  silently discarded, and this is the single most common international bug.
- **Valid codes.** ISO 639-1 language, optionally with an ISO 3166-1 Alpha-2 region: `en`,
  `en-GB`, `es-MX`. A region alone is invalid, and `en-UK` is wrong because the code is `GB`.
  Wrong codes fail without complaint.
- **`x-default`** present for the fallback.
- **One implementation.** `<link>` tags, HTTP `Link` headers, or the XML sitemap. Pick one;
  check it in the served output or the served sitemap, not the source.

**Canonicals:** each locale self-canonicalises. Canonicalising every language to the English
page is the fastest way to remove every other language from search, and it is common.

**Crawlability of every locale:**
- No IP or `Accept-Language` redirects that trap crawlers in one locale. Googlebot mostly
  crawls from the US, so a forced redirect can mean it only ever sees the US version. Offer
  a dismissible banner instead of a redirect.
- Every locale in the sitemap, or a sitemap per locale.
- Framework i18n that redirects the locale-less root so nothing is served there.

**Localisation, which is Substance not Access**, but gets found here: machine-translated
boilerplate, one language with a swapped flag, or currency and contact details copied from
the origin market. Hand it to `seo-substance-content-editing` with the finding.

**`<html lang>`** correct per locale.

## Step 2 — Fix

- Decide and apply **one URL strategy**: subdirectories (`/fr/`), subdomains, or ccTLDs.
  Subdirectories are the usual default for a single brand. Changing an existing strategy is
  a migration and goes through `seo-access-migrations` with sign-off.
- Rebuild hreflang clusters completely rather than patching: a half-migrated cluster is
  worse than none.
- Make each locale self-canonical.
- Remove forced geo-redirects; add a dismissible locale suggestion if the business wants one.
- Set `<html lang>` and, where relevant, `inLanguage` in schema, with one consistent
  organisation `@id` across locales.

## Step 3 — Verify (on the served output)

- Fetch a page from each locale and read its `<link rel="alternate">` set, or the headers,
  or the sitemap entry, whichever the site uses.
- Build the cluster from what is **served** and check reciprocity programmatically across
  the whole set. This is the check people skip and the one that finds the fault.
- Confirm each locale's canonical points at itself.
- Request a locale-specific URL from outside the target country and confirm it is not
  redirected.

## Step 4 — Report

- Which clusters are valid, which are one-way, and which have invalid codes, with the
  specific pages and values.
- The URL strategy, stated, and whether it is applied consistently.
- Anything that looked deliberate and was left alone, named, so the owner can confirm.
- Localisation quality as a separate finding, because it is Substance work and a different
  budget.

Say plainly that hreflang does **not** make a locale rank in its market: it tells Google
which version to show to whom. Market performance is the usual five systems in that market,
and `seo-demand-keyword-research` should be run per market rather than translated.

---

## Reference files
- `seo-orchestrator/references/profiles/international.md` — the depth: the hreflang mechanism in full, the URL strategy trade-offs, the common failures, and the verified Google sources.
- `seo-access-connect/SKILL.md` — canonicals and the site graph that hreflang sits on top of.
- `seo-access-migrations/SKILL.md` — for changing an existing locale structure, which is a migration.
- `seo-orchestrator/references/existing-site-safety.md` — why existing locale wiring is treated as intentional.
