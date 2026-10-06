# Analytics, Search Console & web-vitals — install patterns

Read this to install measurement plumbing correctly and verify it on the served output. Scope reminder: this is **setup only**. Interpreting the data is live-data work, outside the build.

---

## GA4 (Google Analytics 4)

Universal Analytics (the old `analytics.js`/`ga()`) is **defunct** — if you find a UA tag, remove it. Use **GA4** (`gtag.js` with a `G-XXXXXXX` Measurement ID), installed **once**.

### Next.js (App Router) — preferred
Use `@next/third-parties` (official, optimised):
```tsx
// app/layout.tsx
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }) {
  return (
    <html lang="en-GB">
      <body>{children}</body>
      <GoogleAnalytics gaId="G-XXXXXXX" />
    </html>
  )
}
```
Or with `next/script` if you prefer manual control:
```tsx
import Script from 'next/script'
// in the root layout, once:
<Script src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX" strategy="afterInteractive" />
<Script id="ga4" strategy="afterInteractive">{`
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXX');
`}</Script>
```
Place it **once** in the root layout — not per page (which double-counts).

### Generic (any site)
The standard `gtag.js` snippet in `<head>`, once, site-wide. On hosted platforms, use the platform's analytics field or a tag-manager integration rather than editing code.

### The common failures
- **Two tags** (e.g. one in the theme + one via a plugin/tag manager) → every event double-counted. Find and remove the duplicate.
- **Legacy UA tag** still present → remove.
- **Client-only injection that never loads** (or is blocked before consent) → confirm it actually fires.
- **Wrong Measurement ID** (a staging/other-project ID) → confirm the right `G-` ID.

---

## Google Search Console verification

GSC is where the user sees real indexing/performance data. Verification proves they own the site. Methods:
- **HTML meta tag** — easiest for a code site. Next.js via the Metadata API:
  ```tsx
  export const metadata = { verification: { google: 'your-verification-token' } }
  ```
  (renders `<meta name="google-site-verification" content="…">`).
- **HTML file** — upload the provided file to the site root.
- **DNS record** — a TXT record (verifies the whole domain; good for domain-wide).
- **Via GA4** — if analytics is already installed and the user has access.

The agent puts the **token/method in place**; the **user completes verification** in their GSC account (a live step) and then submits the sitemap there.

---

## Core Web Vitals (field) reporting — optional

Real-user CWV (the field score Google uses) only exists once real users hit the live site. You can wire reporting so the user sees it over time:
- **Next.js:** `useReportWebVitals` (from `next/web-vitals`) to forward LCP/INP/CLS to GA4.
- **Generic:** the `web-vitals` library reporting to your analytics endpoint.

