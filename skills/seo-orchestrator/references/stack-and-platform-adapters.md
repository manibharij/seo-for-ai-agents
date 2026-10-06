# Stack and platform adapters

Read this in Step 0, straight after the first fetch. It is the routing table: detect the stack and the platform, then open the file that says where each fix lives and what you cannot change. The ladder and the diagnosis are the same everywhere, because you always judge the served HTML. What changes is where the fix lives: a code edit, a theme file, a plugin screen, a builder panel or a CMS field.

Framework facts here were verified against each framework's own documentation in 2026-10. Versions move fast, so read the project's `package.json` (or lockfile, `Gemfile`, `composer.json`) before you trust any version-specific advice, and prefer the installed version's docs over this file when they disagree.

**Out of scope:** native mobile apps and app indexing (Android App Links, iOS Universal Links, deep links into apps from search). The pack covers websites only.

---

## Step 0: detect, in this order

1. **The repo, if you have one.** Config files and dependencies are the strongest evidence (tables below).
2. **The served output.** Response headers, `<meta name="generator">`, asset paths and framework markers in the raw HTML. Use this when you only have a URL. Headers can be stripped and generator tags removed, so treat a missing signal as "unknown", never as "not this stack".
3. **Ask** only if both are inconclusive and the answer changes the fix.

```bash
URL="https://example.com/"
curl -sIL "$URL" | grep -iE "^(server|x-powered-by|powered-by|x-generator):"
curl -sL "$URL" | grep -oE '<meta name="generator"[^>]*>|/_next/static|/_nuxt/|/_app/immutable|/_astro/|ng-version|ng-server-context="[a-z]*"|q:container|__reactRouterContext|wp-content|cdn\.shopify\.com|data-wf-site|static\.parastorage\.com|static1\.squarespace\.com|framerusercontent' | sort | uniq -c
```
```powershell
$URL = "https://example.com/"
$r = Invoke-WebRequest -Uri $URL -UseBasicParsing
$r.Headers.GetEnumerator() | Where-Object { $_.Key -match '^(server|x-powered-by|powered-by|x-generator)$' }
[regex]::Matches($r.Content, '<meta name="generator"[^>]*>|/_next/static|/_nuxt/|/_app/immutable|/_astro/|ng-version|ng-server-context="[a-z]*"|q:container|__reactRouterContext|wp-content|cdn\.shopify\.com|data-wf-site|static\.parastorage\.com|static1\.squarespace\.com|framerusercontent') | Group-Object Value | Select-Object Count, Name
```

Record the result in `.seo/` state (stack, platform, version, and whether you have write access), because every later finding is phrased in that idiom.

---

## The fork: where can a fix actually be made?

| Kind | Examples | Who applies the fix | Detail |
|---|---|---|---|
| **Code-editable app** | Next.js, Nuxt, SvelteKit, Astro, React Router, Angular, TanStack Start, SolidStart, Qwik, Gatsby, SPAs, static generators | The agent, as a code change | The tables below, plus `1-reach-indexation/references/rendering-ssr-csr.md` and `2-read-content/references/metadata-titles-descriptions.md` |
| **Server-rendered stack** | Rails, Django, Laravel, plain PHP | The agent, in templates, routes and server config | Below |
| **Docs generator** | Docusaurus, VitePress, Starlight (code); Mintlify (hosted) | Config and front matter; Mintlify through its config file | Below |
| **Headless CMS + front end** | Contentful, Sanity, Strapi, Storyblok, Payload | Code for the template, editors for the field values | [platforms/headless-cms.md](platforms/headless-cms.md) |
| **Hosted platform or builder** | WordPress, Shopify, Webflow, Wix, Squarespace, Framer, Ghost, HubSpot, Drupal, BigCommerce | Usually a person, in a settings screen, plugin or theme | The platform files linked below |

On a hosted platform the diagnosis still applies in full. The agent's job shifts to diagnosing precisely and then telling the user exactly what to change and where. Never pretend a platform is code. If the platform does not expose a fix, say so and offer the closest real option, because that honesty is part of the method.

---

## Code-editable frameworks

