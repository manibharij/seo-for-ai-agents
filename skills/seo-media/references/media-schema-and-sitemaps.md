# Media schema, sitemaps and checks

Read this for the patterns. Every value must mirror **real, on-page** media: never fabricate a transcript, duration, upload date, creator or licence. Render markup server-side so it is in the served HTML. Facts about people and rights come only from `[established]` entries in `.seo/context.md` or from the media's own source.

Google facts in this file were checked against Google Search Central in October 2026 (verified 2026-10). Sources are listed at the end. Re-check them before promising a result: these features change.

---

## Watch pages: the rule that decides video indexing

Google indexes a video only when it is on a **watch page**: a page whose main purpose is to show one video, where the main reason a visitor comes is to watch it. Google's Video indexing report help gives these as examples of pages that are **not** watch pages:
- a blog post where the video complements the text;
- a product page with a complementary video;
- a category page listing several videos of equal prominence.

Google also says the watch page itself must be indexed and performing in Search before its video is considered.

What this means in practice:
- **Do not add `VideoObject` to every page that embeds a player.** On a supplementary page the markup will not earn a video result, and spreading it adds maintenance with no payoff.
- **Give each important video one watch page** (for example `/videos/fitting-a-tap`) with the player near the top, a title and description about the video, and the transcript. Mark that page up.
- Keep supplementary embeds where they help readers, and link them to the watch page.
- Creating watch pages means new URLs and new content. Propose it as a `needs-human` finding unless the user has asked for it.

## VideoObject (JSON-LD)

Google's required properties are `name`, `thumbnailUrl` and `uploadDate`. Recommended: `description`, `duration`, `contentUrl` (the video file, preferred) or `embedUrl` (the player), plus `hasPart` for clips.

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "How to fit a mixer tap",
  "description": "A plumber fits a mixer tap to a kitchen sink, from isolating the water to testing for leaks.",
  "thumbnailUrl": ["https://example.com/videos/fitting-a-tap/thumb-1200.jpg"],
  "uploadDate": "2026-05-20T09:00:00+01:00",
  "duration": "PT8M30S",
  "contentUrl": "https://cdn.example.com/video/fitting-a-tap.mp4",
  "embedUrl": "https://example.com/embed/fitting-a-tap"
}
```
- `duration` is ISO 8601 (`PT8M30S` is 8 minutes 30 seconds). `uploadDate` is the real date, ideally with a time zone.
- `name` and `description` should be unique per video.
- For embedded YouTube or Vimeo, describe the embedded video accurately; values must still be true. Take `uploadDate` and `duration` from the platform, not from a guess.
- `transcript` (text) is allowed on `VideoObject`; the bigger win is the transcript visible on the page.

## Key moments: `Clip` and `SeekToAction`

Key moments let Google link to points inside a video. Use them only when the video has real chapters a viewer would use.

**`Clip`: you name each segment.** Required per clip: `name`, `startOffset` (seconds) and `url` (a URL that starts playback at that point). `endOffset` is recommended. No two clips of the same video on a page may share a start time.

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "How to fit a mixer tap",
  "thumbnailUrl": ["https://example.com/videos/fitting-a-tap/thumb-1200.jpg"],
  "uploadDate": "2026-05-20T09:00:00+01:00",
  "contentUrl": "https://cdn.example.com/video/fitting-a-tap.mp4",
  "hasPart": [
    { "@type": "Clip", "name": "Isolate the water", "startOffset": 0, "endOffset": 75,
      "url": "https://example.com/videos/fitting-a-tap?t=0" },
    { "@type": "Clip", "name": "Remove the old tap", "startOffset": 75, "endOffset": 260,
      "url": "https://example.com/videos/fitting-a-tap?t=75" },
    { "@type": "Clip", "name": "Test for leaks", "startOffset": 430, "endOffset": 510,
      "url": "https://example.com/videos/fitting-a-tap?t=430" }
  ]
}
```
The `?t=` URLs must really start playback at that second. If your player ignores the parameter, fix the player first.

