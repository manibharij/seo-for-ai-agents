---
job: ai-visible
title: I want AI assistants to recommend me
situation: >-
  Someone has noticed that ChatGPT, AI Overviews, Perplexity or Copilot answers
  questions in their market and does not mention them. They want to be named.
roles: [identity-steward, content-editor, distribution-strategist, technical-engineer, account-reporter]
data:
  required: []
  helpful: [search-console, ai-visibility-sampling, brand-mention-data]
guardrails: [eligibility-only, established-facts-only, no-fabricated-proof, report-weak-verification-as-weak]
default_autonomy: 2
stop_when: >-
  Eligibility work is identified across all five systems and the sampled
  baseline is recorded.
done_when: >-
  Identity resolves, the questions are answered in extractable form, AI crawler
  access is verified on served output, and a dated sampled baseline exists so
  change can be observed without being over-claimed.
---

# AI visible

This job arrives with an expectation the pack has to reset in the first reply: there is no
lever here. Being named by an assistant is not a feature you can switch on, and nobody,
including every tool currently selling "AEO", can make it happen reliably. An assistant
synthesises from many sources and may cite nobody.

What this job can honestly deliver is **eligibility**: you are resolvable, you answer the
question, a crawler can read you, and you are present in the sources the engine draws on.
That is the ceiling, and it is worth saying out loud before any work starts, because a
client who was promised citations will judge good work as a failure.

The most common way this job goes wrong is treating it as a formatting exercise. Adding
`llms.txt`, chunking pages into FAQ fragments and sprinkling schema is the cargo cult of
this surface. Google states plainly that optimising for its AI features is still SEO,
needs no special files or markup, and does not require writing differently. The real
constraint is almost always Identity.

## Why Identity leads here

On a conventional search surface, Access is the floor: fail it and nothing else counts. On
an assistant surface the floor is **Identity**, because the engine has to be able to work
out who you are before it can consider recommending you. A business with an inconsistent
name, an unresolvable entity and no third-party presence is not a candidate, however
beautifully its pages are built.

This reorders the work relative to every other job in the pack. See `surfaces/chatgpt.md`
for the weighting, and the other `surfaces/` profiles, because they differ: Perplexity
shows its citations and is therefore the honest bellwether, while Google's AI Mode can only
be sampled and Discover is close to unobservable.

## Order of work

### 1. Set the expectation, in writing
Before diagnosing anything, state what can and cannot be claimed, and what verification
will look like (sampled prompts, dated, with variance). If the client needs a guaranteed
outcome, this is the moment to say no.

### 2. Establish a sampled baseline
`operations/ai-visibility-sampling`.

Choose a representative set of prompts in the customer's actual language, run them, and
record: prompt, date, engine, whether named, what was said, which competitors were named,
which sources were cited. This is a sample and is labelled as one.

Do this **before** any changes, or there is nothing to compare against and every later
claim is unfalsifiable. Re-run on a schedule, never on demand after a change, because
running it twice until you like the answer is not measurement.

### 3. Make the entity resolvable
`identity/context`, `identity/entity-graph`, `identity/nap-consistency`.

The highest-value work in this job, and the least glamorous:
- One canonical business name, spelled identically everywhere it appears.
- A coherent entity graph: consistent `@id`s, `sameAs` to profiles that genuinely exist,
  one `Organization` that is demonstrably the same thing across every page.
- Real people attached to real expertise, with `Person` entities that resolve to genuine
  profiles. Never invented.
- Presence in the public knowledge bases and directories the engines draw on, which is
  Distribution work and is advisory.

### 4. Answer the actual questions, extractably
`substance/intent-match`, `substance/answerability`, `demand/prompt-demand`.

Prompt demand is not query demand: people ask assistants in longer, more situational
language. Find the real questions, then answer each one in a self-contained passage that
makes sense lifted out of the page, because that is literally what happens to it.

This means plain, specific, committed writing. Hedged marketing copy gives a synthesiser
nothing to quote. It does **not** mean fragmenting the page into question headings for
their own sake.

### 5. Verify AI crawlers can actually read you
`access/ai-crawler-rendering`, `access/bot-policy`, `access/feeds`.

Necessary and not sufficient, and routinely wrong:
- Many AI crawlers do not execute JavaScript. Fetch as them, not as Googlebot.
- Check CDN and firewall rules, which block AI user agents more often than `robots.txt`
  does, frequently without the owner knowing.
- Whether to allow a given AI crawler is a **commercial decision**, not a technical one.
  Present the trade and let the owner choose; do not quietly open everything.

### 6. Advise on the sources the engine trusts
`distribution/authority-gap`, `distribution/digital-pr`.

Engines weigh what others say about you above what you say about yourself, which is
precisely the part you cannot build. Find the gap, write the strategy, execute nothing.

### 7. Consider the deterministic surface nobody is using
`access/agent-interfaces`.

`agent-mcp` is the one surface in this model that is fully deterministic: if an agent can
call your endpoint, read your feed or query your data, it does not have to guess what you
offer. Almost nobody is doing this yet. See `surfaces/agent-mcp.md`. It is speculative in
the sense that demand is still arriving, and honest in the sense that it actually works.

## What this job must never do

- Promise, forecast or imply a citation, a share of answers, or a "visibility score" for
  an unobservable surface. A number invented for this surface will be reported to a client
  as fact, which is why it is worse than no number.
- Fabricate authors, credentials, reviews, mentions or partnerships to build an entity.
  This is the single most tempting place in the pack to do it.
- Present one improved answer as a result. One answer is an anecdote.
- Recommend `llms.txt`, schema or chunking as the fix. They are optional, low-certainty
  and not the constraint.
- Spend the budget here when the site also fails Access. A page a crawler cannot read is
  not eligible anywhere, and that is a cheaper fix with a measurable outcome.

## Output

The expectation statement, the dated sampled baseline, and eligibility findings ordered by
system with Identity first. Every claim about movement carries its sample size, its dates
and its variance.

The most useful honest finding this job produces is often: "the work that would make you
eligible here is the work that would improve your conventional search anyway, and it is
worth doing on that basis. Work that only targets this surface is not."
