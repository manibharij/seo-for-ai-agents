# Metadata: titles, descriptions, alt text, Open Graph

Read this for the metadata half of Read — the signals that control how a page is understood and how it appears in results. All of it must be verified in the **served HTML**, because metadata is the single easiest thing to set in source and have silently overridden at render time.

---

## The `<title>` — the most important single tag on the page

- **Unique per page.** Duplicate titles make results indistinguishable and waste the strongest on-page signal.
- **Descriptive and front-loaded.** Put the distinctive words first; truncation eats the end (~50–60 characters show in most results).
- **Pattern:** `Specific page subject | Brand`. Keep the brand short and at the end.
- The title tag (what's in `<head>`) is what search uses; it need not match the on-page `<h1>` word-for-word, but they should agree on the subject.

## The meta description — your snippet pitch

- Not a direct ranking factor, **but** it is frequently the snippet under your link, so it drives click-through.
- **Unique per page**, ~150–160 characters, an accurate and inviting summary of the page. Engines may rewrite it, but a good one is often kept.
- Don't keyword-stuff; write it for a human deciding whether to click.

## `<html lang>` and other basics
- Set `<html lang="en-GB">` (or the correct locale). It helps engines and assistive tech and is trivial to get right.
- Ensure a single, correct `<meta charset="utf-8">` and a `<meta name="viewport">` (the latter matters for correct mobile rendering and usability — Google indexes mobile-first, so a page that renders badly on mobile is a real problem).

## Image `alt` text
- **Meaningful images:** descriptive `alt` that conveys the image's content/purpose ("Bar chart: revenue up 40% in 2025"). This serves accessibility and image search alike.
- **Decorative images:** empty `alt=""` so assistive tech and engines skip them. Do not omit the attribute entirely.
- Don't keyword-stuff alt text; describe the image.

## Open Graph & Twitter Cards (secondary, cheap, worth it)
- `og:title`, `og:description`, `og:image`, `og:url`, `og:type`, and `twitter:card` control how links look when shared. Not a ranking factor, but they affect click-through from social and messaging.

---

## Next.js App Router — the Metadata API (your stack)

Next renders metadata into the served HTML for you **if** you use the Metadata API correctly. The common bugs are: setting `<title>` manually in a component (fights the framework), or expecting a child to set metadata when a parent layout already fixed it.

### Static metadata (fixed pages)
```tsx
// app/about/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About us',                         // becomes "About us | Brand" via the template below
  description: 'Who we are and what we do — a clear, unique ~155-char summary.',
}
```

### A title template + defaults in the root layout
```tsx
// app/layout.tsx
export const metadata: Metadata = {
  title: {
    default: 'Brand — what you do',          // used when a page sets no title
    template: '%s | Brand',                  // child titles slot into %s
  },
  description: 'Site-wide default description.',
  metadataBase: new URL('https://example.com'),  // makes og/canonical URLs absolute
  openGraph: { type: 'website', siteName: 'Brand' },
}
```

### Dynamic metadata (data-driven routes)
```tsx
// app/blog/[slug]/page.tsx
// Next.js 15+: params is a Promise and must be awaited (Next 14 passed it synchronously).
export async function generateMetadata(
  { params }: { params: Promise<{ slug: string }> }
): Promise<Metadata> {
  const { slug } = await params
  const post = await getPost(slug)
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: { title: post.title, description: post.excerpt, images: [post.ogImage] },
    alternates: { canonical: `/blog/${post.slug}` },   // canonical strategy is rung 4
  }
}
```

Notes:
- `metadataBase` is needed for absolute `og:image`/canonical URLs — without it you get warnings and relative URLs.
- A child page's metadata **merges with and overrides** its ancestors. If a page shows the wrong title, look up the layout chain.
- Don't hand-write `<title>`/`<meta>` in JSX alongside the Metadata API; pick the API.
- `title.template` applies to **child** segments only. A template in `app/layout.tsx` does not apply to the title set in `app/page.tsx` (same segment), so the home page title is used exactly as written.
- Since Next.js 15.2, `generateMetadata` may stream: for clients that run JavaScript the tags can be appended to `<body>`, while HTML-only bots get them in `<head>`. If a non-Google crawler matters and is not on Next.js's `htmlLimitedBots` list, check what it receives, and set `htmlLimitedBots` in `next.config` if needed.

---

## Per-framework metadata patterns

Each cell is where that tag comes from in the framework's idiomatic setup. Whatever the framework, the tag only counts if it is in the served HTML, so the framework must render on the server (see `1-reach-indexation/references/rendering-ssr-csr.md`). Verified 2026-10 against each framework's docs.

| Framework | Title template | Canonical | Open Graph | JSON-LD injection | Robots `noindex` | `hreflang` |
|---|---|---|---|---|---|---|
| **Next.js App Router** | Root layout `title: { template: '%s \| Brand', default: 'Brand' }`; pages set `title`; `title.absolute` skips the template | `alternates: { canonical: '/path' }` with `metadataBase` in the root layout | `openGraph: { ... }` (a page's object **replaces** the parent's whole object) | Native `<script type="application/ld+json">` in a page or layout, `JSON.stringify(data).replace(/</g, '\\u003c')` | `robots: { index: false, follow: true }` | `alternates: { languages: { 'en-GB': '/en-gb/page', 'de-DE': '/de/page' } }` |
| **Nuxt** | `titleTemplate: '%s \| Brand'` in `app.vue` (`useHead`) or `app.head` in `nuxt.config`; pages set `title` with `useSeoMeta` or `definePageMeta` | `useHead({ link: [{ rel: 'canonical', href }] })` (`useSeoMeta` does not handle links) | `useSeoMeta({ ogTitle, ogDescription, ogImage })` | `useHead({ script: [{ type: 'application/ld+json', innerHTML: JSON.stringify(data) }] })` | `useSeoMeta({ robots: 'noindex, follow' })` | `@nuxtjs/i18n` `useLocaleHead()` (needs `baseUrl`), or `useHead` links |
| **SvelteKit** | No built-in template. Return SEO fields from `load`, render them once in the root `+layout.svelte` `<svelte:head>` (the pattern SvelteKit's SEO docs recommend) | `<link rel="canonical" href={...}>` in `<svelte:head>` | `<meta property="og:...">` in `<svelte:head>` | `{@html}` of a `<script type="application/ld+json">` string inside `<svelte:head>`, with `<` escaped | `<meta name="robots" content="noindex">` in `<svelte:head>` | `<link rel="alternate" hreflang="..." href="...">` in `<svelte:head>` |
| **Astro** | A layout component takes a `title` prop and renders ``<title>{`${title} \| Brand`}</title>`` | `<link rel="canonical" href={new URL(Astro.url.pathname, Astro.site)} />` (needs `site`) | `<meta property="og:...">` in the layout head, from props | `<script type="application/ld+json" set:html={JSON.stringify(data)} />` (escape `<` yourself) | A `noindex` prop that renders the robots meta | Manual `<link rel="alternate">`; the `astro:i18n` helpers (such as `getAbsoluteLocaleUrl`) build the URLs |
| **React Router framework mode / Remix** | No template: a child route's `meta` **replaces** the parent's array. Build titles with a shared helper, or use React 19 `<title>` in the component (now recommended by the docs) | `{ tagName: 'link', rel: 'canonical', href }` in `meta`, the `links` export, or a `<link>` rendered in the component | `{ property: 'og:title', content }` in `meta` | `{ 'script:ld+json': data }` in `meta` (React Router escapes it) | `{ name: 'robots', content: 'noindex' }` in `meta` | `{ tagName: 'link', rel: 'alternate', hrefLang: 'de', href }` in `meta` |
| **Angular** | Route `title`, plus a custom `TitleStrategy` for `%s \| Brand` | No built-in: create or update the `<link>` through `DOCUMENT` in a service | `Meta.updateTag({ property: 'og:title', content })` | Append a `<script type="application/ld+json">` through `DOCUMENT` during server rendering | `Meta.updateTag({ name: 'robots', content: 'noindex' })` | Manual `<link rel="alternate">` through `DOCUMENT` |

React Router v8 renamed the `data` argument of `meta` to `loaderData`; v7 code reading `data` breaks on upgrade. Angular head changes reach the served HTML only with `@angular/ssr` or prerendering; otherwise they happen in the browser.

**Other stacks, briefly:**
- **TanStack Start:** the route `head()` option returns `meta`, `links` and `scripts`, rendered by `<HeadContent />` in the root. Nested routes win: a child's `title`, or a meta tag with the same `name` or `property`, overrides the parent's.
- **SolidStart:** `<Title>`, `<Meta>` and `<Link>` from `@solidjs/meta` inside routes, defaults in `root.tsx`. Wrap `<Title>` in a component to add the brand suffix.
- **Qwik City:** `export const head: DocumentHead` per route; a layout's `head` can be a function that receives the page's `head` and changes it (for example, to append the brand).
- **Docs generators:** front matter `title` and `description` in Docusaurus, VitePress and Starlight; the generator applies the site template.

---

## Classic override bugs

These survive code review because each file looks right on its own. Find them in the served HTML.

1. **The layout title wins.** A page sets no title and inherits the layout's, so every page in a section shares one title. In React Router a route without a `meta` export inherits its parent's; in Next.js a page with no `title` gets the nearest `title.default`. Also: a client component that sets `document.title` after hydration, so crawlers that read the raw HTML see the layout title.
2. **Two `<title>` elements.** A title in the layout's `<svelte:head>` and another in the page's can both reach the server HTML; the same happens when an Astro page adds a title to a layout that already prints one. Render the title in one place.
3. **Every page canonicalises to the home page.** `alternates: { canonical: '/' }` in the Next.js root layout is inherited by every page that does not set its own `alternates`. The same happens with a hard-coded canonical in an SPA's `index.html`. Set canonicals per page, derived from the route.
4. **Duplicate canonicals from layout and page.** The layout hand-writes a `<link rel="canonical">` and the page sets one through the framework API; or a theme and an SEO plugin both print one; or a tag manager injects one on top of the platform's. With conflicting canonicals, search engines may ignore them all.
5. **Open Graph replaced wholesale.** In Next.js, a page that sets `openGraph: { title }` drops the layout's `og:image` and `og:description` (shallow merge). In React Router, a child `meta` drops every parent tag. Share common fields through a helper and spread them in.
6. **A staging `noindex` in a shared layout** that ships to production. Check the robots meta on every template after launch.

```bash
curl -sL https://example.com/page | grep -oiE '<title[^>]*>|<link[^>]+rel=.canonical.[^>]*>|<meta[^>]+name="robots"[^>]*>' | sort | uniq -c
```
```powershell
$h = (Invoke-WebRequest -Uri "https://example.com/page" -UseBasicParsing).Content
[regex]::Matches($h, '(?i)<title[^>]*>|<link[^>]+rel=.canonical.[^>]*>|<meta[^>]+name="robots"[^>]*>') | Group-Object Value | Select-Object Count, Name
```

A count above 1 for `<title` or for the canonical is a finding.

---

## Verifying metadata on the rendered output

The whole point — confirm it is in what is *served*, per template:

```bash
curl -sL https://example.com/page | grep -iE "<title>|name=\"description\"|<html"
```
```powershell
$h = Invoke-WebRequest -Uri "https://example.com/page" -UseBasicParsing
$h.Content | Select-String -Pattern "<title>|name=`"description`"|<html "
```

Confirm in the served HTML:
- [ ] `<title>` present, unique, descriptive, front-loaded.
- [ ] `<meta name="description">` present, unique, accurate, ~150–160 chars.
- [ ] `<html lang>` set.
- [ ] Meaningful images carry descriptive `alt`; decorative ones use `alt=""`.
- [ ] Open Graph tags present (if you added them) with an absolute `og:image`.
- [ ] No two tested templates share the same title or description.

A Lighthouse/PageSpeed MCP's SEO audit confirms title/description presence and alt coverage in one pass — use it if available, but the served-HTML check above is sufficient on its own.
