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
- **Reciprocity:** if A points to B, B must point back to A. Google says annotations without return links may be ignored.
- **Correct codes:** ISO 639-1 language, optionally followed by an ISO 3166-1 Alpha 2 region: `en`, `en-GB`, `es`, `es-MX`. A region on its own (`GB`) is not valid, and `en-UK` is wrong (the code is `GB`). Wrong codes silently fail.
- **Canonical + hreflang together:** each locale page canonicalises to **itself**, not to one master locale (canonicalising all locales to the English page hides the others).
- Implement it one way: `<link>` tags in the `<head>`, HTTP `Link` headers (useful for PDFs), or the XML sitemap. Verify it in the **served output** or the served sitemap.

Google facts in this profile were checked against Google Search Central in October 2026 (verified 2026-10): https://developers.google.com/search/docs/specialty/international/localized-versions and https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites.

## `x-default` rules
- `x-default` is the page for users whose language or region matches none of your versions. Google says it works best with language selector pages; a sensible default locale is also common.
- Give each cluster at most one `x-default`, and include it in every page of the cluster, like the other alternates.
- Point it at a page that serves everyone: a language picker, or the global or default-language version. Do not point it at a page that auto-redirects by IP, because Googlebot (which mostly crawls from the USA and sends no `Accept-Language`) would only ever see one outcome.
- `x-default` can share a URL with another entry (for example `en` and `x-default` both pointing at `/`). That is valid.
- It is optional. Without it, unmatched users get whichever version Google picks.

## hreflang in sitemaps

For large sites, sitemap annotations keep the `<head>` small and are easier to generate from one locale table. Each `<url>` lists every alternate including itself and `x-default`, and every locale URL gets its own `<url>` entry with the same set.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/en-gb/pricing</loc>
    <xhtml:link rel="alternate" hreflang="en-GB" href="https://example.com/en-gb/pricing"/>
    <xhtml:link rel="alternate" hreflang="en-US" href="https://example.com/en-us/pricing"/>
    <xhtml:link rel="alternate" hreflang="fr-FR" href="https://example.com/fr-fr/tarifs"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/pricing"/>
  </url>
  <url>
    <loc>https://example.com/en-us/pricing</loc>
    <xhtml:link rel="alternate" hreflang="en-GB" href="https://example.com/en-gb/pricing"/>
    <xhtml:link rel="alternate" hreflang="en-US" href="https://example.com/en-us/pricing"/>
    <xhtml:link rel="alternate" hreflang="fr-FR" href="https://example.com/fr-fr/tarifs"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/pricing"/>
  </url>
  <url>
    <loc>https://example.com/fr-fr/tarifs</loc>
    <xhtml:link rel="alternate" hreflang="en-GB" href="https://example.com/en-gb/pricing"/>
    <xhtml:link rel="alternate" hreflang="en-US" href="https://example.com/en-us/pricing"/>
    <xhtml:link rel="alternate" hreflang="fr-FR" href="https://example.com/fr-fr/tarifs"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/pricing"/>
  </url>
</urlset>
```
The `xmlns:xhtml` declaration is required. Every URL listed must return `200` and be self-canonical. Do not mix methods for the same pages with different values: if the `<head>` and the sitemap disagree, you have created the conflict you were trying to avoid.

## Framework i18n routing

**Next.js App Router (the pack's default).** The App Router has no built-in i18n config (that was a Pages Router feature). The Next.js guide builds it from a `[lang]` segment and a request interceptor; libraries such as `next-intl` package the same pattern. From Next.js 16 the interceptor file is `proxy.ts` (earlier versions called it `middleware.ts`).
- Put routes under `app/[lang]/`, set `<html lang>` from the param in `app/[lang]/layout.tsx`, and pre-render locales with `generateStaticParams`. Return `notFound()` for unknown locales.
- Emit hreflang from `generateMetadata` with `alternates.languages`. Next.js accepts `x-default` as a key.

```tsx
// app/[lang]/pricing/page.tsx
import type { Metadata } from 'next'