**`SeekToAction`: Google finds the segments.** You tell Google where the timestamp goes in your URL, and it identifies key moments itself. Google must be able to fetch the video file, and the feature supports a limited set of languages (listed in Google's video structured data docs).

```json
"potentialAction": {
  "@type": "SeekToAction",
  "target": "https://example.com/videos/fitting-a-tap?t={seek_to_second_number}",
  "startOffset-input": "required name=seek_to_second_number"
}
```
`startOffset-input` must be exactly that string.

**YouTube-hosted video:** put timestamps and labels in the YouTube description. Google can also detect segments automatically.

## Transcripts and captions

Spoken content is invisible to engines until it is text. A real transcript:
- turns the video's content into indexable, quotable text that answer engines can cite;
- helps people who cannot or prefer not to listen.

Put the transcript in the served HTML. A collapsed `<details>` element is fine; a button that fetches the text on click is not. If no transcript exists, the task is to **produce accurate captions or a transcript** (a tool or human step) and then add them. Do not write one from memory or guess the content.

## Thumbnails and fetchability
- Use a real frame or designed thumbnail at a stable URL. Google reads thumbnails from `thumbnailUrl`, the `<video poster>` attribute, `<video:thumbnail_loc>` or `og:video:image`.
- Do not block the video file or thumbnail with `robots.txt` or `noindex`, and keep the file at a stable URL (signed URLs that expire in minutes defeat `contentUrl`).

## Video sitemaps

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  <url>
    <loc>https://example.com/videos/fitting-a-tap</loc>
    <video:video>
      <video:thumbnail_loc>https://example.com/videos/fitting-a-tap/thumb-1200.jpg</video:thumbnail_loc>
      <video:title>How to fit a mixer tap</video:title>
      <video:description>A plumber fits a mixer tap to a kitchen sink, from isolating the water to testing for leaks.</video:description>
      <video:content_loc>https://cdn.example.com/video/fitting-a-tap.mp4</video:content_loc>
      <video:duration>510</video:duration>
    </video:video>
  </url>
</urlset>
```
The `<urlset>` **must declare the video namespace** or the entries are ignored. Google requires `video:thumbnail_loc`, `video:title`, `video:description`, and at least one of `video:content_loc` (the file) or `video:player_loc` (the player). `<loc>` is the watch page. Values must match the `VideoObject` and the real video.

In Next.js App Router, `app/sitemap.ts` supports a `videos` array (`title`, `thumbnail_loc`, `description`, plus optional `content_loc`, `player_loc`, `duration` and more):

```ts
// app/sitemap.ts
import type { MetadataRoute } from 'next'
import { getVideos } from '@/lib/videos'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const videos = await getVideos()
  return videos.map((v) => ({
    url: `https://example.com/videos/${v.slug}`,
    lastModified: v.updatedAt,
    videos: [{
      title: v.title,
      thumbnail_loc: v.thumbnailUrl,
      description: v.description,
      content_loc: v.fileUrl,
      duration: v.durationSeconds,
    }],
  }))
}
```

## Image sitemaps

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://example.com/products/widget</loc>
    <image:image>
      <image:loc>https://example.com/img/widget.webp</image:loc>
    </image:image>
  </url>
</urlset>
```
The enclosing `<urlset>` **must declare the image namespace** (`xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"`); without it Google silently ignores the `image:` entries. List only real, `200` images that matter (product shots, key illustrations), not every icon. In Next.js, each `app/sitemap.ts` entry takes an `images: string[]` array and Next.js adds the namespace.

## Image fundamentals (overlaps the Read rung)
- Descriptive `alt` for meaningful images, `alt=""` for decorative ones; descriptive filenames where you control them.
- Use `<img>` or `<picture>`: Google does not index CSS background images. Google Images supports BMP, GIF, JPEG, PNG, WebP, SVG and AVIF.
- Modern formats, correct sizes, `width`/`height` set. Next.js: `next/image`.
- Do not block image paths in `robots.txt` if you want them indexed.

## The LCP image: do not lazy-load the hero

Lazy-loading tells the browser to wait until an image nears the viewport. For the hero image, that wait delays Largest Contentful Paint. web.dev's guidance is direct: never lazy-load the LCP image, and add `fetchpriority="high"` to it.

```html
<img src="/img/hero-1600.avif" alt="Plumber fitting a chrome mixer tap"
     width="1600" height="900" fetchpriority="high">
```