| Stack | Detect in the repo | Detect in the served HTML | Default rendering | Where SEO fixes live | Main Reach risk |
|---|---|---|---|---|---|
| **Next.js, App Router** *(default)* | `next.config.*`, an `app/` directory | `/_next/static/`, `self.__next_f`, often `x-powered-by: Next.js` | Server Components, prerendered or server-rendered | `metadata` / `generateMetadata`, `app/sitemap.ts`, `app/robots.ts`, `redirects()` in `next.config`, `proxy.ts` | `"use client"` high in the tree; content fetched in `useEffect` |
| **Next.js, Pages Router** | a `pages/` directory | `/_next/static/`, `__NEXT_DATA__` | Static unless a data function is exported | `next/head`, `getStaticProps` / `getServerSideProps` | Content fetched client-side with no data function |
| **Nuxt** | `nuxt.config.*` | `/_nuxt/`, `__NUXT_DATA__`, often `x-powered-by: Nuxt` | Universal (server) rendering | `useSeoMeta`, `useHead`, `routeRules`, a sitemap module | `ssr: false`; real content inside `<ClientOnly>` |
| **SvelteKit** | `svelte.config.js`, `@sveltejs/kit` | `/_app/immutable/`, `data-sveltekit-*` attributes | SSR | `<svelte:head>`, `load` in `+page.ts` / `+page.server.ts`, a `+server.ts` sitemap | `export const ssr = false`; content loaded in `onMount` |
| **Astro** | `astro.config.*` | `/_astro/`, `astro-island`, usually a generator tag | Static by default; SSR per route with an adapter | The layout `<head>`, `@astrojs/sitemap` (needs `site` set) | `client:only` components; `server:defer` islands (both missing from the initial HTML) |
| **React Router, framework mode** (v7 onward; Remix v2 is its predecessor) | `react-router.config.ts`, `@react-router/dev`; `@remix-run/*` for Remix v2 | `window.__reactRouterContext` (`__remixContext` on Remix v2) | SSR (`ssr: true` is the default) | `meta` export or React 19 `<title>` / `<meta>` in components, `loader`, `headers` export | `ssr: false` (SPA mode); data in `useEffect` instead of a `loader` |
| **Angular SSR** | `angular.json`, `@angular/ssr`, `app.routes.server.ts` | `ng-version` attribute; `ng-server-context="ssr"` or `"ssg"` when server-rendered (absent means client-rendered) | **Client-side** unless `@angular/ssr` is added | Route `title` and `TitleStrategy`, the `Meta` service, render modes in `app.routes.server.ts` | No SSR at all; routes set to `RenderMode.Client`; `@defer` blocks render only their placeholder on the server |
| **TanStack Start** | `@tanstack/react-start` (or the Solid variant) | `$_TSR` script markers | SSR by default | The route `head()` option rendered by `<HeadContent />`; server routes for a sitemap | Routes with `ssr: false` |
| **SolidStart** | `@solidjs/start` | `_$HY` hydration script | SSR | `@solidjs/meta`: `<Title>`, `<Meta>`, `<Link>` | Client-only rendering configured; content fetched only in the browser |
| **Qwik City** | `@builder.io/qwik-city` (check `package.json` for the router package your version uses) | `q:container` attribute | SSR, then resumed (no hydration pass) | `export const head: DocumentHead`, `routeLoader$` | Content produced only in `useVisibleTask$`, which runs in the browser |
| **Gatsby** | `gatsby-config.*` | `id="___gatsby"`, `/page-data/` | Static | Head API, `gatsby-plugin-sitemap` | Content fetched client-side after load |
| **Vite or CRA SPA** | `vite.config.*` with no SSR framework, or `react-scripts` | A near-empty `<div id="root">` | **Client-side only** | Needs SSR or prerendering first; a big rock, flag it | Everything: the raw HTML is a shell |
| **Static generators** (Hugo, Eleventy, Jekyll) | `hugo.toml` / `config.toml`, `eleventy.config.*` / `.eleventy.js`, `_config.yml` | Often a generator tag | Static | Templates and generator config | Rarely rendering; check robots, sitemap, canonicals |

### Docs generators

