# Media SEO — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the media skill. Makes images and video discoverable and indexable.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** It marks up only real media truthfully — never fabricate transcripts/durations. Review on the served output. See the repo's `DISCLAIMER.md`.

---

You are making my images and video discoverable in search. Mark up only **real, on-page** media, truthfully, and verify on the **served HTML**. Work in four steps.

## Step 1 — Diagnose
- **Images:** descriptive `alt` on meaningful images? Descriptive filenames? Modern formats (WebP/AVIF), right sizes, lazy-loaded with dimensions set? An image sitemap for important images? Images blocked in robots.txt?
- **Video:** `VideoObject` schema present (name, description, thumbnailUrl, uploadDate, duration, contentUrl/embedUrl)? Real **transcript/captions** so the spoken content is indexable text? A real thumbnail? A video sitemap? Is the media in the served HTML or injected only client-side?

## Step 2 — Fix
- **Images:** descriptive alt (`alt=""` for decorative) + filenames; modern formats/sizing/lazy-load with width+height (Next.js: `next/image`); add image entries to the sitemap; don't block image paths in robots.txt.
- **Video:** add **`VideoObject` JSON-LD** with **real** values only (ISO 8601 `duration`, real `uploadDate`), rendered server-side; surface a **real transcript/captions** in the served HTML (if none exists, tell me to generate accurate captions — don't fabricate); ensure a real thumbnail; add a video sitemap for important self-hosted video. For embedded YouTube/Vimeo, describe it accurately. **Never** mark up media that isn't on the page or invent values.

## Step 3 — Verify (served output)
Confirm meaningful images have alt; `VideoObject` is in the **raw** served HTML and **honest** (matches the real media); transcripts are real text in the served output; image/video sitemap reachable and lists real 200 URLs. Validate `VideoObject` (against Google's video requirements); report eligibility, not guaranteed results.

## Step 4 — Report
Tell me what was missing (e.g. "videos had no structured data or transcript, so Google couldn't understand them"), what you added (with proof), what needs me (real transcripts I wouldn't want fabricated), and the boundary — this makes media *eligible* to be found, it doesn't guarantee video results or rankings.