const base = 'https://example.com'
const locales = ['en-gb', 'en-us', 'fr-fr'] // URL segments

export async function generateMetadata(
  { params }: { params: Promise<{ lang: string }> }
): Promise<Metadata> {
  const { lang } = await params
  if (!locales.includes(lang)) return {}
  return {
    alternates: {
      canonical: `${base}/${lang}/pricing`, // self-canonical, never the default locale
      languages: {
        'en-GB': `${base}/en-gb/pricing`,
        'en-US': `${base}/en-us/pricing`,
        'fr-FR': `${base}/fr-fr/pricing`,
        'x-default': `${base}/pricing`,
      },
    },
  }
}
```
- `app/sitemap.ts` accepts `alternates.languages` per entry and emits the `xhtml:link` tags. Include the entry's own locale in its `languages` map: Next.js's own example omits it, and self-reference is required.
- **The redirect trap:** the common Next.js i18n example redirects any locale-less path to a locale chosen from `Accept-Language`. Googlebot sends no `Accept-Language`, so it is always sent to the default locale from `/`. Keep every locale reachable by its own URL with no redirect, link the locales to each other, and make the root either a real page (the `x-default`) or a single, stable redirect to the default locale. Do not redirect a request that already has a locale prefix.

**Nuxt (`@nuxtjs/i18n`).** Set `baseUrl` and give every locale a `language` (for example `{ code: 'en', language: 'en-GB' }`). Without these, the module cannot write correct hreflang. Call `useLocaleHead()` in the layout and pass its `htmlAttrs`, `link` and `meta` to `useHead`; it writes `<html lang>`, hreflang alternates, the canonical and `og:locale` tags.
- `detectBrowserLanguage` is **on by default**, with a cookie and `redirectOn: 'root'`, so only `/` is redirected. Keep `redirectOn: 'root'` at most; for the cleanest setup, set `detectBrowserLanguage: false` and use a suggestion banner (below).
- Check the served HTML for the `x-default` entry and self-reference rather than assuming the module wrote what you expect.

Other stacks (Astro, SvelteKit, Remix, hosted platforms): apply the same rules and verify on the served output. Platform notes are in `platforms/`.

## Locale suggestion banners instead of forced redirects

Google advises against automatically redirecting users from one language version to another: it can stop users and search engines from seeing all versions. Suggest instead of forcing:
- Serve the requested URL as asked, always, with `200`.
- If the visitor's browser language or location suggests another version, show a dismissible banner: "This page is available in Français. Switch?" linking to the equivalent page (not the homepage).
- Remember the choice (a cookie) and respect it on later visits. A remembered choice may redirect a person who chose it; a guess must not.
- Render the banner client-side or vary it carefully: the server HTML that crawlers see stays the same for every visitor.
- Keep a visible language switcher on every page, with plain `<a href>` links to each equivalent page, so crawlers and users can reach every locale.

## Check hreflang reciprocity

Run this on a sample of URLs per template (home, a category, a detail page) in every locale. It fetches the served HTML, reads the hreflang links, fetches every alternate, and reports missing return links, missing self-references, non-`200` alternates, redirects, malformed codes and canonicals that point elsewhere. Python 3 standard library only, so it runs the same in bash and PowerShell.

```python
#!/usr/bin/env python3
"""Check hreflang reciprocity on served HTML.
Usage: python hreflang_check.py URL [URL ...]   (exit code 1 if any issue)"""
import re, sys, urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin

CODE = re.compile(r"^(x-default|[a-z]{2,3}(-[a-z]{4})?(-([a-z]{2}|[0-9]{3}))?)$", re.I)

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.alts, self.canonical = {}, None
    def handle_starttag(self, tag, attrs):
        if tag != "link": return
        a = {k.lower(): (v or "") for k, v in attrs}
        rel = a.get("rel", "").lower().split()
        if "alternate" in rel and "hreflang" in a: self.alts[a["hreflang"]] = a.get("href", "")
        if "canonical" in rel: self.canonical = a.get("href")

