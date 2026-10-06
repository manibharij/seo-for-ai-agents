# Platform: WordPress

Read this when Step 0 detects WordPress. The diagnosis is unchanged: fetch the served HTML and assess every rung. What this file adds is where each fix lives in WordPress, what you cannot change, and the failures that recur on WordPress sites. Platform facts verified 2026-10 unless marked as judgement.

---

## Detection

- **Served HTML:** `/wp-content/` and `/wp-includes/` asset paths; a `Link: <https://example.com/wp-json/>; rel="https://api.w.org/"` response header; often `<meta name="generator" content="WordPress x.y">` (themes and security plugins sometimes remove it).
- **Which SEO plugin:** the plugin leaves an HTML comment in `<head>`.
  - Yoast: `<!-- This site is optimized with the Yoast SEO plugin vX ... -->`
  - Rank Math: `<!-- Search Engine Optimization by Rank Math ... -->`
  - Two SEO plugins active at once is itself a finding (see failure patterns).
- **Repo or file access:** `wp-config.php`, `wp-content/themes/<theme>/`, `wp-content/plugins/`. A child theme lives in its own folder with a `style.css` that names a `Template:` parent.
- **Hosted WordPress.com plans** may block plugins and theme file edits. Check what the plan allows before you write a plugin-based fix.

```bash
curl -sL https://example.com/ | grep -oE '<!-- [^>]*(Yoast|Rank Math)[^>]*-->|<meta name="generator"[^>]*>|<meta name=.robots.[^>]*>'
```
```powershell
$h = (Invoke-WebRequest -Uri "https://example.com/" -UseBasicParsing).Content
[regex]::Matches($h, '<!-- [^>]*(Yoast|Rank Math)[^>]*-->|<meta name="generator"[^>]*>|<meta name=.robots.[^>]*>') | ForEach-Object Value
```

---

## Where each setting lives

| Setting | Where | Notes |
|---|---|---|
| Titles and meta descriptions | Per post: the SEO plugin's box in the editor. Templates: Yoast SEO > Settings (content types), or Rank Math SEO > Titles & Meta | Fix the template for site-wide patterns; fix the post for one page |
| Canonical | The SEO plugin, per post (advanced tab) | The plugin outputs a self-referencing canonical by default. Only override with a reason |
| `noindex` | Per post in the plugin's advanced tab; per content type or taxonomy in the plugin's settings | Check archives (tags, authors, dates, attachments) here |
| Site-wide "discourage" switch | Settings > Reading > Search engine visibility | See failure patterns. Since WordPress 5.3 it outputs `<meta name='robots' content='noindex, nofollow' />` rather than a `robots.txt` disallow |
| XML sitemap | Core: `/wp-sitemap.xml` (since 5.5). Yoast: `/sitemap_index.xml`, toggled in Yoast SEO > Settings > Site features. Rank Math: `/sitemap_index.xml`, in Rank Math SEO > Sitemap Settings | Only one generator should be live. SEO plugins replace the core sitemap |
| `robots.txt` | WordPress serves a virtual file unless a physical `robots.txt` exists in the web root. Yoast and Rank Math both offer an editor (Rank Math: General Settings > Edit robots.txt) | A physical file overrides the virtual one and the plugin editor |
| Permalinks | Settings > Permalinks | Changing the structure changes every post URL. See failure patterns |
| Redirects | An SEO plugin's redirect manager (Rank Math; Yoast Premium), a redirects plugin, or the server config | Server-level redirects are fastest; plugin redirects are easiest for non-developers |
| Schema | The SEO plugin's schema settings; WooCommerce adds product markup | Check for duplicate `Product` or `Organization` graphs from several sources |
| Headings, markup, performance | The theme (block theme templates in the Site Editor, or PHP templates in classic themes) | Edit a **child theme**, never the parent, or an update will erase the fix |

---

## WooCommerce

