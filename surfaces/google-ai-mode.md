---
surface: google-ai-mode
title: Google AI Overviews and AI Mode
verification: partial
verification_methods: [sampled_prompt, serp, search_console_api]
claimable_outcome: eligibility
weighting: [substance, access, identity, distribution, demand]
---

# Google AI Overviews and AI Mode

## What this surface is

Google's generated answers: AI Overviews above the classic results, and AI Mode as a
conversational surface of its own. Both compose an answer from sources and link to some of
them.

The important structural fact, and the one that saves the most wasted money: **Google
states that this is still SEO.** AI features draw on its core ranking systems, and Google
says explicitly that there is no need to chunk content into fragments, add AI text files
such as `llms.txt`, add special schema, or write differently for AI (Google Search
Central, "Optimizing your website for generative AI features on Google Search", verified
2026-10).

So this is not a separate discipline with its own tricks. It is the same work, judged on
whether a passage can be lifted out and used.

## What decides whether you are drawn on

1. **Substance.** First here, unlike the assistant surfaces where Identity leads, because
   Google already knows who you are from the web index. What it needs is a passage that
   answers the question specifically and can stand alone. Hedged copy gives a generator
   nothing to use.
2. **Access.** Necessary and genuinely checkable. If the content is not in what Google
   receives, it cannot be drawn on. Also relevant: snippet controls. `nosnippet`,
   `max-snippet` and `data-nosnippet` limit what can be shown, and Google has a site-level
   control for its AI features. Those are **commercial decisions** for the owner, not
   technical defaults for an agent to set.
3. **Identity.** Experience, expertise and authorship, weighted heavily where the query is
   YMYL-adjacent, which a surprising share of generated answers are.
4. **Distribution.** Earned authority still feeds the ranking systems these features draw
   on, so it is upstream rather than absent.
5. **Demand.** Generated answers appear for question-shaped and exploratory queries far
   more than for navigational or transactional ones, which is itself a useful planning
   signal: look at which of your queries trigger one.

## How to verify

Partial, and the gap between what you can see and what you want to know is wide:

- **Search Console** reports clicks and impressions from AI experiences inside overall
  Search performance, without breaking them out into their own filterable dimension in the
  way most people expect. Treat it as a blended figure and say so.
- **Sampled queries**, run on a schedule from a consistent location, recording whether an
  overview appeared, whether you were linked, and which sources were. Appearance itself is
  volatile: the same query can show an overview one day and not the next.
- **The SERP shape** for your priority queries: whether Google chose to generate an answer
  at all tells you what it thinks the intent is.
- **Served output** for the usual Access checks, plus whatever snippet controls are set.

## What is unknowable here

- Why a particular source was chosen, or your share of generated answers.
- Whether an overview will appear for a query tomorrow. Triggering is unstable, and
  measured trigger rates have moved substantially over time.
- The click impact in isolation, because an overview changes the behaviour of the whole
  result page, and you only see the blended outcome.
- How AI Mode weighs sources differently from AI Overviews, which Google has not detailed.

## What may never be claimed

No guarantee of inclusion, no "AI visibility score" presented as a measurement, and no
forecast of traffic change from an overview appearing or disappearing. Inclusion is
sampled, dated and variable.

Also never claim that a special format earned the inclusion. Google says the special
formats are unnecessary, so attributing a result to `llms.txt` or to FAQ fragmentation is
a story, not a finding.

## Honest note on effort

Treat this as a reason to do the Substance work properly rather than as a project of its
own. A page that answers a real question plainly, with the answer near the top, from a
site whose entity resolves, is as eligible as anything can be made.

The two things genuinely worth doing specifically for this surface are both cheap: decide
the snippet controls deliberately rather than by default, and check that the content is in
the served HTML. Everything beyond that is ordinary good work, and anyone charging
separately for "AEO" on top of it should be asked what exactly is different.