cache = {}
def fetch(url):
    if url not in cache:
        req = urllib.request.Request(url, headers={"User-Agent": "hreflang-check/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                final, status, html = r.geturl(), r.status, r.read().decode("utf-8", "replace")
        except Exception as e:
            cache[url] = (getattr(e, "code", "ERR"), url, {}, None); return cache[url]
        p = Links(); p.feed(html)
        cache[url] = (status, final, {k: urljoin(final, v) for k, v in p.alts.items()},
                      urljoin(final, p.canonical) if p.canonical else None)
    return cache[url]

norm = lambda u: u.rstrip("/") if u else u
problems = 0
for start in sys.argv[1:]:
    status, final, alts, canon = fetch(start)
    print(f"\n{start}  [{status}]  {len(alts)} hreflang links")
    issues = []
    if final != start: issues.append(f"redirects to {final}")
    if not alts: issues.append("no hreflang links in served HTML")
    if canon and norm(canon) != norm(final): issues.append(f"canonical points elsewhere ({canon})")
    if alts and norm(final) not in {norm(u) for u in alts.values()}: issues.append("no self-referencing hreflang")
    if alts and "x-default" not in {k.lower() for k in alts}: issues.append("no x-default (fine only if you have no fallback page)")
    for code, url in alts.items():
        if not CODE.match(code): issues.append(f"invalid code '{code}'")
        if code.lower() == "x-default" or norm(url) == norm(final): continue
        s2, f2, alts2, _ = fetch(url)
        if s2 != 200 or f2 != url: issues.append(f"{code}: {url} returned {s2}" + (f", redirected to {f2}" if f2 != url else ""))
        elif norm(final) not in {norm(u) for u in alts2.values()}: issues.append(f"{code}: {url} does not link back")
    print("\n".join("  - " + i for i in issues) or "  ok")
    problems += len(issues)
sys.exit(1 if problems else 0)
```
```bash
python3 hreflang_check.py https://example.com/en-gb/pricing https://example.com/fr-fr/tarifs
```
```powershell
python .\hreflang_check.py https://example.com/en-gb/pricing https://example.com/fr-fr/tarifs
```
The code check is syntax only: `en-UK` passes the pattern but is still wrong. Read the codes too. For sitemap-based hreflang, check the sitemap entries instead, since the HTML will have none.

## URL structure (pick one, be consistent)
- **Subdirectories** (`example.com/fr/`) — simplest, consolidates domain authority. Common default.
- **Subdomains** (`fr.example.com`) — more separation, more setup.
- **ccTLDs** (`example.fr`) — strongest geo-signal, most overhead.

## Type-specific checks
- **No forced geo/IP redirects** that block crawlers from other locales; suggest with a banner instead.
- **Translated, not duplicated:** real localisation; don't ship the same language under two regions with no difference.
- **Currency/format** localised (ties to e-commerce profile).
- **hreflang reciprocity and self-reference** present and correct in the served output (run the check above).
- **One `x-default` per cluster**, pointing at a page that does not auto-redirect.

## Common failures
- Missing/one-way/typo'd hreflang (the most common international bug).
- All locales canonicalising to the English version (hides the rest).
- IP or `Accept-Language` redirects trapping crawlers in a single locale.
- Framework i18n that redirects every locale-less URL, so the root never serves a page.
- "Translation" that's the same language with a different flag.

## Priority tilt
Weight **Connect** (hreflang + canonicals + URL strategy) highest, then **Read** (genuine localisation). Combine with the base profile for everything else. On an existing international site, treat hreflang clusters as **intentional** — verify before changing (see `existing-site-safety.md`).