- **Product URLs:** the product base is set in Settings > Permalinks (`/product/` by default). Changing it changes every product URL and needs redirects.
- **Faceted and sorted URLs:** `?orderby=`, `?filter_*` and layered navigation parameters can multiply listing URLs. Keep them out of the sitemap and canonical them to the unfiltered listing where they add nothing (see `4-connect-architecture/references/canonicals-and-architecture.md`).
- **Cart, checkout and account pages** should not be indexed. Check that they carry `noindex` in the served HTML.
- **Out-of-stock and discontinued products:** decide per product. Keep the page live (with the stock state in `Product` markup) if it returns; 301 to the closest replacement if it is gone for good. Never redirect everything to the home page.
- **Product schema:** WooCommerce and the SEO plugin can both emit `Product`. Validate the served HTML and keep one complete graph.

---

## What is locked or awkward

- **Core output** (feeds, oEmbed links, REST API links in `<head>`) needs code (`remove_action` in a child theme's `functions.php` or a small plugin) rather than a setting.
- **Theme markup** in a commercial theme is changed through a child theme or the theme's own options. Parent theme edits are lost on update.
- **Page builders** (Elementor, Divi and similar) control heading levels and often add heavy markup. Fix headings inside the builder widget settings.
- **Hosted plans** may forbid plugins, so a plugin-based fix becomes a plan question for a person.

---

## Known failure patterns

1. **Staging "discourage" switch left on after launch.** Settings > Reading > Search engine visibility stays ticked, so every page serves `noindex, nofollow` and the core sitemap is disabled. Check the served `<meta name="robots">` on the home page first. High severity, one-click fix, but confirm with a person that the site is meant to be live.
2. **The reverse: staging indexed.** A staging copy (`staging.example.com`, a host's temporary domain) without the switch, password protection or `noindex` gets indexed as a duplicate. Protect staging with HTTP auth or `noindex`, not `robots.txt` alone, because a blocked URL can still be indexed from links.
3. **Two SEO plugins.** Duplicate titles, two canonicals, two sitemaps. Keep one and migrate its settings.
4. **Permalink changes without redirects.** Switching from `/?p=123` or `/2024/05/post/` to `/post/` changes every URL. WordPress guesses some old post URLs, but do not rely on that. Map old to new and 301 (`seo-migrations/references/redirect-mapping.md`).
5. **Physical `robots.txt` shadowing the plugin.** Edits in the plugin "do nothing" because a file in the web root wins.
6. **Thin archives indexed.** Tag, author, date and attachment pages with little content. `noindex` them or improve them; attachment pages are usually best redirected to the file or parent post (Yoast and Rank Math both have a setting).
7. **Caching and optimisation plugins.** "Delay JavaScript" and lazy-load features can hide content or links from the raw HTML, and a stale page cache can keep serving an old title or `noindex` after a fix. Purge the cache, then verify.
8. **`noindex` set in the plugin for a whole post type** (for example, products or landing pages) by accident. Check the content-type settings, not just the post.

---

## Giving instructions when you cannot edit code

Write each finding so a site owner can apply it without guessing:

```text
Finding: every page serves <meta name="robots" content="noindex, nofollow">.
Where: WordPress admin > Settings > Reading > "Search engine visibility".
Change: untick "Discourage search engines from indexing this site", then Save Changes.
Then: purge any page cache (your caching plugin or host dashboard).
Check: open https://example.com/, view source, and confirm the robots meta tag is gone
       or reads "index, follow". Tell me and I will re-fetch it to verify.
```

Name the plugin screen by its menu path, give the exact value, and always end with a check on the live URL. Record platform-limited items in `.seo/` with status `needs-human`.

---

## Verify

Re-fetch the affected URLs (and one URL per template) after any change and after purging caches. Confirm the title, canonical, robots meta, and the sitemap URL your `robots.txt` names. A fix shown in the WordPress admin is not a fix until the served HTML shows it.
