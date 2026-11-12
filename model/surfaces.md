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

| Surface | Verification strength | Note |
|---|---|---|
`google-web` | Strong | Position and index coverage are observable |
`google-maps` | Strong | Only by point: a single check cannot represent an area |
`google-ai-mode` | Partial | Presence can be sampled, never guaranteed |
`google-news` / Discover | Weak | Largely unobservable, highly volatile |
`google-images` / video | Moderate | |
`google-shopping` | Strong on feed, moderate on placement | |
`bing` / `copilot` | Strong | |
`chatgpt` | Weak | Sampled prompts only. No position, no guarantee |
`claude` | Weak | Sampled prompts only |
`gemini` | Weak | Sampled prompts only |
`perplexity` | Moderate | Citations are visible, which makes it the honest bellwether |
`youtube` | Strong | |
`reddit` / communities | Moderate | |
`app-store` | Moderate | Presence only. The deep mechanics are a separate discipline |
`marketplace` | Moderate | |
`agent-mcp` | Strong | Deterministic, and almost nobody is measuring it yet |

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
