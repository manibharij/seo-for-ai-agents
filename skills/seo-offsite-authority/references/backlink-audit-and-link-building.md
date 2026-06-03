# Backlink audit & white-hat link-building

Read this for the off-page detail. Two halves: **auditing** what you have (needs data), and **earning** more (strategy, white-hat only). The governing rule: links are *earned by being worth linking to*. Anything that tries to shortcut that earns penalties.

---

## Reading a backlink profile

Quality, not count. Assess:
- **Referring domains over total links.** 50 links from 50 relevant sites beats 5,000 from one spammy widget. Count unique linking domains and weigh their quality.
- **Authority & relevance.** Strong, *topically relevant* domains pass the most value. A link from a respected site in your field beats a high-authority but irrelevant one.
- **Anchor-text distribution.** Natural profiles are mostly brand and URL anchors, with some generic ("click here", "this guide") and a minority of descriptive/partial-match. A **spike of exact-match commercial anchors** ("buy cheap widgets") is the classic manipulation footprint and a risk.
- **Link velocity.** Steady, organic growth is healthy; sudden unexplained spikes can signal a paid campaign or a negative-SEO attack.
- **Toxicity signals.** Link farms, sitewide footer/template links at scale, PBN footprints (same hosting/owner/templates across "different" sites), irrelevant foreign-language directories, links from hacked or adult/gambling spam.
- **Competitor gap.** The referring domains and content types competitors earn that you don't, filtered to ones you could *realistically and relevantly* earn too.
- **Unlinked mentions & lost links.** Mentions without a link (reclaim) and links that have dropped (recover).

Without connected data (Search Console links report, or Ahrefs/DataForSEO/Semrush), you can't do this honestly. Say so and point to the source to connect; don't estimate a profile.

---

## Disavow: rarely, and carefully

Google's algorithms now **ignore most spammy links automatically**, so the disavow tool is a **last resort**, not routine maintenance. Use it only when there's a genuine, clear problem: a real negative-SEO attack, or a legacy of paid/manipulative links you can't get removed.

- **Format:** a plain-text file, one domain or URL per line, `domain:` prefix for whole domains:
  ```
  # Toxic link farm, attempted manual removal 2026-05, no response
  domain:spammy-link-farm.example
  domain:pbn-footprint.example
  https://hacked-site.example/specific-spam-page
  ```
- Submit it in Search Console's disavow tool. It's the one concrete artifact this skill produces.
- **Risk:** over-disavowing removes links that were *helping*. Disavow only what's genuinely toxic, document why (comments), and prefer removal/outreach first. When unsure, don't.

---

## Earning links, white-hat (the durable half)

You don't "build" links; you make things worth linking to and put them in front of the right people.

- **Linkable assets.** Original research and data, free tools/calculators, definitive/canonical guides, strong original opinion or analysis. Recommend what *this* site is uniquely positioned to create that others in its field would cite.
- **Digital PR.** Newsworthy angles, data-led stories, surveys, expert commentary (responding to journalist requests). Earns editorial links and brand mentions, the highest-quality kind.
- **Unlinked-mention reclamation.** Find mentions of the brand/people without a link; polite outreach to add one. High conversion, low effort.
- **Broken-link building & resource pages.** Find relevant broken links or resource lists where the site *genuinely belongs*, and suggest it as a replacement/addition.
- **Relationships & genuine guest contributions** on real, relevant publications (for audience and authority, not link-farming).
- Prioritise by the **competitor gap** and genuine relevance, not vanity volume.

---

## The black-hat tactics this skill refuses (always)
- **Buying or selling links** (including "sponsored" links that pass PageRank without `rel="sponsored"`/`nofollow`).
- **Link schemes / exchanges** at scale ("link to me and I'll link to you").
- **Private blog networks (PBNs).**
- **Comment, forum, profile, or directory spam.**
- **Paid guest-post networks** and mass low-quality guest posting for links.
- **Automated link generation** of any kind.

These are exactly what search engines penalise. They are never recommended here. If the user asks for them, explain why they're harmful and offer the white-hat alternative instead.

---

## The honest boundary
This skill **audits and strategises**; it does not execute outreach, create the content, or build relationships, those are ongoing, off-site, human (or managed-service) work. Final authority is *earned over time*, and where you rank as a result is live data. The agent gives you the map and the priorities; earning the authority is the journey.