| Tool | Detect | Rendering | Where SEO settings live | Locked or easy to miss |
|---|---|---|---|---|
| **Docusaurus** | `docusaurus.config.*`; generator `Docusaurus vX` | Static HTML per route | Front matter (`title`, `description`, `keywords`, `image`), `themeConfig.metadata`, the sitemap plugin in `preset-classic` | Canonical and `hreflang` links are generated for you, so check them before adding your own. Deeper markup changes need swizzled theme components |
| **VitePress** | `.vitepress/config.*`; generator `VitePress vX` | Static | Front matter (`title`, `description`, `head`), `head` and `transformHead` in config | No sitemap until `sitemap.hostname` is set in config |
| **Starlight** | `@astrojs/starlight` in the Astro config; generator `Starlight vX` | Static (Astro) | Front matter (`title`, `description`, `head`), the `head` config option | The built-in sitemap is generated only when `site` is set in `astro.config.mjs` |
| **Mintlify** (hosted) | `docs.json` in the repo; Mintlify asset hosts in the HTML | Hosted, rendered by Mintlify | Page front matter (`title`, `description`, `og:*`, `canonical`, `noindex`), `seo.metatags` in `docs.json` | Hosting and rendering are locked. `sitemap.xml` and `robots.txt` are generated, and a file of the same name in the project root replaces them |

### Server-rendered stacks

These render HTML on the server for every request, so Reach is usually fine by construction. Audit the templates, status codes and redirects instead.

| Stack | Detect | Where SEO fixes live | Watch for |
|---|---|---|---|
| **Rails** | `Gemfile` with `rails`, `config/routes.rb`; served signals are weak (`csrf-param` / `csrf-token` metas, Turbo `data-turbo` attributes) | The layout (`app/views/layouts/application.html.erb`) with `content_for :title` and `yield(:title)`; redirects in `config/routes.rb`; `public/robots.txt`; a sitemap gem | Lazy Turbo Frames (`<turbo-frame src loading="lazy">`) whose content is not in the initial HTML |
| **Django** | `manage.py`, `settings.py` | Base template blocks (`{% block title %}`, `{% block meta %}`); `django.contrib.sitemaps`; `RedirectView` or `django.contrib.redirects` | `DEBUG = True` in production; trailing-slash duplicates if a proxy rewrites URLs |
| **Laravel** | `artisan`, `laravel/framework` in `composer.json`; `XSRF-TOKEN` / `laravel_session` cookies | Blade layouts (`@yield('title')`, `@section`); `Route::permanentRedirect` in `routes/web.php`; `public/robots.txt` | **Inertia** front ends render in the browser unless Inertia's SSR server is set up and running: check the raw HTML for an empty root element |
| **Plain PHP** | `.php` entry files; often `x-powered-by: PHP/x` | Shared header includes; redirects in `.htaccess` or the nginx config | `index.php` and query-string duplicates; error pages that return `200` |

---

## Hosted platforms and CMSs