`next/image` defaults to `loading="lazy"`, so the hero needs an explicit setting. In Next.js 16, set `loading="eager"` and add `fetchPriority="high"`. `fetchPriority` on its own leaves the default `loading="lazy"` in place. The Next.js docs prefer these two over the `preload` prop in most cases, and `priority` is deprecated:

```tsx
import Image from 'next/image'

<Image src="/img/hero-1600.avif" alt="Plumber fitting a chrome mixer tap"
       width={1600} height={900} loading="eager" fetchPriority="high" />
```
Lazy-load everything else below the fold. Speed work beyond this one image belongs to `seo-performance`.

## Large previews for Discover

Google Discover can show a large image when the page allows it with `max-image-preview:large` (or uses AMP), and the image is at least 1200 px wide. Google advises against generic images such as the site logo in `og:image` or schema markup.

```html
<meta name="robots" content="max-image-preview:large">
```
Next.js App Router, in the root layout:

```ts
export const metadata: Metadata = {
  robots: { googleBot: { 'max-image-preview': 'large' } },
}
```
This only allows a large preview. It does not put a page into Discover.

## Image licence metadata

For sites that license images (photographers, stock libraries, publishers selling rights), licence metadata can show licence details in Google Images, and `license` makes the image eligible for the Licensable badge. Google requires `contentUrl` plus at least one of `creator`, `creditText`, `copyrightNotice` or `license`; `acquireLicensePage` is recommended.

```json
{
  "@context": "https://schema.org",
  "@type": "ImageObject",
  "contentUrl": "https://example.com/photos/harbour-dawn.jpg",
  "license": "https://example.com/licensing/standard",
  "acquireLicensePage": "https://example.com/licensing/buy?photo=harbour-dawn",
  "creditText": "Example Studio",
  "creator": { "@type": "Person", "name": "A. Photographer" },
  "copyrightNotice": "© Example Studio"
}
```
The alternative is IPTC photo metadata embedded in the file (Web Statement of Rights for `license`, Licensor URL for `acquireLicensePage`, plus Creator, Credit Line and Copyright Notice). Every value here is a legal claim: take it only from `[established]` context or the rights holder's records, and raise `needs-human` when it is missing.

## Find images without alt text in the built HTML

Build the site, then scan the HTML output. Common output folders: `out/` (Next.js static export), `.next/server/app/` (Next.js prerendered pages), `dist/` (Vite, Astro, VitePress), `build/` (Docusaurus). These commands list `<img>` tags with **no** `alt` attribute. `alt=""` is treated as present, because it is correct for decorative images; review those by hand.

```bash
# GNU grep (Linux, WSL, Git Bash). Handles <img> tags split across lines.
DIR=out
grep -rioz --include='*.html' '<img[^>]*>' "$DIR" \
  | tr '\n\0' ' \n' \
  | grep -Eiv '[[:space:]]alt([[:space:]]*=|[[:space:]/>])'
```
```powershell
$dir = "out"
Get-ChildItem $dir -Recurse -Filter *.html | ForEach-Object {
  $file = $_.FullName
  [regex]::Matches((Get-Content $file -Raw), '<img\b[^>]*>', 'IgnoreCase') |
    Where-Object { $_.Value -notmatch '\salt(\s*=|[\s/>])' } |
    ForEach-Object { "{0}: {1}" -f $file, ($_.Value -replace '\s+', ' ') }
}
```
Dynamic routes are not in the build output. Check them on the served page instead, for example `curl -s https://example.com/page > page.html`, then run the same command on that file's folder.

To list empty `alt` values for review: `grep -rio --include='*.html' '<img[^>]*alt=""[^>]*>' "$DIR"`.

---

## Worked example: a plumbing firm's video and images

**Situation.** A Next.js App Router site has 12 how-to videos, each embedded in a long blog post. Every post carries `VideoObject`. None has a transcript. The homepage hero is a `next/image` with no loading setting.

