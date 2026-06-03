# Accessibility & semantics (the SEO overlap)

Read this for the large overlap between accessibility (a11y) and SEO. They are not the same discipline — but they pull in the same direction, because both a screen reader and a search/answer engine consume your page as **structured text and relationships**, not as a pixel layout. Fixing the overlap improves both at once.

> Scope honesty: this is the **SEO-relevant slice** of accessibility, not a full WCAG audit. A complete a11y review (colour contrast, focus management, ARIA patterns, keyboard traps, screen-reader testing) is its own discipline — flag it to the user as worthwhile in its own right; don't claim the pack delivers it.

---

## Where a11y and SEO are the same fix

- **Semantic HTML.** `<main>`, `<nav>`, `<article>`, `<header>`, `<footer>`, headings, lists, `<button>` vs `<a>` — assistive tech and engines both rely on real elements to understand structure. `<div>` soup hurts both. (Also in `content-and-structure.md`.)
- **One logical heading outline.** Screen-reader users navigate by headings; engines use them as the page's outline. One `<h1>`, no levels skipped for styling — same rule for both.
- **Descriptive link text.** "Read more"/"click here" is useless to a screen-reader user tabbing through links *and* wastes the anchor signal for engines. Descriptive anchors serve both. (Also in the Connect rung.)
- **Image `alt` text.** Meaningful images need descriptive `alt` (screen readers announce it; image search uses it); decorative images need `alt=""` so both skip them. Same rule.
- **`<html lang>`.** Tells screen readers which voice/pronunciation and tells engines the language. Set it correctly (e.g. `en-GB`).
- **Real text, not text-in-images.** Content baked into images is invisible to both screen readers and engines (and to AI crawlers). Use real text; reserve images for images.
- **Labels and structure on forms/tables.** Proper `<label>`s, `<th>`/`<caption>` on tables — clearer for assistive tech and more parseable for engines.
- **Meaningful document order.** Content that makes sense read top-to-bottom in the DOM (not visually reordered by CSS into a sequence that reads as nonsense) helps both.

---

## a11y issues that are also SEO issues — check these
- [ ] Exactly one `<h1>`; logical heading nesting (no skipped levels for visual size).
- [ ] Main content in semantic landmarks (`<main>`, `<nav>`, `<article>`…), not anonymous `<div>`s.
- [ ] Meaningful images have descriptive `alt`; decorative ones have `alt=""`.
- [ ] Links use descriptive text that makes sense out of context (no "click here").
- [ ] `<html lang>` set correctly.
- [ ] Important content is real text in the served HTML, not baked into images.
- [ ] Interactive navigation uses real `<a href>`/`<button>` (not click-handlers on `<div>`s) — crawlable *and* keyboard-accessible.

Fix these as part of Read; they raise both your accessibility and your readability to engines.

---

## Where a11y goes beyond SEO (flag, don't over-claim)
These matter for real users but are outside this pack's SEO remit — recommend a proper a11y pass:
- Colour contrast and text legibility.
- Keyboard navigation and visible focus states; no keyboard traps.
- Correct ARIA roles/states for custom widgets (and *not* mis-used ARIA).
- Motion/animation safety, time limits, and other WCAG criteria.

Surfacing these honestly ("your pages would benefit from a dedicated accessibility review — here's what I noticed") is the right move: it serves the user, and it's consistent with the pack's habit of flagging what's beyond build-time SEO rather than pretending to cover it.
