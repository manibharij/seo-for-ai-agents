# Context Gathering — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the context-gathering skill. Learns the business properly and writes it down once, so every later piece of SEO or content work is grounded instead of guessed. Run this before any content, positioning, schema or E-E-A-T work.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** It records what it can establish and flags what it cannot. Check the facts it captured before relying on them. See the repo's `DISCLAIMER.md`.

---

You are learning my business properly before doing any SEO or content work, and writing it down so you never have to guess. Work in five steps. **Record where every fact came from. Never invent one to fill a gap.**

## Step 1 — Read what you already have
Go through my repository (README, docs, CHANGELOG, package manifest, CMS models, product and pricing data, i18n files, support macros and sales FAQs) and my served site (home, product/service, pricing, about, team, docs, blog, FAQ, and the legal pages — terms and privacy usually name the registered entity, and the footer carries the address and phone). Read any structured data already on the site for canonical entity names and spellings.

## Step 2 — Reach a little further
**If I have Search Console connected** (my own key), read the query report: it is the literal language of people who already reach me, and the best source of my audience's vocabulary. **If a keyword tool is connected**, use it for real demand. Otherwise use free public sources — search suggestions, related searches, "people also ask" questions, and public reference entries for entity spellings. Look at competitors for coverage and positioning only. Respect robots.txt and rate limits, take nothing behind a login, collect no personal data, and never copy competitor wording.

## Step 3 — Label every fact
Mark each one **[established]** (I state it — quote where), **[inferred]** (you concluded it — say from what), **[unknown]** (you could not tell), or **[conflict]** (two sources disagree — record both, don't pick silently). **Inferences may guide strategy. Only established facts may ever appear in published copy, structured data, or a trust signal. Unknown stays unknown.**

## Step 4 — Write it to `.seo/context.md`
Sections: **Identity** (what this is, legal entity, address and phone if local) · **Offer** (what's actually sold, pricing) · **Audience** (segments, the job they're hiring me for, their vocabulary in their own words with examples) · **Differentiators** (true and provable only, each with its proof) · **Proof assets** (real case studies, data, named testimonials, credentials, authors and what they're genuinely expert in) · **Voice** (tone, person, habits, avoided words — with real quoted examples from my copy) · **Claims and constraints** (what I may not say: regulation, compliance, competitor-naming) · **Topical territory** (what I should own, what's out of scope) · **Competitors** · **Entities** (canonical names and spellings) · **Open questions** · **Freshness** (what's volatile and needs re-checking). **No API keys, no credentials, no private customer data in the file** — it gets committed.

## Step 5 — Ask me only what's left
Work it out yourself first; don't hand me a questionnaire. Then give me **a short ranked list of only the questions you genuinely couldn't answer and that would change the work**, each with **a default you'll use if I don't reply**. Three good questions beat twenty. Anything I don't answer stays unknown, and you degrade gracefully rather than assuming.

**Then tell me:** what you established, what you only inferred, what conflicts you found, and what you still don't know. Re-read and re-check this file at the start of future runs — stale context applied confidently is worse than none.
