# CI recipes — automate the audit

Read this for ready-to-adapt automation. The goal: a deterministic regression gate that fails a build when a change makes the site less crawlable/indexable, plus scheduled drift checks. All of it runs the pack's own **served-output** logic — no paid data, host-agnostic.

> Run checks against a **running URL** — a deploy-preview for PRs (Vercel/Netlify expose one), production for scheduled runs. CI can't inspect served HTML of a site that isn't deployed.
>
> **Mind the preview environment.** Deploy previews are frequently `noindex`'d or password-protected by the host, and may self-canonical to the preview URL. So a `noindex`/canonical check run against a preview will fire on things that are *correct* for a preview. The recipe below treats those checks as warnings on a preview and hard failures on the scheduled **production** run — which is where they actually matter. (If your preview is password-protected, the fetch returns the auth wall, not your HTML; point PR checks at an accessible preview or rely on the production schedule.)

---

## What to gate (fail) vs warn

**Fail the build** (high-severity, unambiguous regressions):
- A key page's primary content is **missing from the raw served HTML** (rendering regressed to client-only).
- A key URL returns non-`200`, or a redirect **chain/loop**.
- A stray `noindex` (meta or `X-Robots-Tag`) on a page that should be indexed.
- Missing or wrong `<link rel="canonical">` on a key template.
- Sitemap missing, unreachable, or listing non-`200` URLs.
- Post-migration: a mapped old URL no longer `301`/`308`s to its target.

