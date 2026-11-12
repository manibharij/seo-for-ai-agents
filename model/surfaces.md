# Surfaces

A **surface** is a place where visibility is judged. It is an axis across the five
systems, not a system of its own.

This is the structural fix for the oldest problem in the method. When the model had
only one engine in it, a second engine had to be bolted on above the ladder, which is
how AEO became "the layer on top". It never was a layer. **A surface is a column**, and
being named by an assistant draws on all five systems at once, verified differently.

## What a surface profile declares

Every profile in `surfaces/` states four things:

1. **Weighting.** Which systems decide outcomes here, in order.
2. **Verification.** How you check, and on what evidence.
3. **What is unknowable.** Stated plainly, never estimated into a number.
4. **What is out of your control.** So that nobody promises an outcome they cannot
   deliver.

## The surfaces, and how honestly each can be verified

Each one has a profile in [`surfaces/`](../surfaces/), indexed in
[`surfaces/README.md`](../surfaces/README.md).

| Surface | Verification strength | Note |
|---|---|---|
[`google-web`](../surfaces/google-web.md) | Strong | Position and index coverage are observable |
[`google-maps`](../surfaces/google-maps.md) | Strong | Only by point: a single check cannot represent an area |
[`google-ai-mode`](../surfaces/google-ai-mode.md) | Partial | Presence can be sampled, never guaranteed |
[`google-news-discover`](../surfaces/google-news-discover.md) | Weak | Largely unobservable, highly volatile |
[`google-images`](../surfaces/google-images.md) | Moderate | Mostly an Access problem, and cheap to fix |
[`google-shopping`](../surfaces/google-shopping.md) | Strong on feed, moderate on placement | Feed and page must agree |
[`bing-copilot`](../surfaces/bing-copilot.md) | Strong | Copilot retrieves from the Bing index |
[`chatgpt`](../surfaces/chatgpt.md) | Weak | Sampled prompts only. No position, no guarantee |
[`claude`](../surfaces/claude.md) | Weak | Sampled prompts only |
[`gemini`](../surfaces/gemini.md) | Weak | Sampled prompts only, and no first-party reporting |
[`perplexity`](../surfaces/perplexity.md) | Moderate | Citations are visible, which makes it the honest bellwether |
[`youtube`](../surfaces/youtube.md) | Strong | Demand leads here, not Access |
[`reddit-communities`](../surfaces/reddit-communities.md) | Moderate | Never your page. Read it, never post to it |
[`app-store`](../surfaces/app-store.md) | Moderate | Presence only. The deep mechanics are a separate discipline |
[`marketplace`](../surfaces/marketplace.md) | Moderate | Your listing may outrank your own site |
[`agent-mcp`](../surfaces/agent-mcp.md) | Strong | Deterministic, and almost nobody is measuring it yet |

## The rule that keeps this honest

**Weak verification must be reported as weak.** An assistant surface cannot be measured
the way a ranking can: the engine synthesises from many sources and may cite nobody.
Work on these surfaces improves **eligibility**, and eligibility is the only thing that
may ever be claimed.

A profile that invents a score for an unobservable surface is worse than no profile,
because someone will then report it to a client.

## Why `agent-mcp` is on this list

Because it is the surface where demand is about to arrive, and it is the only one that
is fully deterministic. If an agent can call your data, read your feed or query your
endpoint, it does not need to guess what you offer. The pack's own work on machine
readable interfaces belongs here rather than as a footnote under AEO.