| Platform | Detect in the served output | Where SEO settings live | What is locked | Deep reference |
|---|---|---|---|---|
| **WordPress** | `/wp-content/`, `/wp-json/` in a `Link` header, generator `WordPress x.y`; plugin comments such as `This site is optimized with the Yoast SEO plugin` or `Search Engine Optimization by Rank Math` | The SEO plugin, Settings > Reading and Permalinks, the theme or child theme | On hosted plans: plugins and theme files may be unavailable | [platforms/wordpress.md](platforms/wordpress.md) |
| **Shopify** | `powered-by: Shopify` header, `cdn.shopify.com`, `window.Shopify` | Theme Liquid (`layout/theme.liquid`), `templates/robots.txt.liquid`, each resource's search engine listing, URL redirects | Fixed URL prefixes (`/products/`, `/collections/`, `/pages/`, `/blogs/`), checkout, the sitemap | [platforms/shopify.md](platforms/shopify.md) |
| **Webflow** | `data-wf-site` and `data-wf-page` attributes | Site settings > SEO, page settings, CMS collection SEO fields | Rendering, the sitemap generator, CMS item URLs under the collection slug | [platforms/site-builders.md](platforms/site-builders.md) |
| **Wix** | `x-wix-request-id` header, generator `Wix.com Website Builder`, `static.parastorage.com` | SEO & GEO dashboard, page SEO settings, URL Redirect Manager, robots.txt editor | Rendering and markup; app page URL structures | [platforms/site-builders.md](platforms/site-builders.md) |
| **Squarespace** | `server: Squarespace`, `static1.squarespace.com` | Page settings (SEO tab), site SEO settings, Developer tools > URL mappings | `robots.txt` is not editable; markup is mostly fixed | [platforms/site-builders.md](platforms/site-builders.md) |
| **Framer** | `server: Framer`, generator `Framer`, `framerusercontent.com` | Site settings (SEO, Hosting > Redirects), page settings | Rendering, sitemap, much of the markup | [platforms/site-builders.md](platforms/site-builders.md) |
| **Ghost, HubSpot CMS, Drupal, BigCommerce** | Generator `Ghost x.y`; generator `HubSpot` and `x-hs-*` headers; generator or `x-generator: Drupal`; BigCommerce asset hosts | See the short section in the site-builders file | Varies | [platforms/site-builders.md](platforms/site-builders.md) |
| **Headless CMS** (Contentful, Sanity, Strapi, Storyblok, Payload) | Only in the repo: `contentful`, `@sanity/client` / `next-sanity`, `@strapi/*`, `@storyblok/*`, `payload` | Field values in the CMS; the tags they become in the front-end templates | Nothing reaches the live page until the front end rebuilds or revalidates | [platforms/headless-cms.md](platforms/headless-cms.md) |

---

## Per-stack notes that cut across rungs

### Next.js, App Router (the default)
- **Reach:** Server Components render on the server by default. Failures come from `"use client"` placed too high, or data loaded in `useEffect`. Push client boundaries down to interactive leaves and fetch on the server.
- **Read:** the Metadata API (`metadata`, `generateMetadata`, `title.template`, `metadataBase`). Since 15.2, `generateMetadata` can stream: for browsers and bots that run JavaScript the tags may be appended to `<body>`, while HTML-only bots (Next.js keeps a user-agent list, `htmlLimitedBots`) get them in `<head>`. Check the served HTML with more than one user agent.
- **Understand:** JSON-LD as a native `<script type="application/ld+json">` in a page or layout, escaping `<` as `<`. Not `next/script`.
- **Connect:** `<Link href>` renders a real `<a href>`; canonicals through `alternates.canonical`.
- **Plumbing:** `app/sitemap.ts`, `app/robots.ts`; redirects in `next.config` `redirects()` or in **`proxy.ts`**. Next.js 16 deprecated the `middleware` file convention and renamed it `proxy` (file `proxy.ts`, exported function `proxy`, Node.js runtime by default). The codemod is `npx @next/codemod@canary middleware-to-proxy .`. On an older project, look for `middleware.ts` instead.
- **Since 15:** `params`, `searchParams` and `draftMode()` are Promises and must be awaited.

### Next.js, Pages Router
Data through `getStaticProps` / `getServerSideProps`, not `useEffect`. Metadata through `next/head`. Same principles, older APIs.

### Everything else
Use the tables above to find where fixes live, then go to the deep reference for the rung:
- Rendering and Reach, per framework: `1-reach-indexation/references/rendering-ssr-csr.md`.
- Hydration, streaming, links, soft 404s, JavaScript-set `noindex` and canonicals: `1-reach-indexation/references/javascript-seo.md`.
- Titles, canonicals, Open Graph, JSON-LD, `noindex` and `hreflang` per framework: `2-read-content/references/metadata-titles-descriptions.md`.
- Moving between stacks: `seo-migrations/references/framework-migrations.md`.

---

## Using the adapter in the audit

1. Detect the stack and the platform in Step 0 and record them, with the version, in `.seo/`.
2. Phrase each fix in the right idiom (the code change, or the exact setting and screen) and adjust the effort. A fix that is one line in Next.js can be awkward or impossible on a hosted builder, and `prioritisation.md` should weight it accordingly.
3. Without write access, or on a hosted platform, write each finding as an instruction a person can follow: the screen, the field, the value, and how to check it afterwards on the live URL. Each platform file has a template for this.
4. Record anything the platform will not let you change as `needs-human` or `wont-fix` with the reason, so a later audit does not raise it again as new.
