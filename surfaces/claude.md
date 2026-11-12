---
surface: claude
title: Claude
verification: weak
verification_methods: [sampled_prompt]
claimable_outcome: eligibility
weighting: [identity, substance, distribution, access, demand]
---

# Claude

## What this surface is

Anthropic's assistant. Like ChatGPT it synthesises an answer and may name nobody, so the
weighting and the honest ceiling are the same: read
[`chatgpt.md`](chatgpt.md) first, because the reasoning there applies here almost
unchanged. This file records only what differs.

## What differs from ChatGPT

- **Retrieval varies by product and configuration.** Some surfaces have live web search,
  some answer from training, and the same question can be handled either way. You often
  cannot tell which happened from the answer, which makes attributing any change harder
  than it already is on an opaque surface.
- **Crawling is a separate consideration.** Anthropic operates its own crawlers, and
  whether they are permitted is controlled by your `robots.txt` and by any CDN or firewall
  bot rules. Check this specifically rather than assuming a rule written for Googlebot or
  GPTBot covers it. As with every AI crawler, whether to allow it is a **commercial
  decision** for the owner, not a default for an agent to set.
- **Citation behaviour differs by surface.** Where links are shown they tend to be few,
  which makes a sample of citations less informative than Perplexity's.

## How to verify

Sampled prompts, exactly as for ChatGPT: a fixed prompt set, run on a schedule, recording
prompt, date, whether named, what was said, competitors named, sources linked where any
are.

Verify crawler access separately and concretely, by fetching your pages as Anthropic's
crawler user agent and confirming the content is present without JavaScript execution.
That part **is** strongly verifiable even though the surface is not, and it is worth doing
because it is a precondition rather than a hope.

## What is unknowable here

Everything that is unknowable for ChatGPT, plus one more: whether a given answer came from
live retrieval or from training data. That matters, because if it came from training then
nothing you ship this month can affect it on any predictable timescale.

## What may never be claimed

Eligibility only. No guarantee of a mention, no share-of-answers figure, no forecast, and
no claim that a change caused a different answer.

Be especially careful not to imply that content can be placed into a model's training
data. You cannot, you cannot verify it, and the timing is entirely outside your control.

## Honest note on effort

There is no work that is specific to this surface and worth doing on its own. Resolving
your entity, answering real questions plainly, earning third-party coverage and keeping
your pages readable without JavaScript cover it, and all four are justified by
conventional search anyway.

The only genuinely surface-specific item is the five-minute check that your bot policy
does not block the crawler while the owner believes it is allowed, or allow it while the
owner believes it is blocked. Both situations are common and both are decisions somebody
should have made deliberately.
