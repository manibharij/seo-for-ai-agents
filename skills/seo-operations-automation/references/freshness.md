# Keeping the pack's facts fresh

Search and AI crawler facts change often: a crawler operator adds a user agent, Google retires a rich result, a CDN changes a default. Advice that was right six months ago can now block a crawler or promise a feature that no longer exists. The pack dates every volatile fact so that both readers and a scheduled check can tell how old it is.

## For people using the pack

Volatile facts in the skills carry a stamp such as "verified 2026-10", usually next to the source link. The stamp is the month someone last checked the fact against that source. Treat anything older than about six months as a lead to re-check, not as settled. Open the source link and confirm the fact before you act on it, especially before you change robots.txt, firewall rules or structured data on a live site. If the source has changed, trust the source over the pack, and consider opening an issue or a pull request.

## For contributors: the stamp convention

- **Stamp volatile facts.** Write "verified YYYY-MM" (lower case, ISO year and month) in the same sentence or table as the fact, next to the primary source URL. For example: `([AI features and your website](https://developers.google.com/search/docs/appearance/ai-features), verified 2026-10)`. A heading stamp such as "The main AI crawler tokens (verified 2026-10)" covers the table under it.
- **Link the primary source.** Use the operator's or standard's own page (Google Search Central, web.dev, each crawler operator's docs, schema.org, framework docs), not a blog summary. Put the link in prose or a Markdown link, not inside code: the check skips URLs in code blocks and inline code, because those are examples, API endpoints and XML namespaces.
- **Only stamp what you checked.** If you could not verify a fact this month, leave the old stamp or label the sentence as judgement. Never update a date you did not re-verify.

### What counts as volatile

- **Crawler tokens and user agents:** names, what each one controls, published IP range files.
- **Quotas and limits:** API quotas, file size and line limits (sitemaps, disavow files), rate limits.
- **Rich result availability:** which structured data types Google or Bing still show, eligibility rules, required and recommended properties.
- **CDN and host defaults:** bot management settings, AI crawler blocking defaults, managed robots.txt behaviour.
- **Framework APIs:** rendering defaults, metadata and sitemap APIs, version and release status.
- **Thresholds and policies:** Core Web Vitals thresholds, consent requirements, search engine guidelines.

Stable facts, such as how HTTP status codes work or the meaning of `rel="canonical"`, need no stamp.

## How to re-verify

1. Run the check locally to see what is stale or broken:

   ```bash
   python3 scripts/check-freshness.py              # dates and links
   python3 scripts/check-freshness.py --offline    # dates only
   ```

   ```powershell
   python scripts/check-freshness.py
   python scripts/check-freshness.py --offline
   ```

   Useful options: `--months 6` changes the staleness threshold (default 3), `--strict` exits 1 when anything is stale, broken or unreachable, `--output report.md` saves the report, `--include-code` also checks URLs inside code.
2. For each item, open the source and compare it with what the pack says.
3. If the fact still holds, update the stamp to the current month. If it changed, correct the fact in the full skill, its references and its copy-paste mini, then update the stamp.
4. For a redirect, replace the link with the target once you have confirmed the target page says the same thing. For a broken link, find the page's new home or a current primary source.
5. "Blocked, check manually" means the site refused an automated request (a 401, 403 or 429, or a known bot-blocking host such as help.openai.com). That is not a failure: open it in a browser and check it by hand.

## How the workflow works

`.github/workflows/freshness.yml` runs on the 1st of each month and on demand from the Actions tab (`workflow_dispatch`). It runs `scripts/check-freshness.py --strict`, adds the report to the run summary, and when there are stale stamps, broken links or unreachable URLs it opens a single issue titled "Freshness check: facts to re-verify", or updates the body of the open one and adds a comment linking the run. Redirects and blocked sites appear in the report but do not open an issue on their own. It uses the built-in `GITHUB_TOKEN` with `issues: write` permission and needs no secrets. Close the issue once the items are re-verified; the next run opens a new one if anything is still stale.

The link check is polite: it sends a HEAD request (falling back to GET), identifies itself with a user agent naming the pack, runs at most a few requests at once, and makes one request at a time per host with a short pause.
