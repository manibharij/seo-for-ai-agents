# Platforms: site builders and hosted CMSs

Read this when Step 0 detects Webflow, Wix, Squarespace or Framer, or one of the hosted CMSs in the short section at the end (Ghost, HubSpot CMS, Drupal, BigCommerce). On all of them the diagnosis is the usual one, on the served HTML. The fixes live in builder panels, so most findings become instructions for a person. Platform facts verified 2026-10 against each platform's help centre unless marked as judgement. Builders rename their menus often, so if a menu path below is not where the user looks, ask them to search the settings for the field name.

---

## What all builders have in common

- **Rendering is the platform's.** You cannot switch a builder from client-side to server-side rendering. The big builders serve content in the initial HTML for normal pages. Embedded widgets, third-party apps and custom code blocks are the usual exceptions, so check those in the raw HTML.
- **Markup is mostly fixed.** Heading levels, image `alt` text and link text are usually editable per element. Wrapper markup and template structure are not.
- **Sitemaps are generated.** You control inclusion (through page-level indexing toggles), not the file.
- **Redirects work only for dead URLs on some builders** (Squarespace says so explicitly). Unpublish or delete the old page first.
- **Staging domains** (`*.webflow.io`, free subdomains, preview links) can be indexed as duplicates. Check each one.
- **Custom code** (head code injection, embeds) is often available on paid plans and is the escape hatch for canonicals, `hreflang` or JSON-LD the builder does not support. Treat it carefully: injected tags can duplicate tags the builder already prints.

---

## Webflow

**Detection:** `data-wf-site` and `data-wf-page` attributes on `<html>`.

| Setting | Where |
|---|---|
| Title, meta description, Open Graph | Page settings (static pages); for CMS items, the SEO settings on the collection template, bound to CMS fields |
| Global canonical | Site settings > SEO > Global canonical tag URL. Enter the base URL with protocol and `www` if used, **without** a trailing slash (a trailing slash produces `//` in every canonical) |
| Page canonical | Page settings > Page canonical URL (overrides the global one for that page) |
| `noindex` | The page's **Sitemap indexing** toggle adds `<meta content="noindex" name="robots">` and removes the page from the sitemap. CMS items have an equivalent per-item setting |
| `robots.txt` | Site settings > SEO > Indexing. Once created it cannot be deleted, only replaced (an empty `Disallow:` allows everything) |
| Sitemap | Site settings > SEO > Sitemap: "Auto-generate sitemap"; Webflow adds the sitemap URL to `robots.txt` |
| Staging subdomain | Site settings: turn **staging indexing** off. Webflow then serves a blocking `robots.txt` only on the `webflow.io` subdomain |
| 301 redirects | Site settings, in the redirects section of the publishing settings |

