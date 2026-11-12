---
surface: chatgpt
title: ChatGPT
verification: weak
verification_methods: [sampled_prompt]
claimable_outcome: eligibility
weighting: [identity, substance, distribution, access, demand]
---

# ChatGPT

## What this surface is

A conversational engine that synthesises an answer from many sources and may name
nobody. There is no position, no ranking and no index you can inspect. It retrieves,
it draws on training, and it decides.

## What decides whether you are named

In order of influence, which is the reverse of the order most people work in:

1. **Identity.** The engine must be able to resolve who you are and what you do before
   it can recommend you. A business with an inconsistent name, an unresolvable entity
   or no presence in the sources the engine trusts is not a candidate, however good its
   pages are. This is why Identity leads here and Access does not.
2. **Substance.** Clear, specific, extractable answers to the questions people actually
   ask. Hedged marketing copy gives a synthesiser nothing to lift.
3. **Distribution.** What third parties say about you, because the engine weighs sources
   it did not get from you more heavily than the ones it did. This is the part you
   cannot build, only earn, which is why eligibility is the ceiling of any promise.
4. **Access.** Necessary, not sufficient. If the crawler cannot render your pages you
   are invisible, but rendering correctly earns nothing by itself. Check
   `access/ai-crawler-rendering` specifically: the assumption that an AI crawler
   executes your JavaScript is often wrong.
5. **Demand.** Prompt demand, not query demand. People ask assistants in longer, more
   situational language than they type into a search box, and the useful unit of work is
   the prompt, not the keyword.

## How to verify

**Sampled prompts only.** Choose a representative set of prompts, run them on a
schedule, and record whether you were named, what was said, and which sources were
cited. That is a sample, with all the variance a sample has: the same prompt can
produce a different answer an hour later, and non-determinism is a property of the
surface rather than a measurement error.

Record: prompt, date, whether named, position in the answer if named, competitors
named, sources cited.

## What is unknowable here

- Why you were or were not named.
- Your share of all answers, because the population of prompts is unbounded.
- Whether a change you made caused a change in the answer. Correlation is all you get.
- Anything resembling a rank.

## What may never be claimed

No guarantee of citation, ever. The engine synthesises from many sources and may cite
no one, so a perfect page is not a sufficient condition. The claimable outcome is
**eligibility**: you were resolvable, you answered the question, and you were present
in the sources the engine draws on.

Report movement as sampled and dated. A single improved answer is an anecdote, not a
result.

## Honest note on effort

This surface rewards work that is worth doing anyway. Resolving your entity, answering
real questions plainly and earning third-party coverage all improve conventional search
at the same time. Work that only targets this surface, and has no other justification,
is usually not worth the money.
