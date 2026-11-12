# Edge, CDN and bot access

Read this when a page works in your browser but a crawler may not be getting it, or before you sign off Reach on any site behind a CDN, WAF or managed host. A firewall, bot filter or deployment gate sits in front of the app, so it can block or challenge a crawler whatever `robots.txt` says. It never shows up in the repo, which is why source-based audits miss it.

Google's own guidance for AI features lists "ensuring that crawling is allowed in robots.txt, and by any CDN or hosting infrastructure" as a baseline ([AI features and your website](https://developers.google.com/search/docs/appearance/ai-features), verified 2026-10). The same holds for classic Search and for every AI crawler.

Vendor settings below were verified against each vendor's documentation in 2026-10. Dashboards get renamed often, so confirm the current label before you quote a path to the user.

---

## 1. Test what each user agent is served

Fetch the same URL as a browser, as Googlebot and as a few AI crawlers, and compare status, size and final URL. A difference means a rule keyed on the user agent (UA).

```bash
URL="https://example.com/a-real-content-page"
while IFS='|' read -r name ua; do
  printf '%-14s ' "$name"
  curl -s -o /dev/null -A "$ua" -w '%{http_code}  %{size_download} bytes  %{url_effective}\n' "$URL"
done <<'UAS'
browser|Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
Googlebot|Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
GPTBot|Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.4; +https://openai.com/gptbot
OAI-SearchBot|Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; OAI-SearchBot/1.4; +https://openai.com/searchbot
PerplexityBot|Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)
ClaudeBot|Mozilla/5.0 (compatible; ClaudeBot/1.0)
UAS
```

```powershell
$Url = 'https://example.com/a-real-content-page'
$agents = [ordered]@{
  'browser'   = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
  'Googlebot' = 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
  'GPTBot'    = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.4; +https://openai.com/gptbot'
  'ClaudeBot' = 'Mozilla/5.0 (compatible; ClaudeBot/1.0)'
}
foreach ($name in $agents.Keys) {
  try {
    $r = Invoke-WebRequest -Uri $Url -UserAgent $agents[$name] -UseBasicParsing -ErrorAction Stop
    '{0,-12} {1}  {2} chars' -f $name, [int]$r.StatusCode, $r.Content.Length
  } catch {
    '{0,-12} {1}' -f $name, [int]$_.Exception.Response.StatusCode
  }
}
```

The Googlebot, GPTBot, OAI-SearchBot and PerplexityBot strings are the operators' published ones (the `Chrome/` version is a placeholder). The ClaudeBot line is a minimal string containing the token, which is what UA rules usually match on. Run the same loop against `/robots.txt`.