**Locked:** rendering, CMS item URLs (they sit under the collection's slug), the sitemap format, assets served from Webflow's CDN (a `robots.txt` on your domain cannot control them).

**Failure patterns:**
- A canonical injected through Google Tag Manager or custom code **plus** the global canonical: two canonicals. Webflow's own docs warn that search engines may then ignore both.
- The `webflow.io` staging domain indexed alongside the custom domain.
- A page blocked in `robots.txt` but still listed in the auto-generated sitemap. Webflow keeps `robots.txt`-blocked pages in the sitemap; use the Sitemap indexing toggle instead.
- CMS templates with an empty SEO description binding, so every item shares the default.

---

## Wix

**Detection:** `x-wix-request-id` header, `<meta name="generator" content="Wix.com Website Builder">`, assets on `static.parastorage.com`.

| Setting | Where |
|---|---|
| Title, description, canonical, `noindex` per page | The page's SEO settings in the editor (SEO basics and advanced SEO) |
| Site-wide SEO and patterns | The **SEO & GEO** dashboard (SEO settings for each page type) |
| `robots.txt` | SEO & GEO dashboard > Tools and settings > Robots.txt Editor. Wix warns its support will not help with custom changes |
| Redirects | SEO & GEO dashboard > Tools and settings > **URL Redirect Manager**. Up to 5,000 redirects per site; the home page cannot be redirected there (redirect at domain level instead); 301s work only on a custom domain |
| Structured data | Page-level structured data markup in advanced SEO settings; apps (Stores, Bookings) add their own |

**Locked:** rendering and most markup; app page URL structures; the sitemap.

**Failure patterns:**
- Pages excluded from indexing in page settings that someone later expects to rank; `robots.txt` edits made to "fix" this instead of the page setting (Wix itself recommends checking page settings first).
- Duplicate structured data from a manual block plus an app.
- Redirects set up while the site was still on a free Wix URL, which cannot work.

---

## Squarespace

**Detection:** `server: Squarespace` header, assets on `static1.squarespace.com`.

| Setting | Where |
|---|---|
| Title, description, URL slug, social image | The page's settings, SEO tab |
| Site-wide title formats and description | The site's SEO settings panel |
| `noindex` a page | The page's SEO settings ("hide from search engines") |
| Redirects | Developer tools > **URL mappings**. Syntax: `/old-url -> /new-url 301`. About 400 KB of mappings (roughly 2,500 lines). A mapping only fires when no live page exists at the old URL |
| `robots.txt` | **Not editable.** The only control is a Crawlers setting that asks a listed set of AI crawlers not to crawl (off by default) |
| Sitemap | Automatic at `/sitemap.xml` |

**Locked:** `robots.txt`, rendering, most template markup, the sitemap. Code injection is available on some plans for extra head tags.

**Failure patterns:**
- Redirects added while the old page is still live, so they never fire.
- The AI-crawler opt-out ticked without a decision from a person, which removes the site from those assistants' crawl (see `cite-aeo-geo/references/ai-crawlers-and-llms-txt.md`).
- Default page titles built from the site title with no page-specific text.

---

## Framer

**Detection:** `server: Framer` header, `<meta name="generator" content="Framer ...">`, assets on `framerusercontent.com`.

| Setting | Where |
|---|---|
| Title and description | Site settings for defaults; each page's settings for overrides; CMS pages bind to CMS fields |
| `noindex` | The page's "show page in search engines" setting |
| Redirects | Site settings > Hosting > Redirects. Wildcards are supported (`/blog/*`) |
| Sitemap and `robots.txt` | Generated automatically (`/sitemap.xml`); treat `robots.txt` as locked unless the user's plan exposes an editor |
| JSON-LD | Custom code in page or site settings |

**Locked:** rendering (Framer server-renders pages), sitemap, most markup.

**Failure patterns:** CMS pages without bound SEO fields (identical titles); animation-heavy layouts that hurt page experience; custom-code JSON-LD that drifts from the visible content.

---

## Ghost, HubSpot CMS, Drupal and BigCommerce

- **Ghost.** Detect with `<meta name="generator" content="Ghost x.y">`. Per post: meta title, description, canonical URL and social cards in the post settings. Sitemap is automatic. Redirects through a `redirects.yaml` file (301 and 302 blocks) uploaded in the admin's Labs settings; custom routes in `routes.yaml`. Site-wide head tags through code injection; markup through the theme (Handlebars), which a developer can edit.
- **HubSpot CMS.** Detect with `<meta name="generator" content="HubSpot">` and `x-hs-*` response headers. Titles, descriptions and canonicals in each page's settings; `robots.txt`, redirects and domain settings in the account's website settings; markup through templates and modules in the design manager. Hosting and CDN are locked.
- **Drupal.** Detect with a `Drupal` generator tag or `x-generator: Drupal` header. SEO depends on contributed modules: Metatag (titles, descriptions, canonicals, Open Graph), Pathauto (URL patterns), Redirect, and a sitemap module such as Simple XML Sitemap. `robots.txt` is a file in the web root. Self-hosted Drupal is code-editable; managed hosts may restrict modules.
- **BigCommerce.** Edit `robots.txt` in Settings > Website (Search Engine Robots section, needs the Manage Settings permission). 301 redirects in Settings > 301 Redirects, with bulk import (paid plans). Markup through the Stencil theme. Headless BigCommerce (for example the Catalyst front end) is a code-editable Next.js app.

---

## Giving instructions when you cannot edit anything

The user applies the fix; your job is to make it unambiguous and checkable.

```text
Finding: https://example.webflow.io/ is indexable and duplicates https://www.example.com/.
Where: Webflow > Site settings > SEO > Indexing.
Change: turn off staging (webflow.io) indexing, then publish the site.
Check: open https://example.webflow.io/robots.txt and confirm it now disallows all crawlers.
       Tell me and I will re-fetch it to verify. The custom domain must be unaffected.
```

Always include: the screen and field, the exact value, whether a publish step is needed, and the live URL to check. Record what the builder does not support as `needs-human` or `wont-fix` with the reason and the closest available option (for example, custom head code on a paid plan).

---

## Verify

Builders publish asynchronously and cache at the edge. Wait for the publish to finish, then fetch the live custom-domain URL and confirm the change in the served HTML. Check the staging domain separately.
