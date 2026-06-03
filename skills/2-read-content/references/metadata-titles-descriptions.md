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

### Other frameworks (brief)
- **Astro:** set `<title>`/`<meta>` in the layout `<head>`, usually via props/frontmatter.
- **Nuxt:** `useHead()` / `definePageMeta`.
- **SvelteKit:** `<svelte:head>` in the page/layout.
- **Remix:** the route `meta` export.

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
