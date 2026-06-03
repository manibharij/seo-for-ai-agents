# Media schema & sitemaps

Read this for the patterns. Every value must mirror **real, on-page** media — never fabricate a transcript, duration, or upload date. Render markup server-side so it's in the served HTML.

---

## VideoObject (JSON-LD)

For a real video on the page:

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Exact video title shown on the page",
  "description": "Accurate description of the video's content.",
  "thumbnailUrl": ["https://example.com/thumb.jpg"],
  "uploadDate": "2026-05-20",
  "duration": "PT8M30S",
  "contentUrl": "https://example.com/video.mp4",
  "embedUrl": "https://example.com/embed/abc"
}
```
- `duration` is ISO 8601 (`PT8M30S` = 8 min 30 s). `uploadDate` is a real date.
- Provide `contentUrl` (the file) and/or `embedUrl` (the player).
- For embedded YouTube/Vimeo, describe the embedded video accurately; values must still be true.
- Optional but valuable: `transcript` (text), `hasPart`/`Clip` for key moments (only if real).
- **Never** mark up a video that isn't on the page, or invent duration/date/thumbnail.

## Transcripts & captions — the highest-value media SEO move
Spoken content is invisible to engines until it's text. A real transcript or captions:
- Turns the video's content into **indexable, citable** text (also a strong AEO signal — answer engines can quote it).
- Improves accessibility (a genuine win in its own right).
Put the transcript in the served HTML (collapsible is fine, but in the DOM, not behind a click that injects it client-side). If no transcript exists, the task is to **generate accurate captions/transcript** (a tool/human step) and then add them — do **not** fabricate a transcript.

## Image sitemaps
Help important images get discovered. Either a dedicated image sitemap or `image:` extensions in your sitemap entries:

```xml
<url>
  <loc>https://example.com/products/widget</loc>
  <image:image>
    <image:loc>https://example.com/img/widget.webp</image:loc>
  </image:image>
</url>
```
List only real, `200` images that matter (product shots, key illustrations) — not every icon. In Next.js you can extend `app/sitemap.ts` to include image entries.

## Video sitemaps
For important self-hosted video, a video sitemap entry exposes the metadata to Google:

```xml
<url>
  <loc>https://example.com/watch/intro</loc>
  <video:video>
    <video:thumbnail_loc>https://example.com/thumb.jpg</video:thumbnail_loc>
    <video:title>Exact video title</video:title>
    <video:description>Accurate description.</video:description>
    <video:content_loc>https://example.com/video.mp4</video:content_loc>
  </video:video>
</url>
```
Values must match the `VideoObject` and the real video.

## Image fundamentals (overlaps the Read rung's page-experience)
- Descriptive `alt` (meaningful) / `alt=""` (decorative); descriptive filenames where you control them.
- Modern formats (WebP/AVIF), correct sizes, lazy-load below the fold, width/height set (CLS). Next.js: `next/image`.
- Don't block image paths in `robots.txt` if you want them indexed.

---

## Verify on the served output
- `alt` present on meaningful images; `VideoObject` JSON-LD in the **raw** served HTML and **honest** (every value matches the real media).
- Transcript/captions are real text in the served output.
- Image/video sitemap reachable; lists real `200` media URLs that match the markup.
- Validate `VideoObject` (MCP validator or Google's video structured-data requirements); report eligibility, never guaranteed display.
- Media-bearing pages aren't client-only shells (media present before JS runs).