Be explicit: this *enables* the user to see field CWV accruing; it does not produce a score at build time. Lab CWV (Lighthouse) is the build-time proxy (see the Read rung's `page-experience.md`).

---

## Google Tag Manager or the Google tag (gtag.js)

Pick one route and install it once. Google's guidance (verified 2026-10, [GA4 tag options](https://developers.google.com/analytics/devguides/collection/ga4/tag-options)):
- **Google tag (`gtag.js`)** when developers own the tags and the site only sends data to Google services. It does not support third-party or custom tags.
- **Google Tag Manager** when marketers manage tags without code changes, or when third-party tags are needed. Google recommends Tag Manager to get started.

If GTM is already on the site, configure GA4 as a tag inside the container and do not add a separate `gtag.js` snippet. The Next.js docs give the same advice for `@next/third-parties` (verified 2026-10, [Next.js third-party libraries](https://nextjs.org/docs/app/guides/third-party-libraries)):

```tsx
// app/layout.tsx: GTM instead of the GoogleAnalytics component, never both
import { GoogleTagManager } from '@next/third-parties/google'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en-GB">
      <GoogleTagManager gtmId="GTM-XXXXXXX" />
      <body>{children}</body>
    </html>
  )
}
```

**Server-side tagging** runs a Tag Manager server container in a cloud project the site owner controls, so tags run there instead of in the browser ([server-side tagging](https://developers.google.com/tag-platform/tag-manager/server-side/intro)). It involves hosting, cost and data-protection decisions, so this skill names it and stops. If the user already runs one, `GoogleTagManager` accepts a `gtmScriptUrl` pointing at their tagging server.

---

## Consent Mode v2 (EEA and UK visitors)

**When it applies.** Google's EU user consent policy covers end users in the European Economic Area, the UK and Switzerland ([EU user consent policy](https://www.google.com/about/company/user-consent-policy/)). For EEA users, Google says that to keep using measurement, ad personalisation and remarketing features, sites must collect consent and share consent signals with Google, and GA4 reads `ad_user_data` and `ad_personalization` for those signals ([GA4 consent help](https://support.google.com/analytics/answer/14275483)). All verified 2026-10. Whether a consent banner is legally required, and what it says, is a decision for the user and their adviser; this skill installs the signals and flags the gap.

**The four signals** ([consent mode concepts](https://developers.google.com/tag-platform/security/concepts/consent-mode)):

| Signal | Controls |
|---|---|
| `ad_storage` | Advertising cookies or device identifiers |
| `analytics_storage` | Analytics cookies, for example visit duration |
| `ad_user_data` | Sending user data to Google for advertising |
| `ad_personalization` | Personalised advertising |

**Basic or advanced.** In basic mode, Google tags do not load until the visitor interacts with the banner, and nothing is sent before consent. In advanced mode, tags load at once with the denied defaults and send cookieless measurements, which Google uses for more detailed modelling. Advanced sends more data, so it is a privacy decision for the user, not a technical default.

**Order matters.** The default must be set before any `config` call. With the Google tag ([consent mode setup guide](https://developers.google.com/tag-platform/security/guides/consent)):

```js
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('consent', 'default', {
  ad_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied',
  analytics_storage: 'denied',
  wait_for_update: 500,
  region: ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IS','IE','IT','LV','LI','LT','LU','MT','NL','NO','PL','PT','RO','SK','SI','ES','SE','GB','CH']
});
// later, from the banner's accept handler:
gtag('consent', 'update', {
  ad_storage: 'granted',
  ad_user_data: 'granted',
  ad_personalization: 'granted',
  analytics_storage: 'granted'
});
```

`region` limits the denied default to the listed countries (the EEA, the UK and Switzerland here); drop it to deny by default everywhere, which some businesses prefer. `wait_for_update` gives an asynchronous banner time, in milliseconds, to send its update. Update only the signals the visitor actually granted.

**Next.js App Router.** Put the default in the root layout with `strategy="beforeInteractive"`, which Next.js injects into the `<head>` of the initial HTML ahead of its own code (verified 2026-10, [Script component](https://nextjs.org/docs/app/api-reference/components/script)). The Google tag then loads after it.

```tsx
// app/layout.tsx
import Script from 'next/script'
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en-GB">
      <body>
        {children}
        <Script id="consent-default" strategy="beforeInteractive">{`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('consent', 'default', {
            ad_storage: 'denied', ad_user_data: 'denied',
            ad_personalization: 'denied', analytics_storage: 'denied',
            wait_for_update: 500
          });
        `}</Script>
      </body>
      <GoogleAnalytics gaId="G-XXXXXXX" />
    </html>
  )
}
```

Most consent management platforms send the `update` themselves, and many can set the default too. If the user's platform does, use its integration and do not add a second default. With GTM, set consent defaults through the platform's GTM template or GTM's consent settings rather than a hand-written snippet.

---

## Bing Webmaster Tools

Bing Webmaster Tools reports how Bing crawls and indexes the site. Ways to verify:
- **Import from Google Search Console** (the quickest). The user signs in to Bing Webmaster Tools and imports; imported sites are verified automatically, their sitemaps come across, and Bing re-checks ownership by syncing with Search Console. Up to 100 sites per import. If the user later removes that access, they must verify another way (verified 2026-10, [Bing Webmaster blog: import from Search Console](https://blogs.bing.com/webmaster/september-2019/Import-sites-from-Search-Console-to-Bing-Webmaster-Tools)).
- **Meta tag:** `<meta name="msvalidate.01" content="TOKEN">` in the home page `<head>`. In Next.js, the Metadata API's `verification.other` renders any name and content pair:
  ```tsx
  export const metadata = {
    verification: { google: 'GOOGLE_TOKEN', other: { 'msvalidate.01': 'BING_TOKEN' } },
  }
  ```
- **XML file:** `BingSiteAuth.xml`, downloaded from Bing Webmaster Tools, at the site root.
- **DNS:** a CNAME record with the name Bing provides, pointing to `verify.bing.com`.

The meta tag, file and DNS details above are from Bing's verification flow as widely documented; Bing's own help page did not render for verification on 2026-10-06, so confirm the exact values inside Bing Webmaster Tools when you add the site. The agent places the token or file; the user completes verification and the import in their own account.

---

## Install table: other stacks

The same rules apply everywhere: one tag, consent default before config, and a check on the served output. Where a platform has an official integration, use it rather than pasting code into a theme, which is how duplicate tags happen.

| Stack | Where the tag goes | Search Console and Bing tokens | Notes |
|---|---|---|---|
| **Nuxt** | Nuxt Scripts: `scripts.registry.googleAnalytics` in `nuxt.config.ts` with your `G-` ID, and `useScriptGoogleAnalytics()` for events ([Nuxt Scripts](https://scripts.nuxt.com/scripts/google-analytics)). | `app.head.meta` in `nuxt.config.ts`, or `useHead` in `app.vue` ([Nuxt SEO and meta](https://nuxt.com/docs/4.x/getting-started/seo-meta)). | Nuxt Scripts' registry setup turns on first-party mode, which serves the script from your own domain and proxies requests; mention it so the user knows. |
| **SvelteKit** | The `gtag.js` snippet in `src/app.html`, inside `<head>` above `%sveltekit.head%` ([project structure](https://svelte.dev/docs/kit/project-structure)). | Meta tags in `src/app.html`, or in `<svelte:head>` in the root `+layout.svelte`. | Client-side navigation is handled by GA4's history-change page views (Enhanced Measurement); do not also send manual page views, or each one counts twice. |
| **Astro** | The `gtag.js` snippet in the shared layout's `<head>`. To move it off the main thread, the Partytown integration (`npx astro add partytown`) runs scripts marked `type="text/partytown"` in a worker; forward `dataLayer.push` in its config ([Astro Partytown](https://docs.astro.build/en/guides/integrations-guide/partytown/)). | Meta tags in the shared layout's `<head>`. | Test events after enabling Partytown; a worker changes timing. |
| **WordPress** | Site Kit by Google: connects Analytics and places the tag without code edits, and verifies Search Console ownership with a token file or meta tag ([Site Kit docs](https://sitekit.withgoogle.com/documentation/supported-services/search-console/)). | Site Kit for Google. For Bing, the SEO plugin's webmaster-tools field, or the Search Console import. | Site Kit's consent mode setting needs the WP Consent API plugin and a consent management plugin ([Site Kit consent mode](https://sitekit.withgoogle.com/documentation/using-site-kit/consent-mode/)). Check that the theme or another plugin is not also adding a tag. |
| **Shopify** | The Google & YouTube sales channel app, following Shopify's GA4 setup ([Shopify help](https://help.shopify.com/en/manual/reports-and-analytics/google-analytics/google-analytics-4)). | Search Console: the HTML tag pasted directly below `<head>` in `theme.liquid` (Online Store, Edit code), or DNS. Bing: the Search Console import. | Remove any older GA snippet in `theme.liquid` so events are not counted twice (judgement; Shopify's page does not mention duplicates). |

Platform detail beyond measurement is in `seo-orchestrator/references/platforms/wordpress.md` and `seo-orchestrator/references/platforms/shopify.md`. All rows verified 2026-10 against the linked pages, except where marked judgement.

---

## Verifying setup on the served output

```bash
# exactly one GA4 tag?
curl -sL https://example.com | grep -o "G-[A-Z0-9]\{6,\}" | sort -u
# search-console verification token present?
curl -sL https://example.com | grep -i "google-site-verification"
# consent default, GTM container, Bing token
curl -sL https://example.com | grep -oE "consent', *'default'|GTM-[A-Z0-9]+|msvalidate\.01"
curl -s -o /dev/null -w "%{http_code}\n" https://example.com/BingSiteAuth.xml
```
```powershell
(Invoke-WebRequest "https://example.com" -UseBasicParsing).Content |
  Select-String -Pattern "G-[A-Z0-9]{6,}|google-site-verification"
$html = (Invoke-WebRequest "https://example.com" -UseBasicParsing).Content
[regex]::Matches($html, "consent', *'default'|GTM-[A-Z0-9]+|msvalidate\.01") | ForEach-Object Value
try { (Invoke-WebRequest "https://example.com/BingSiteAuth.xml" -UseBasicParsing).StatusCode } catch { $_.Exception.Response.StatusCode.value__ }
```

Confirm:
- [ ] Exactly **one** GA4 snippet with the correct `G-` ID (no duplicates, no legacy UA).
- [ ] If a network/browser MCP is available: the analytics request **fires once** on load.
- [ ] GSC verification token/method in place (the user then verifies in GSC).
- [ ] Sitemap reachable and referenced in `robots.txt`, ready to submit.
- [ ] No tracking added that bypasses a required consent mechanism (flag consent gaps to the user).
- [ ] Where Consent Mode applies: `gtag('consent', 'default'` appears in the served HTML before the first `config` call, and the banner sends an `update`.
- [ ] Only one of GTM or a standalone `gtag.js` loads GA4.
- [ ] Bing: `msvalidate.01` in the served HTML, `/BingSiteAuth.xml` returning 200, or the user has imported the site from Search Console.

Record what's set up in `.seo/` so progression runs confirm the tags didn't regress (a redeploy dropping analytics is common). Then hand off: the instruments are in; **reading them is the live-data discipline, not the build.**
