# Profile: international / multilingual

Use for any site targeting multiple countries or languages. This is a **modifier you combine** with another profile (e.g. international + e-commerce). The defining concern is **hreflang** and a clean multi-locale architecture so the right version is served to the right audience without duplicate-content confusion.

## How each rung shifts
- **Reach** — each locale's content must be reachable and in the served HTML; each locale in the sitemap (or per-locale sitemaps). Avoid IP-based auto-redirects that trap crawlers in one locale — let all locales be crawlable; use hreflang to express the relationship, not forced redirects.
- **Read** — genuinely localised content (real translation/localisation), not machine-translated boilerplate or one language with a swapped flag. Correct `<html lang>` per locale (e.g. `en-GB`, `fr-FR`).
- **Understand** — schema consistent per locale; `inLanguage` where relevant; consistent entity `@id` for the organisation across locales.
- **Connect** — the heart of this profile: **hreflang** annotations linking equivalent pages across locales, plus correct canonicals (each locale self-canonicalises; hreflang expresses alternates). Clear URL strategy (subdirectory `/fr/`, subdomain, or ccTLD).
- **Cite** — answer formatting in each locale's language; entity consistency across locales so engines resolve one organisation.

## hreflang — the core mechanism
- Each page lists `rel="alternate" hreflang="<lang>[-<REGION>]"` for **every** locale version, **including itself** (self-referential), plus `hreflang="x-default"` for the fallback.
- **Reciprocity:** if A points to B, B must point back to A. Non-reciprocal hreflang is ignored.
- **Correct codes:** ISO language (+ optional ISO region): `en`, `en-GB`, `es`, `es-MX`. Wrong codes silently fail.
- **Canonical + hreflang together:** each locale page canonicalises to **itself**, not to one master locale (canonicalising all locales to the English page hides the others).
- Implement in the `<head>` or via an XML sitemap's hreflang annotations; verify they're in the **served output**.

## URL structure (pick one, be consistent)
- **Subdirectories** (`example.com/fr/`) — simplest, consolidates domain authority. Common default.
- **Subdomains** (`fr.example.com`) — more separation, more setup.
- **ccTLDs** (`example.fr`) — strongest geo-signal, most overhead.

## Type-specific checks
- **No forced geo/IP redirects** that block crawlers from other locales.
- **Translated, not duplicated:** real localisation; don't ship the same language under two regions with no difference.
- **Currency/format** localised (ties to e-commerce profile).
- **hreflang reciprocity and self-reference** present and correct in the served output.

## Common failures
- Missing/one-way/typo'd hreflang (the most common international bug).
- All locales canonicalising to the English version (hides the rest).
- IP redirects trapping crawlers in a single locale.
- "Translation" that's the same language with a different flag.

## Priority tilt
Weight **Connect** (hreflang + canonicals + URL strategy) highest, then **Read** (genuine localisation). Combine with the base profile for everything else. On an existing international site, treat hreflang clusters as **intentional** — verify before changing (see `existing-site-safety.md`).