**Reading the result:**
- Same status and roughly the same size for every UA: no UA-based rule is in the way.
- `403`, `429`, `503` or a much smaller body for one bot: a block, rate limit or challenge page. A Cloudflare challenge carries the header `cf-mitigated: challenge` ([Cloudflare docs](https://developers.cloudflare.com/cloudflare-challenges/challenge-types/challenge-pages/detect-response/)).
- `401`, or a redirect to a login page: a deployment or password gate (see Vercel and Netlify below).

### What UA spoofing cannot show you

Your request comes from your IP, not the crawler's. Good WAFs verify bots by IP range, reverse DNS or signed requests, so:
- A spoofed Googlebot that gets a `403` may only be the WAF correctly blocking an impostor. It does not prove the real Googlebot is blocked.
- A spoofed bot that gets a `200` does not prove the real one gets through, because rules aimed at verified bots (Cloudflare's AI bot policies, AWS WAF's `CategoryAI`) match on verified identity, which your laptop does not have.
- Strict bot filters can block `curl` itself as a non-browser client. That is a false alarm about your tool, not about crawlers.

So treat the UA comparison as a screen, then confirm with evidence from the real crawler:
1. **Search Console URL Inspection, live test.** "View tested page" shows the HTTP response, headers and the HTML Google received ([Search Console Help](https://support.google.com/webmasters/answer/9012289)). The live test uses `Google-InspectionTool`, which Google lists among its common crawlers, so a WAF rule written only for the `Googlebot` token can still treat it differently. Check the indexed result as well as the live test.
2. **Server or CDN logs.** Filter by UA, then verify the IPs. A real crawler hitting `403`/`503` in the logs is the proof you need. Most CDNs also have a security event log that names the rule that fired (Cloudflare: **Security > Analytics > Events**; Vercel: Firewall observability; AWS WAF: sampled requests and WAF logs).
3. **Verify the IPs.** Google documents a reverse-then-forward DNS check ([Verify Google crawlers](https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests)):

```bash
host 66.249.66.1                        # expect ...googlebot.com, google.com or googleusercontent.com
host crawl-66-249-66-1.googlebot.com    # must resolve back to the same IP
```
```powershell
(Resolve-DnsName -Name 66.249.66.1 -Type PTR).NameHost
(Resolve-DnsName -Name crawl-66-249-66-1.googlebot.com -Type A).IPAddress
```

Published IP ranges to match against (all verified 2026-10):

| Operator | IP list |
|---|---|
| Google (Googlebot and other common crawlers) | `https://developers.google.com/static/crawling/ipranges/common-crawlers.json` (also `special-crawlers.json`, `user-triggered-fetchers.json`, `user-triggered-fetchers-google.json`, `user-triggered-agents.json` in the same folder) |
| OpenAI | `https://openai.com/gptbot.json`, `https://openai.com/searchbot.json`, `https://openai.com/chatgpt-user.json` |
| Anthropic | `https://claude.com/crawling/bots.json` |
| Perplexity | `https://www.perplexity.com/perplexitybot.json`, `https://www.perplexity.com/perplexity-user.json` |
| Apple | `https://search.developer.apple.com/applebot.json` (reverse DNS `*.applebot.apple.com`) |
| Common Crawl | `https://index.commoncrawl.org/ccbot.json` (reverse DNS `*.crawl.commoncrawl.org`) |

---

## 2. Platform by platform

Each entry says what to check and what to tell the user to change. Without dashboard access you cannot see these settings, so give the user the exact screen and ask them to read back what it says.

### Cloudflare

- **AI bot policies.** **Security Settings > Configure AI bot policies** sets Search, Agent and Training separately, each to *Block (on all pages)*, *Block on pages with ads* or *Allow*. Cloudflare's documented default for domains added from 15 September 2026 is to block Training and Agent on pages with ads while allowing Search. That default applies to new domains, so on an existing zone read the setting rather than assume it. Cloudflare counts mixed-purpose crawlers (Search plus Training) as Training wherever Training is blocked, so a Training block can also stop a crawler that feeds a search product. The older **Block AI bots** setting is deprecated, and its 2024 predecessor was the **AI Scrapers and Crawlers** toggle, so older guides use those names ([Cloudflare docs](https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/), [changelog](https://developers.cloudflare.com/changelog/post/2026-07-01-ai-traffic-options/)).
  *Tell the user:* "Open Security Settings > Configure AI bot policies and read me the setting for Search, Agent and Training. If you want AI assistants to cite you, Search must be Allow, and blocking Agent stops assistants fetching your page when a user asks about it." Agent and Training are business choices: present them, do not decide them.
- **Bot Fight Mode** (Free plan) challenges traffic matching known bot patterns. It cannot be bypassed with WAF custom rules or Page Rules, and Cloudflare warns it may challenge API and mobile app traffic ([docs](https://developers.cloudflare.com/bots/get-started/bot-fight-mode/)). It lives under **Security Settings**, filtered by **Bot traffic**.
  *Tell the user:* if logs show crawlers or monitoring being challenged, turn it off, or move to Super Bot Fight Mode, which supports Skip rules and has its own Verified bots setting.
- **Verified bots.** Cloudflare verifies bots by Web Bot Auth signatures, published IP lists or reverse DNS ([docs](https://developers.cloudflare.com/bots/concepts/bot/verified-bots/)). Check that no WAF custom rule blocks or challenges a verified search crawler.
- **Managed robots.txt.** When on, Cloudflare prepends its own AI-crawler rules to your origin's `robots.txt`, or serves one if you have none ([docs](https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/)). The `robots.txt` crawlers read is then not the one in your repo, so always fetch the live file.
- **AI Crawl Control** has per-crawler allow and block actions and shows `robots.txt` violations. On the Free plan it identifies crawlers by UA only.

### Vercel

- **Deployment Protection.** *Standard Protection* protects everything except production domains. *All Deployments* also protects the production domain, which shuts out every crawler ([docs](https://vercel.com/docs/deployment-protection)). A protected URL answers a crawler, CI job or fetch tool with a `401` or a Vercel login redirect instead of the page, so a preview cannot be audited with plain `curl`, Lighthouse or a fetch tool.
  *To test a protected preview:* send the project's bypass secret in the `x-vercel-protection-bypass` header (Vercel exposes it to deployments as `VERCEL_AUTOMATION_BYPASS_SECRET`), or run `vercel curl <url>` (Vercel CLI 48.8.0 or later), which adds the header for you ([bypass docs](https://vercel.com/docs/deployment-protection/methods-to-bypass-deployment-protection/protection-bypass-automation), [`vercel curl`](https://vercel.com/docs/cli/curl)). Keep the secret out of reports, URLs and commits, and do not switch protection off to run a test.
  *Tell the user:* production should normally be on Standard Protection or none. If it is on All Deployments, the live site is invisible to search.
- **Preview `noindex`.** Vercel adds `X-Robots-Tag: noindex` to preview deployments, except a non-production branch with a custom domain ([Vercel KB](https://vercel.com/kb/guide/are-vercel-preview-deployment-indexed-by-search-engines)). That is correct for previews. Check that production does not carry it, and that a `staging.` custom domain gets its own `noindex`.
- **Firewall.** The bot protection managed ruleset (off by default) challenges non-browser traffic but excludes verified bots. The AI bots managed ruleset (off by default) can log or deny known AI crawlers. Custom rules can match on UA. Vercel says its Bot Protection degrades behind another reverse proxy such as Cloudflare ([docs](https://vercel.com/docs/bot-management)).
  *Tell the user:* "In the project's Firewall settings, read me the AI bots ruleset action and any custom rules that match a user agent."

### AWS WAF and CloudFront

- **Bot Control** (`AWSManagedRulesBotControlRuleSet`) labels verified bots and does not block them in most category rules, but **`CategoryAI` blocks AI bots whether they are verified or not** ([AWS docs](https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-bot.html)). `SignalNonBrowserUserAgent` blocks non-browser UAs from unverified clients, which is why your own `curl` may be blocked. Bot Control verifies using the request's origin IP, so behind another proxy a real crawler can look unverified unless a forwarded-IP allow rule runs first.
  *Tell the user:* if they want AI citation, set `CategoryAI` to Count, or add a label-based allow rule for the crawlers they choose. Also review rate-based rules and geo blocks.
- **CloudFront custom error responses** can replace an origin error with another page and change the status code ([AWS docs](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GeneratingCustomErrorResponses.html)). The common single-page-app setup maps `403`/`404` to `/index.html` with `200`, which turns every missing URL into a soft 404. CloudFront also caches error responses for a configurable time.

### Netlify

- The **User Agent Blocker** extension blocks a preset list of AI crawlers and SEO or search crawlers that you pick ([docs](https://docs.netlify.com/build/build-with-ai/block-ai-crawlers/)). Check that no search crawler is ticked by accident.
- **Firewall Traffic Rules** (IP and geography) run first, then WAF rules, then rate limiting.
- **Password Protection and basic auth** can cover the whole live site, part of it, or only Deploy Previews ([docs](https://docs.netlify.com/manage/security/secure-access-to-sites/overview/)). Check it covers previews only.
- A catch-all rewrite such as `/* /index.html 200` serves `200` for URLs that do not exist. Confirm unknown paths return `404`.

### Fastly

Fastly Bot Management is configured under **Security > Bot Management** ([docs](https://www.fastly.com/documentation/guides/security/bot-management/about-bot-management/)), and VCL can read whether a detected bot is verified (`fastly.bot.category.is_verified`, [reference](https://www.fastly.com/documentation/reference/vcl/variables/miscellaneous/fastly-bot-category-is-verified/)). Check that the bot actions allow search crawlers, and review custom VCL for anything keyed on `User-Agent`.

---

## 3. Headers and caching set at the edge

These never appear in the app's source, so read them on the served response (`curl -sI`, or `.Headers` in PowerShell).

- **`X-Robots-Tag` added at the edge.** Host defaults (Vercel previews), `_headers` files, Cloudflare Transform Rules or a CloudFront response headers policy can add `noindex` to production by mistake. Compare the headers on the production host with a preview.
- **`Vary`.** If the origin serves different HTML by user agent, the cache must key on it, or a crawler can be handed a copy cached for someone else. Better still, serve the same HTML to everyone: anything else edges towards cloaking.
- **Cached error and challenge pages.** A CDN can cache a `5xx`, a maintenance page, a challenge page or an empty shell from a failed build, then serve it to crawlers for the cache lifetime. A soft 404 (error content with `200`) usually comes from an edge fallback rule. Read the cache headers (`Age`, `Cache-Control`, `CF-Cache-Status`, `X-Vercel-Cache`, `X-Cache`) alongside the body.

---

## 4. Done when

- [ ] The UA comparison shows the same status and similar content for the browser, Googlebot and the AI crawlers the user wants, on a content page and on `/robots.txt`.
- [ ] Any difference is explained by a named rule, and the user has decided whether to keep it.
- [ ] URL Inspection (live test) or verified log lines show Google receiving `200` and the real content.
- [ ] Production carries no edge-set `noindex`, and no deployment gate covers it.
- [ ] Unknown URLs return `404`, not a cached or rewritten `200`.
- [ ] Dashboard changes are listed for the user as precise instructions (screen, setting, value), because you cannot make them from the repo.
