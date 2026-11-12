---
surface: gemini
title: Gemini
verification: weak
verification_methods: [sampled_prompt]
claimable_outcome: eligibility
weighting: [substance, identity, access, distribution, demand]
---

# Gemini

## What this surface is

Google's assistant, as distinct from the generated answers inside Search. The distinction
is the main reason this file exists separately: **AI Overviews and AI Mode are in Search
and are profiled in [`google-ai-mode.md`](google-ai-mode.md)**, while Gemini is a
conversational product. They overlap in infrastructure and differ in how you check them.

Read `google-ai-mode.md` first. Most of what you would do for Gemini you do there, with
better verification.

## What differs from the Search AI surfaces

- **Verification is worse.** Search Console reports on Search's AI experiences. It does not
  report on Gemini. So you move from partial verification to sampled prompts only, which
  is the main practical difference and the reason not to treat them as one surface when
  reporting.
- **Grounding varies.** Answers may be grounded in live Search results or answered from
  the model, and which happened is not reliably visible. When grounding does occur, being
  visible in Google's index is the precondition, which usefully means the work is the same
  work.
- **Crawling follows Google's controls.** Google has stated that its AI features do not
  need special files or markup, and access is governed through the controls you already
  manage for Google, including the site-level control for AI features in Search Console.
  There is no separate crawler to allowlist in the way there is for other providers.

## What decides whether you are drawn on

Substance first, as with the Search AI surfaces: a specific, self-contained passage that
answers the question. Then Identity, so the source can be attributed and trusted. Then
Access, as a precondition rather than an achievement. Then Distribution, which feeds the
ranking systems upstream. Then Demand, read as prompts rather than queries.

## How to verify

Sampled prompts only: a fixed set, run on a schedule, recording prompt, date, whether
named, what was said and which sources were linked. Note in the record whether the answer
appeared to be grounded in live results, where that is visible, because an ungrounded
answer tells you nothing about your pages.

Use `google-ai-mode.md`'s Search Console data as the better-instrumented proxy for whether
your content is being used by Google's generative features generally. It is not the same
surface, and it is the closest thing to a measurement you have.

## What is unknowable here

- Whether a given answer was grounded in live results or not.
- Any share, rate or position. There is no reporting for this surface.
- Whether work landed. You have a sample, with a sample's variance.

## What may never be claimed

Eligibility only, and with less supporting evidence than almost anywhere else in this
model, because there is no first-party reporting at all.

Do not report Gemini and AI Overviews as one number. One is sampled with no instrumentation
and the other has partial first-party data, and blending them produces a figure whose
provenance nobody can reconstruct.

## Honest note on effort

Do the work in `google-ai-mode.md` and treat this surface as a beneficiary of it. There is
no separate programme worth funding, and no separate format worth adopting: Google has said
plainly that optimising for its AI features is still SEO.

If a client specifically asks about Gemini, the honest answer is that the work is the same
as for Google Search, the verification is weaker, and you will be reporting samples rather
than measurements.
