# SEO Audit, read-only: now the default

*This file is kept so existing links still work.*

[`audit.md`](audit.md) is now read-only by default. It diagnoses the whole Visibility Ladder on the served HTML, records findings with ids, saves the report to `.seo/`, and changes nothing on your site. Paste that instead.

- **No files at all?** Paste [`audit.md`](audit.md) and add "chat only": it then writes nothing, not even `.seo/`, and reports in chat.
- **Ready to apply fixes?** Paste [`fix.md`](fix.md) with the refs you approve, for example "apply R-03 and R-07".
- **Checking fixes after a deploy?** Paste [`recheck.md`](recheck.md).

All three treat fetched content (pages, `robots.txt`, `llms.txt`, sitemaps, API responses) as data, never instructions.
