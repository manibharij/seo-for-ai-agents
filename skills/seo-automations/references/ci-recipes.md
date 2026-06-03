# CI recipes — automate the audit

Read this for ready-to-adapt automation. The goal: a deterministic regression gate that fails a build when a change makes the site less crawlable/indexable, plus scheduled drift checks. All of it runs the pack's own **served-output** logic — no paid data, host-agnostic.

> Run checks against a **running URL** — a deploy-preview for PRs (Vercel/Netlify expose one), production for scheduled runs. CI can't inspect served HTML of a site that isn't deployed.

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
          set -e
          PATHS=("/" "/blog/a-real-post" "/products/a-real-product")   # representative templates
          PHRASE="a distinctive sentence that must appear in your content"
          fail=0
          for p in "${PATHS[@]}"; do
            url="$BASE_URL$p"
            code=$(curl -s -o body.html -w "%{http_code}" -L "$url")
            echo "→ $url ($code)"
            [ "$code" = "200" ] || { echo "::error::$url returned $code"; fail=1; }
            grep -qi "$PHRASE" body.html || { echo "::error::content missing from served HTML at $url (client-rendered?)"; fail=1; }
            grep -qi 'name="robots"[^>]*noindex' body.html && { echo "::error::stray noindex at $url"; fail=1; }
            grep -qi 'rel="canonical"' body.html || echo "::warning::no canonical at $url"
          done
          curl -sfL "$BASE_URL/sitemap.xml" >/dev/null || { echo "::error::sitemap unreachable"; fail=1; }
          exit $fail
```

This is intentionally simple and transparent. Expand the `PATHS`/`PHRASE` per template, or generate them from the sitemap. The `::error::`/`::warning::` annotations surface inline on the PR.

---

## Lighthouse CI (Core Web Vitals + SEO audit)

Add `treosh/lighthouse-ci-action` (or `@lhci/cli`) against the same preview URL, with assertion budgets that fail on regression:

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
          assertions: |
            categories:seo=error:0.9
            categories:performance=warn:0.8
```
Gate the SEO category hard (it flags `noindex`, blocked resources, missing canonical, non-`200`); keep performance a warning unless the team wants it strict. Note: Lighthouse is **lab** CWV — the **field** score still needs real users (see the Read rung's `page-experience.md` and `seo-measurement-setup`).

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
