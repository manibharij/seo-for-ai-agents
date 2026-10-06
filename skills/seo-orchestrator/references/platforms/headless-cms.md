# Platforms: headless CMSs

Read this when the front end is a framework (usually Next.js, Nuxt, Astro or SvelteKit) and the content comes from a headless CMS: Contentful, Sanity, Strapi, Storyblok, Payload or similar. Two systems share each fix. The CMS holds the values, and the front end decides whether those values ever reach the served HTML. Most headless SEO bugs live in the gap between them. Facts verified 2026-10 against each vendor's docs and the Next.js docs.

---

## Detection

There is no reliable served-HTML signal for a headless CMS. Look in the repo:

| CMS | Typical dependencies and files |
|---|---|
| Contentful | `contentful`, `@contentful/rich-text-react-renderer`; env vars such as `CONTENTFUL_SPACE_ID` |
| Sanity | `@sanity/client`, `next-sanity`, `sanity.config.ts`, GROQ queries |
| Strapi | `@strapi/*` (in the CMS project), REST or GraphQL calls to a Strapi URL |
| Storyblok | `@storyblok/*`, `storyblok-js-client` |
| Payload | `payload`, `payload.config.ts` (often in the same Next.js app) |

Then read the front end's adapter row in `../stack-and-platform-adapters.md`. Images on a CMS CDN (`images.ctfassets.net`, `cdn.sanity.io`, `a.storyblok.com`) in the served HTML are a hint, not proof.

---

## 1. CMS fields must flow into metadata and JSON-LD

A CMS can have a perfect "SEO title" field that nothing reads. Trace each field from schema to served tag.

| Tag in the served HTML | Comes from | Typical bug |
|---|---|---|
| `<title>` | An SEO title field, falling back to the entry title | Template reads `entry.title` and ignores the SEO field |
| Meta description | An SEO description field, falling back to an excerpt | Field exists in the CMS schema but is never queried |
| Canonical | The route plus an optional override field | Override field holds a relative or staging URL |
| `noindex` | A boolean field | Field ignored, or inverted (`index: entry.noindex`) |
| Open Graph image | An image field run through the CMS image API | A signed or expiring asset URL, or a relative URL with no `metadataBase` |
| JSON-LD | The same entry data the page renders | Markup built from different fields than the visible content (for example, a price or author that is not on the page) |
| `hreflang` | The CMS locales and the slug of each translation | Alternates point to locales that do not exist for that entry |

In Next.js App Router, query the fields in `generateMetadata` and in the page from the same cached fetch, so the title, the JSON-LD and the visible content cannot disagree:

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next'
import { getPost } from '@/lib/cms' // one cached fetch used by both functions

export async function generateMetadata(
  { params }: { params: Promise<{ slug: string }> }
): Promise<Metadata> {
  const { slug } = await params
  const post = await getPost(slug)
  return {
    title: post.seoTitle ?? post.title,
    description: post.seoDescription ?? post.excerpt,
    alternates: { canonical: post.canonicalOverride ?? `/blog/${slug}` },
    robots: post.noindex ? { index: false, follow: true } : undefined,
  }
}
```

Missing fields are a content task, not a code task. If authors, dates or reviews are missing in the CMS, flag them for a person. Never fill them with invented values.

---

## 2. Preview and draft URLs can leak

Every CMS offers a way to see unpublished content, and each one can expose drafts to crawlers if it is wired carelessly.

- **Contentful:** the Content Preview API (`preview.contentful.com`, with a preview token) returns drafts; the Delivery API (`cdn.contentful.com`) returns published content. A production build using the preview token serves drafts to everyone.
- **Sanity:** queries take a perspective: `published`, `drafts` or `raw`. Since API version `2025-02-19` the default is `published`; older API versions default to `raw`, which includes drafts. Pin the API version and set the perspective explicitly.
- **Storyblok:** the Visual Editor loads your real site in an iframe with `_storyblok` query parameters and needs the draft version. If production fetches `version: 'draft'`, or accepts the preview token publicly, drafts go live.
- **Strapi 5:** the Preview feature builds a URL to your front end with a `status` of draft or published, guarded by a `PREVIEW_SECRET` and `allowedOrigins`.
- **Payload:** drafts and live preview are enabled per collection; the front end decides which version it queries.

**Front-end side (Next.js):** use Draft Mode. `draftMode().enable()` in a route handler sets a `__prerender_bypass` cookie, and only requests with that cookie see drafts. Check the secret before enabling it, and never link to the enable route from public pages.

**What leaks look like in an audit:**
- Preview hostnames (`preview.example.com`, a Vercel preview deployment, a CMS-hosted preview) that are indexable. They should send `noindex` (an `X-Robots-Tag: noindex` header is simplest) or sit behind authentication.
- URLs with `?_storyblok=`, `?preview=` or similar parameters in the index or in internal links.
- Draft-only pages appearing in the sitemap, because the sitemap queries a different perspective from the pages.

---

## 3. "Fixed in the CMS" is not "served"

An editor changes a title, sees it in the CMS, and reports it fixed. The live page may not change for minutes, hours, or ever, depending on how the front end builds.

| Front-end build model | When a CMS change reaches the live HTML |
|---|---|
| Static build (SSG, `output: 'export'`, Astro static) | Only after a full rebuild and deploy. Needs a CMS webhook that triggers the deploy |
| Time-based ISR (`export const revalidate = 3600` in Next.js) | After the window expires **and** a request arrives; the first visitor after expiry still gets the stale page while it regenerates |
| On-demand revalidation | When a CMS webhook calls a route handler that runs `revalidatePath('/blog/slug')` or `revalidateTag('posts', 'max')` (Next.js 16 signature) |
| Fully dynamic SSR | On the next request, subject to CDN caching |
| Any of the above behind a CDN | Also after the CDN entry expires or is purged |

A minimal webhook receiver in Next.js App Router:

```ts
// app/api/revalidate/route.ts
import { revalidatePath } from 'next/cache'

