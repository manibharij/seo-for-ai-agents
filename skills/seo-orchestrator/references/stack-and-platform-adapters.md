# Stack & platform adapters

Read this to make the audit fit the **specific** site. The Visibility Ladder is universal; *how* you diagnose and fix each rung depends on the stack (which framework) and the platform (code-editable app vs hosted/CMS). Detect both in Step 0, then adapt.

> The **diagnosis** is the same everywhere — you always check the served HTML. The **fix** is what changes: a code edit in Next.js, a theme/plugin/setting in WordPress, an app setting in Shopify.

---

## The big fork: code-editable vs hosted/CMS

### Code-editable apps (agent can edit the source)
Next.js, Astro, Nuxt, SvelteKit, Remix, Gatsby, Vite/CRA SPAs, static sites. The agent can directly apply fixes in code. This is the pack's home turf and where fixes are most complete.

### Hosted / CMS / site builders (fixes live in the platform, not your code)
WordPress, Shopify, Wix, Squarespace, Webflow, etc. **The diagnosis still fully applies** — fetch the served HTML and assess every rung exactly the same way. But the **fixes** are often *not* code an agent can edit:
- They live in **platform settings**, a **theme**, **plugins/apps**, or template editors.
- Some are not fixable on the platform at all (e.g. forced client-rendering, or platform-controlled markup).

So on a hosted platform, the agent's job shifts to: **diagnose precisely, then tell the user exactly what to change and where** (which setting, which plugin, which theme file), rather than editing code it doesn't control. Be honest about what the platform won't let you change.

Platform quick-notes (diagnosis universal; fixes as below):
- **WordPress** — most on-page SEO via a plugin (Yoast/Rank Math/SEO Framework): titles, descriptions, canonicals, sitemaps, schema, `noindex`. Theme controls headings/markup/performance. Guide the user to the plugin/theme settings; some fixes need theme/child-theme edits (which an agent *can* do if it has file access).
- **Shopify** — titles/descriptions and some schema via theme Liquid templates and theme settings; sitemap/robots largely auto-managed (and partly locked); apps add structured data. Faceted/collection URLs and duplicate variants need care. Point to theme files and app settings.
- **Wix / Squarespace / Webflow** — SEO controlled through the builder's SEO panels and page settings; markup and rendering are largely platform-controlled. Diagnose and instruct via the builder UI; note what the platform doesn't expose.

> Don't pretend a hosted platform is code. If a fix isn't available in the platform, say so and give the user the closest real option — that honesty is part of the method.

---

## Per-stack adapter (code-editable)

How each rung typically manifests and gets fixed, by framework. (Reach detail is also in `1-reach-indexation/references/rendering-ssr-csr.md`; this is the cross-rung quick map.)

### Next.js — App Router *(default)*
- **Reach:** Server Components render server-side by default; failures come from `"use client"` too high or data in `useEffect`. Fix: server fetch, push client boundaries down.
- **Read/metadata:** Metadata API (`metadata` / `generateMetadata`, `title.template`, `metadataBase`). Page experience via `next/image`, `next/font`, `next/dynamic`.
- **Understand:** JSON-LD from a server component (`<script type="application/ld+json">`), rendered from the same data as the page.
- **Connect:** `<Link href>` (real `<a href>`); canonicals via `alternates.canonical` derived from the route.
- **Reach plumbing:** `app/sitemap.ts`, `app/robots.ts`. (Next 15: `params` is a Promise — await it.)

### Next.js — Pages Router
- Data via `getServerSideProps`/`getStaticProps` (not `useEffect`). Metadata via `next/head`. Sitemap via a library or API route. Same principles, older APIs.

### Astro
- SSG/SSR by default, ships no JS unless asked — usually strong on Reach/performance. Watch `client:only` hiding content. Metadata in the layout `<head>`; `@astrojs/sitemap`; JSON-LD in templates.

### Nuxt (Vue)
- SSR/SSG by default; watch `ssr: false` and `<client-only>`. `useHead()` for metadata; `@nuxtjs/sitemap`.

### SvelteKit
- SSR by default; watch `export const ssr = false` and `onMount`-only content. `load` functions for data; `<svelte:head>` for metadata; endpoint for sitemap.

### Remix / React Router (framework mode)
- SSR via route `loader`s; move `useEffect` fetches into loaders. `meta` export for metadata.

### Gatsby
- SSG; content from the build-time data layer. `gatsby-plugin-sitemap`; Head API / react-helmet for metadata.

### Vite / CRA SPA
- Pure CSR — empty shell, the classic Reach failure. Fix = introduce SSR/prerender (migrate to a meta-framework, add `vike`, or prerender routes). A **big rock** — flag it.

### Static HTML / SSGs (Hugo, Eleventy, Jekyll)
- Reach-rendering is fine by construction; focus on metadata, schema, internal links, and the generator's sitemap/robots config.

---

## Using the adapter in the audit
1. Detect stack + platform in Step 0.
2. For each finding, frame the **fix** in the right idiom (the code change *or* the platform setting), and adjust the **effort** estimate accordingly (a fix that's trivial in Next.js may be awkward or impossible on a hosted builder).
3. On hosted platforms, write findings as **clear instructions for the user** ("In Yoast → Search Appearance, set …") rather than code edits, and record in `.seo/` what's platform-limited.
