---
name: seo-media
description: >-
  Make images and video discoverable and indexable — descriptive alt and filenames,
  modern formats and sizing, image sitemaps, and for video: VideoObject schema,
  real transcripts/captions, thumbnails, and video sitemaps. Use on "image SEO",
  "video SEO", "get my videos/images in Google", "VideoObject", "image sitemap",
  "video sitemap", or "optimise media for search". Marks up only real, on-page media
  truthfully and verifies on the served output. Deepens the alt-text (Read) and
  schema (Understand) rungs for media specifically.
---

# Media SEO — images & video discoverable

A specialist skill for the media most sites under-optimise. Images and video can drive real search traffic (Google Images, video results, and as supporting signals) — but only if engines can find, fetch, and understand them. This deepens what Read (alt text) and Understand (schema) cover, focused on media. As always: mark up only **real** media, truthfully, and verify on the **served output**.

Work the four steps: **Diagnose → Fix → Verify → Report.**

---

## Step 1 — Diagnose

On the served output and asset pipeline:
- **Images:** do meaningful images have descriptive `alt`? Sensible, descriptive filenames (not `IMG_2931.jpg`)? Modern formats (WebP/AVIF) and appropriate sizes? Lazy-loaded below the fold with dimensions set (CLS)? Is there an **image sitemap** (or images included in the sitemap) for important imagery? Are images blocked in `robots.txt`?
- **Video:** is video content represented with **`VideoObject` schema** (name, description, thumbnail, uploadDate, duration, contentUrl/embedUrl)? Are there **transcripts/captions** so the spoken content is indexable text (not locked in the media)? A real, accessible **thumbnail**? A **video sitemap** for important videos? Is the video in the served HTML/markup or injected only client-side?
- **Both:** is the media actually in the **served HTML** (a gallery or player rendered only client-side is invisible to crawlers — a Reach issue for media)?

## Step 2 — Fix

Apply the safe, truthful fixes; flag anything needing real content (e.g. a transcript only a human/tool can produce accurately).

### Images
- Descriptive `alt` for meaningful images (`alt=""` for decorative) and descriptive filenames where you control them.
- Serve modern formats, correct sizes, lazy-load below-the-fold, set width/height (Next.js: `next/image`). (Overlaps the Read rung's page-experience — coordinate.)
- Add an **image sitemap** (or `image:` entries in the sitemap) for important images so they're discoverable.
- Don't block needed image paths in `robots.txt`.

### Video
- Add **`VideoObject` JSON-LD** with **real** values only: `name`, `description`, `thumbnailUrl`, `uploadDate`, `duration` (ISO 8601), and `contentUrl`/`embedUrl`. Render it server-side so it's in the served HTML.
- Surface a **real transcript or captions** — this turns spoken content into indexable, citable text (a strong AEO signal too) and aids accessibility. If no transcript exists, flag it as a task (generate captions, then add) — don't fabricate a transcript.
- Ensure a genuine, fetchable **thumbnail**.
- Add a **video sitemap** for important self-hosted videos.
- For embedded third-party video (YouTube/Vimeo), still add `VideoObject` describing it accurately and a transcript on-page where you can.
- **Don't** mark up video that isn't on the page, or claim a duration/upload date that's wrong.

## Step 3 — Verify (on the served output)
- Re-fetch and confirm: meaningful images carry `alt`; `VideoObject` JSON-LD is present in the **raw** served HTML and **honest** (every value matches the real media on the page); transcripts/captions are real text in the served output; the image/video sitemap is reachable and lists real, `200` media URLs.
- Validate the `VideoObject` (MCP validator or against Google's video structured-data requirements). Report eligibility honestly — eligible ≠ guaranteed.
- Confirm media-bearing pages aren't client-only shells (media present pre-JS).

## Step 4 — Report
Plain English: what was missing (e.g. "your videos had no structured data or transcripts, so Google couldn't understand or surface them"), what you added (with served-output proof), what needs you (real transcripts/captions you wouldn't fabricate), and the boundary — this makes media *eligible* to be found/surfaced; it doesn't guarantee rankings or video results.

---

## Reference files
- `references/media-schema-and-sitemaps.md` — `VideoObject` and image-sitemap/video-sitemap patterns (honest values only), transcript/caption handling, formats/sizing, and exact verification.