export async function POST(request: Request) {
  if (request.headers.get('x-webhook-secret') !== process.env.REVALIDATE_SECRET) {
    return new Response('Unauthorised', { status: 401 })
  }
  const { slug } = await request.json()
  revalidatePath(`/blog/${slug}`)
  revalidatePath('/blog') // the listing page that links to it
  return Response.json({ revalidated: true })
}
```

Points to check, from the Next.js docs:
- `revalidatePath` invalidates; the page regenerates on the **next request**, not immediately.
- Revalidate the exact public path. `proxy.ts` (formerly `middleware.ts`) does not run for on-demand revalidation, so rewrites are not applied.
- With several self-hosted instances, the default file-system cache is per instance, and a revalidation call only clears the instance that receives it. A shared cache handler fixes this.
- Revalidate the sitemap, listing pages and any page that shows the changed entry (cards, related posts), not just the entry's own page.
- The `x-nextjs-cache` response header shows `HIT`, `STALE`, `MISS` or `REVALIDATED`.

Webhooks fail silently: a wrong secret, a changed URL, a CMS environment that is not the production one. When a fix "did not take", check the CMS webhook log before anything else.

---

## 4. Always verify on the live URL

The only proof is the served HTML of the production URL.

```bash
URL="https://www.example.com/blog/slug"
curl -sIL "$URL" | grep -iE "^(age|cache-control|x-nextjs-cache|x-vercel-cache|cf-cache-status):"
curl -sL "$URL" | grep -oiE '<title>[^<]*</title>|<meta[^>]+name="description"[^>]*>|<link[^>]+rel=.canonical.[^>]*>|<meta[^>]+name="robots"[^>]*>'
```
```powershell
$URL = "https://www.example.com/blog/slug"
$r = Invoke-WebRequest -Uri $URL -UseBasicParsing
$r.Headers.GetEnumerator() | Where-Object { $_.Key -match '^(age|cache-control|x-nextjs-cache|x-vercel-cache|cf-cache-status)$' }
[regex]::Matches($r.Content, '<title>[^<]*</title>|<meta[^>]+name="description"[^>]*>|<link[^>]+rel=.canonical.[^>]*>|<meta[^>]+name="robots"[^>]*>') | ForEach-Object Value
```

If the old value is still served, read the cache headers: a `HIT` or a large `Age` means the change has not propagated. Request the URL a second time after a `STALE` response. Do not mark a finding `fixed` until the new value is in the served HTML.

---

## Giving instructions when you cannot edit code

Split each finding by owner: the CMS editor changes the field; the developer changes the template or the webhook. Say which.

```text
Finding: /blog/pricing-guide serves the title "Untitled" because the SEO title field is empty
         and the template has no fallback to the entry title.
Editor (now): Contentful > Blog post "Pricing guide" > SEO title: "How we price our plans", then Publish.
Developer (later): in app/blog/[slug]/page.tsx, fall back to post.title when seoTitle is empty.
Check: after publishing, the live page may take up to the revalidation window to change.
       Tell me when it is published and I will re-fetch the live URL.
```

---

## Related
- Front-end rendering and Reach: `1-reach-indexation/references/rendering-ssr-csr.md`, `1-reach-indexation/references/javascript-seo.md`.
- Per-framework metadata patterns: `2-read-content/references/metadata-titles-descriptions.md`.
- Honest JSON-LD built from page data: `3-understand-schema/references/schema-types-and-jsonld.md`.
