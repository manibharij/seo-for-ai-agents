---
surface: perplexity
title: Perplexity
verification: moderate
verification_methods: [sampled_prompt, served_html]
claimable_outcome: eligibility
weighting: [substance, identity, access, distribution, demand]
---

# Perplexity

## What this surface is

An answer engine that retrieves live, composes a reply, and **shows its citations
inline**. That last part is why it matters out of proportion to its size: it is the only
assistant-shaped surface where you can see which sources were used.

That makes Perplexity the honest bellwether for assistant work generally. If your page is
being cited here, it is extractable, it is reachable by an AI crawler, and your entity
resolves well enough to be used. Those are the same preconditions the opaque engines need,
and this is the one place you can observe them.

## What decides whether you are cited

1. **Substance.** First, and more directly than anywhere else. The engine retrieves and
   quotes, so a specific, self-contained, factual passage that answers the question is the
   whole game. Vague copy is not cited because there is nothing in it to cite.
2. **Identity.** It needs to be able to say who the source is, and it surfaces the domain
   and often the author. A resolvable entity with real expertise gets used more readily,
   particularly on anything consequential.
3. **Access.** Critical in a specific, checkable way: it retrieves live, so the content
   must be in what its crawler receives. Verify against **PerplexityBot** specifically
   rather than assuming Googlebot's behaviour generalises, and check CDN and firewall rules
   as well as `robots.txt`.
4. **Distribution.** It draws on sources that are themselves well cited, so earned
   coverage feeds in indirectly.
5. **Demand.** Prompt-shaped rather than query-shaped: longer, more situational, more
   comparative.

## How to verify

Better than any other assistant surface, which is the point:

- **Sampled prompts** with the citations recorded. Because citations are visible, you get
  far more than a yes or no: which of your pages was used, which passage, which
  competitors were cited alongside you, and what the engine thought the question was.
- **Citation share across a prompt set**, which is a real, if noisy, comparative metric.
  Still a sample, still dated, but genuinely informative in a way a ChatGPT sample is not.
- **A fetch as PerplexityBot** to confirm the page is retrievable and the content is
  present without JavaScript execution.
- **Referral traffic in analytics**, which exists here in measurable quantities, unlike
  most of this category.

Record: prompt, date, whether cited, which URL, which passage, competitors cited, and
whether the engine's framing of the question matched your assumption about the intent.

## What is unknowable here

- The retrieval and ranking logic, and why one of your pages was chosen over another.
- The population of prompts, so citation share is share of **your sample**, not of the
  surface.
- Run-to-run variation's true magnitude without repeating the same prompts over time.
- Whether a change you made caused a change in citation. Correlation, as everywhere here.

## What may never be claimed

Eligibility only, as with every assistant surface. Visible citations make the sample
better; they do not make the outcome guaranteed or the measurement complete.

Specifically, do not present citation share from a handful of prompts as a market metric.
"Cited in 6 of our 20 tracked prompts on 12 November" is honest. "28% AI visibility" is
not, because the denominator is invented.

## Honest note on effort

Use this surface as your instrument, not your target. Work for assistant eligibility in
general, then watch here to see whether it is working, because this is the only window
you have.

The practical loop is: fix Access for AI crawlers, make the answers specific and
self-contained, resolve the entity, then sample here monthly. If citations start
appearing here and nowhere else, the work is landing and the opaque engines are simply
opaque. If nothing appears here either, the problem is upstream and the sampling has told
you something useful for very little money.