**Warn** (annotate the PR, don't block): Core Web Vitals drift within tolerance, minor metadata gaps, new pages not yet in the sitemap. Tune to avoid false-failure fatigue — a gate that cries wolf gets switched off.

---

## A served-HTML regression check (GitHub Actions)

A minimal, dependency-light gate. Adapt the URL list and assertions to the site.

```yaml
# .github/workflows/seo-guardrail.yml
name: SEO guard rail
on:
  pull_request:
  workflow_dispatch:
  schedule:
    - cron: '0 7 * * 1'   # weekly drift check against production (Mondays 07:00 UTC)

jobs:
  served-html:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check served HTML on key pages
        env:
          # Set BASE_URL to the deploy-preview for PRs, production for schedule.
          BASE_URL: ${{ vars.SEO_BASE_URL }}
        run: |
          # No `set -e`: we accumulate failures explicitly, so a grep that finds
          # nothing (its non-zero exit is the *healthy* case here) can't abort the run.
          fail=0

          # Deploy previews are often legitimately noindexed / self-canonical by the
          # host, so environment-sensitive checks (noindex, canonical host) are a
          # WARNING on a preview and a hard ERROR on production. The weekly scheduled
          # run hits production, where these are enforced for real.
          case "$BASE_URL" in
            *vercel.app*|*netlify.app*|*staging*|*preview*) SOFT="warning" ;;
            *) SOFT="error" ;;
          esac
          softfail() { echo "::$SOFT::$1"; [ "$SOFT" = "error" ] && fail=1; return 0; }

          # Each path carries the distinctive phrase that must appear in its RAW served
          # HTML (catches client-only rendering). One stable phrase per template beats a
          # single global string that any copy edit silently breaks. Better still: generate
          # this list from the sitemap so coverage tracks the site.
          # (grep patterns are double-quoted so single/double HTML attribute quotes both match.)
          check() { # <path> <phrase-that-must-be-in-served-html>
            local url="$BASE_URL$1" phrase="$2"
            local code; code=$(curl -s -D head.txt -o body.html -w "%{http_code}" -L "$url")
            echo "→ $url ($code)"

            [ "$code" = "200" ] || { echo "::error::$url returned $code"; fail=1; }
            grep -qiF "$phrase" body.html || { echo "::error::content missing from served HTML at $url (client-rendered?)"; fail=1; }

            # noindex: meta robots/googlebot (EITHER attribute order) OR X-Robots-Tag header.
            if grep -qiE "<meta[^>]+name=[\"']?(robots|googlebot)[^>]*content=[^>]*noindex" body.html \
               || grep -qiE "<meta[^>]+content=[^>]*noindex[^>]*name=[\"']?(robots|googlebot)" body.html \
               || grep -qiE "^x-robots-tag:.*noindex" head.txt; then
              softfail "noindex present (meta or X-Robots-Tag) at $url"
            fi

            # canonical: exactly one, pointing at a real production URL (not missing, not a dev host).
            local n href
            n=$(grep -icE "<link[^>]+rel=[\"']?canonical" body.html)
            href=$(grep -ioE "<link[^>]+rel=[\"']?canonical[^>]*>" body.html \
                   | grep -ioE "href=[\"'][^\"']+" | head -1 | sed -E "s/^href=[\"']//")
            if   [ "$n" -eq 0 ]; then echo "::error::no canonical at $url"; fail=1
            elif [ "$n" -gt 1 ]; then echo "::error::$n canonicals at $url (must be exactly one)"; fail=1
            elif echo "$href" | grep -qiE "localhost|127\.0\.0\.1|vercel\.app|netlify\.app|staging|preview"; then
              softfail "canonical points to a non-production host at $url: $href"
            fi
          }

          # Representative templates — adapt, and give each its real phrase:
          check "/"                        "a distinctive sentence on the homepage"
          check "/blog/a-real-post"        "a distinctive sentence in this post"
          check "/products/a-real-product" "a distinctive sentence on this product"

          # Sitemap reachable and not serving an error page.
          curl -sfL "$BASE_URL/sitemap.xml" >/dev/null || { echo "::error::sitemap unreachable"; fail=1; }

          exit $fail
```

Transparent on purpose, but the assertions are the load-bearing part: the `noindex` check catches **both attribute orders, `googlebot`-specific tags, and the `X-Robots-Tag` header** (a bare `grep noindex` misses the last two and false-positives on body copy); the canonical check verifies **exactly one, pointing at production** (presence alone is not enough); and environment-sensitive checks soften on previews so the gate doesn't cry wolf. Expand `check` per template, or generate the calls from the sitemap so coverage tracks the site.

---

## Lighthouse CI (Core Web Vitals + SEO audit)

Add `treosh/lighthouse-ci-action` (or `@lhci/cli`) against the same preview URL, asserting via a `lighthouserc.json` so you can gate the right things:

```yaml
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: treosh/lighthouse-ci-action@v12
        with:
          urls: |
            ${{ vars.SEO_BASE_URL }}/
            ${{ vars.SEO_BASE_URL }}/blog/a-real-post
          configPath: ./lighthouserc.json
```
```json
// lighthouserc.json — gate unambiguous audits hard; keep category scores as warnings
{
  "ci": {
    "assert": {
      "assertions": {
        "is-crawlable":     ["error", { "minScore": 1 }],
        "http-status-code": ["error", { "minScore": 1 }],
        "canonical":        ["error", { "minScore": 1 }],
        "categories:seo":         ["warn", { "minScore": 0.9 }],
        "categories:performance": ["warn", { "minScore": 0.8 }]
      }
    }
  }
}
```
**Don't hard-gate the SEO *category score*.** It's a shallow checklist: a 0.9 can sit on top of real problems, while trivial nits (a tap-target, one missing description) can drag a healthy page below the line and break the build. Gate the **specific binary audits** that are genuinely pass/fail — `is-crawlable`, `http-status-code`, `canonical` — and keep the SEO and performance *categories* as warnings. Note too that Lighthouse is **lab** CWV and single-run noisy — the **field** score still needs real users (see the Read rung's `page-experience.md` and `seo-measurement-setup`).

---

## Links, redirects, sitemap
- **Broken links:** a link-checker (e.g. `lycheeverse/lychee-action`) on the built site or sitemap.
- **Redirects (post-migration):** a step that fetches each old URL and asserts a single-hop `301`/`308` to the correct target (the check from `seo-migrations/references/redirect-mapping.md`). Schedule it — redirects silently get dropped in later deploys.
- **Sitemap validity:** confirm it parses and all URLs return `200`.

---

## Scheduled re-audit & hooks
- The `schedule:` trigger above runs the gate against **production** weekly, catching drift even with no deploys. Have it open an issue or post to a channel on failure (optional).
- **Pre-deploy / pre-commit hooks** (e.g. via `husky` or a simple npm script) can run a fast subset locally for instant feedback before CI — optional, good for tight loops.

---

## Boundaries to keep honest
- CI runs the **mechanisable** checks only. Schedule the **full agent audit** (the orchestrator) periodically for the judgement-based depth (content quality, schema honesty, positioning) — CI doesn't replace it.
- No secrets in logs; if a check uses an optional data key, read it from CI secrets, never echo it.
- These checks confirm the build is healthy; they don't measure rankings/traffic (live data).