**Diagnose (served output).**
- `curl -s https://example.com/blog/fitting-a-mixer-tap` shows `VideoObject` in the raw HTML, but the video sits under 1,800 words of text. By Google's definition this is a supplementary video, not a watch page.
- The homepage hero renders as `<img loading="lazy" ...>`.
- The missing-alt scan of `.next/server/app/` lists 31 `<img>` tags without `alt`, all from one `Gallery` component.

**Findings (shared schema).**
```yaml
- id: media-blog-videos-not-on-watch-pages
  skill: seo-media
  area: media
  target: /blog/* (video posts)
  severity: high
  evidence: "curl: VideoObject on 12 blog posts; video is supplementary to long text, so not a watch page"
  fix: "Create /videos/<slug> watch pages with player, description and transcript; move VideoObject there; link from posts"
  risk: medium (12 new URLs; needs sign-off)
  status: needs-human
  verified: 2026-10-06
  notes: "Transcripts do not exist yet; captions must be produced first"
- id: media-home-hero-lazy-loaded
  skill: seo-media
  area: media
  target: / (hero)
  severity: medium
  evidence: "curl: hero <img> has loading=\"lazy\""
  fix: "Set loading=\"eager\" and fetchPriority=\"high\" on the hero next/image"
  risk: low
  status: fixed
  verified: 2026-10-06
  notes: ""
- id: media-gallery-missing-alt
  skill: seo-media
  area: media
  target: pages using the Gallery component (/projects/*)
  severity: medium
  evidence: "alt scan of .next/server/app: 31 <img> tags without alt"
  fix: "Pass the CMS caption as alt; alt=\"\" for decorative thumbnails"
  risk: low
  status: fixed
  verified: 2026-10-06
  notes: ""
```

**Fix.** Add `loading="eager"` and `fetchPriority="high"` to the hero. Make `Gallery` require an `alt` prop and feed it from the CMS caption. Propose the watch pages, and once approved, build `app/videos/[slug]/page.tsx` that renders the player, the transcript in a `<details>` element, and `VideoObject` with `Clip` entries for the chapters the plumber already names in the video. Add the `videos` array to `app/sitemap.ts`. Leave the blog embeds in place, drop their `VideoObject`, and link each to its watch page.

**Verify.** Re-run the alt scan (zero results). `curl` the homepage and confirm `fetchpriority="high"` and no `loading="lazy"` on the hero. `curl` a watch page and confirm `VideoObject` and the transcript are in the raw HTML. Fetch `/sitemap.xml` and confirm the `video` namespace and entries. Validate the markup.

**Report.** "Your videos were inside long articles, so Google treated them as extras and did not index them as videos. I've proposed one page per video; that needs your approval and real transcripts. The homepage image was set to load late, which slows the first view; it now loads first. 31 gallery images had no description; they now use your captions."

---

## Verify on the served output
- `alt` present on meaningful images (missing-alt scan returns nothing unexpected).
- LCP image: no `loading="lazy"`, has `fetchpriority="high"`.
- `VideoObject` in the **raw** served HTML of watch pages only, and **honest** (every value matches the real media).
- `Clip` URLs start playback at the stated second; `SeekToAction` target pattern works.
- Transcript or captions are real text in the served output.
- Image and video sitemaps reachable, namespaced, listing real `200` URLs that match the markup.
- `max-image-preview:large` present where intended.
- Licence metadata values match the rights holder's records.
- Validate with an MCP validator or Google's per-feature requirements; report eligibility, never guaranteed display.
- Media-bearing pages are not client-only shells.

## Sources (verified 2026-10)
- Video SEO best practices: https://developers.google.com/search/docs/appearance/video
- Video indexing report, watch-page definition: https://support.google.com/webmasters/answer/9495631
- Video structured data, `Clip`, `SeekToAction`: https://developers.google.com/search/docs/appearance/structured-data/video
- Video sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps
- Image SEO best practices: https://developers.google.com/search/docs/appearance/google-images
- Image licence metadata: https://developers.google.com/search/docs/appearance/structured-data/image-license-metadata
- Discover: https://developers.google.com/search/docs/appearance/google-discover
- LCP and lazy-loading: https://web.dev/articles/optimize-lcp and https://web.dev/articles/lcp-lazy-loading
- Next.js `next/image` and `sitemap.ts`: https://nextjs.org/docs/app/api-reference/components/image and https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap
