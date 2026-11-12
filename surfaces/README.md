# Surfaces

A **surface** is a place where visibility is judged. It is an axis across the five
systems, not a system of its own, and the structural point is in
[`model/surfaces.md`](../model/surfaces.md): when the method had only one engine in it, a
second engine had to be bolted on above the ladder, which is how AEO became "the layer on
top". It never was a layer. A surface is a column.

Every profile states four things, and the last two are the ones that keep the work honest:

1. **Weighting.** Which systems decide outcomes here, in order.
2. **Verification.** How you check, and on what evidence.
3. **What is unknowable.** Stated plainly, never estimated into a number.
4. **What may never be claimed.** So nobody promises an outcome they cannot deliver.

## The surfaces

| Surface | Verification | Leading system | Claimable outcome |
|---|---|---|---|
| [`google-web`](google-web.md) | Strong | Access | Measured position |
| [`google-maps`](google-maps.md) | Strong, by point | Identity | Presence, per coordinate |
| [`google-ai-mode`](google-ai-mode.md) | Partial | Substance | Eligibility |
| [`google-shopping`](google-shopping.md) | Strong on feed, moderate on placement | Identity | Feed health |
| [`google-images`](google-images.md) | Moderate | Access | Measured presence |
| [`google-news-discover`](google-news-discover.md) | Weak | Identity | Eligibility |
| [`bing-copilot`](bing-copilot.md) | Strong | Access | Measured position |
| [`perplexity`](perplexity.md) | Moderate | Substance | Eligibility |
| [`chatgpt`](chatgpt.md) | Weak | Identity | Eligibility |
| [`claude`](claude.md) | Weak | Identity | Eligibility |
| [`gemini`](gemini.md) | Weak | Substance | Eligibility |
| [`youtube`](youtube.md) | Strong | Demand | Position and engagement |
| [`reddit-communities`](reddit-communities.md) | Moderate | Distribution | Presence observed |
| [`app-store`](app-store.md) | Moderate | Identity | Presence and web eligibility |
| [`marketplace`](marketplace.md) | Moderate | Identity | Presence and parity |
| [`agent-mcp`](agent-mcp.md) | Strong | Access | Measured availability |

## How to read that table

**Verification strength is not importance.** `google-web` and `chatgpt` can both matter
commercially; only one of them can be measured. The column exists so that a report says
"sampled on these dates" where sampling is all there is, instead of inventing a number.

**The leading system changes the order of work**, which is the main practical use of these
files. On `google-web`, Access is the floor and nothing above it counts until it is
cleared. On `chatgpt`, Identity leads and Access is necessary but not sufficient. On
`youtube`, Demand leads, because video demand is nothing like text demand. An agent that
runs the same checklist on every surface is working the wrong system first on most of them.

**Eligibility appears five times.** Those are the surfaces where it is the only honest
outcome, and where the industry most often promises more.

## Grouping them

- **Measurable, and where the budget usually belongs:** `google-web`, `bing-copilot`,
  `google-shopping`, `youtube`, `google-images`, `agent-mcp`.
- **Local, where Identity and earned reviews decide it:** `google-maps`.
- **Assistants, all capped at eligibility:** `google-ai-mode`, `perplexity`, `chatgpt`,
  `claude`, `gemini`. Use `perplexity` as the instrument, because it shows its citations.
- **Not your page:** `reddit-communities`, `marketplace`, `app-store`. Advisory, and the
  useful output is usually intelligence plus a strategic question.
- **Arriving:** `agent-mcp`, which is the only fully deterministic surface here and the
  one almost nobody is measuring.

## The rule that keeps this honest

**Weak verification must be reported as weak.** Work on an assistant surface improves
eligibility, and eligibility is the only thing that may ever be claimed. A profile that
invents a score for an unobservable surface is worse than no profile, because someone will
report it to a client as fact.

## Writing a new surface profile

Match the frontmatter (`surface`, `title`, `verification`, `verification_methods`,
`claimable_outcome`, `weighting`) and keep the four required sections. Two further habits
make a profile worth reading: say what differs from the nearest existing surface rather
than repeating it, and end with an honest note on whether surface-specific effort is
actually worth the money. For most surfaces, most of the time, the answer is that the work
worth doing was justified by conventional search anyway.
