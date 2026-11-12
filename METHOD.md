# The Visibility Model

*A method for being found and chosen wherever people and machines are searching: five
systems, one loop, many surfaces.*

The canonical reference lives in [`model/`](model/): [systems](model/systems.md),
[surfaces](model/surfaces.md), [invariants](model/invariants.md). This document is the
narrative version.

---

## Why most SEO advice fails

Open almost any SEO checklist and you get a flat list: add meta descriptions, write alt
text, get backlinks, add schema, improve Core Web Vitals, and twenty more items in no
particular order. It reads like a to-do list. It behaves like a slot machine.

The items are not wrong. The problem is that some of them have a **dependency order** and
the checklist hides it. A beautiful meta description on a page a crawler cannot render is
wasted work. Structured data on a page that never gets fetched is wasted work.

That insight is real, and it is where this method started, as a ladder. But a ladder
turned out to be too small a shape, because it quietly assumed four things: one engine,
one asset, one moment, and one kind of work. All four are now false.

- Demand resolves across Google web search, Maps, AI Mode, ChatGPT, Gemini, Perplexity,
  Copilot, YouTube, Reddit, app stores, marketplaces, and increasingly agent to agent.
- Your entity exists across directories, knowledge bases, review sites and profiles. Much
  of what decides whether you get recommended is not on your domain.
- Visibility decays. A fix verified in March is undone by a deploy in April.
- Most of the work is not a code change. It is reading demand, judging substance,
  maintaining identity, and advising on authority you can only earn.

So the ladder is not wrong. **It was one system mistaken for the whole discipline.**

## The five systems

The systems are separated by **your relationship to control**, because that is what
decides whether an agent may act, advise, or only observe.

| System | Relationship | The question it answers |
|---|---|---|
**Demand** | Observed | What are people and machines actually asking, and which of it is worth having? |
**Identity** | Built | Who are you, provably, everywhere you appear? |
**Substance** | Built | Is what you offer and say actually worth choosing? |
**Access** | Built | Can a machine get it, read it, understand it, and move through it? |
**Distribution** | Earned | Does anything outside your control point at you? |

Around all five runs the **Operations loop**: measure, verify on served output, detect
regressions, monitor, report, repeat.

And across them runs the **surface** axis. A surface is a place where visibility is
judged, and each one weighs the systems differently and can be verified to a different
degree. `google-web` weights Access and Substance and is strongly verifiable.
`google-maps` weights Identity and can only be checked point by point. `chatgpt` weights
Identity first and can only be sampled.

### Where the Visibility Ladder went

**The Ladder is the Access system**, and inside Access it holds exactly as it always did:

1. **Reach.** Can a machine get to the content at all?
2. **Read.** Once reached, is there real content, served, fast and usable?
3. **Understand.** Can the engine identify the entities on the page?
4. **Connect.** Is the page wired into a coherent site?

Diagnose top to bottom, fix bottom to top. The lowest broken rung quietly caps everything
above it.

### Rank is the outcome, not a rung

Rank used to be rung five. It is now **the result the whole model produces**, which is a
promotion rather than a demotion. Its old contents moved to where the work actually
happens: search intent and genuine quality to **Substance**, experience and expertise and
authorship to **Identity**, and the authority you earn to **Distribution**.

This matters practically. "Improve rankings" was never one step you could climb to. It is
five systems being right at once, on a surface you have chosen, and kept right by the
loop.

### Where AI visibility went

AEO used to be "the layer on top of the ladder". That was a symptom of the old shape:
with only one engine in the model, a second engine had to be bolted above it.

**An assistant is a surface, not a layer.** Being named by ChatGPT draws on all five
systems at once and is verified differently and more weakly than a ranking. See
[`surfaces/chatgpt.md`](surfaces/chatgpt.md) for what that means in practice: Identity
leads, Access is necessary but not sufficient, and the only claimable outcome is
**eligibility**, never citation.

That is a sharper position than the old one, not a softer one. It also stops anyone
promising an outcome no one can deliver.

## How the systems relate

Dependency runs one way only where Access is concerned: nothing downstream matters if a
machine cannot reach the page. **Everything else is simultaneous, not sequential.**

A perfect Access score with no Demand reading is a fast, well-formed, beautifully
structured page that nobody was looking for. A site with superb Substance and an
unresolvable Identity will not be recommended by an assistant, because an engine that
cannot work out who you are has nothing to recommend.

## Run it as a loop, not a climb

A real site is never done. Content ships, templates get refactored, platforms get
upgraded, and fixes silently revert.

- **Baseline.** The first pass takes the site's state across all five systems, records
  where it stands, and fixes the safe wins.
- **Progress.** Each later pass re-verifies that past fixes still hold on served output,
  catching the regression that arrived in a deploy, then finds what is new and advances
  the backlog by priority.
- **Maintain.** Over time this keeps a site healthy rather than letting it drift.

In this pack that memory is a `.seo/` folder in the project: a readable report, a
machine-readable issue tracker, and a dated history. The structured shapes are defined in
[`contracts/`](contracts/).

## The rules that keep it honest

Stated in full in [`model/invariants.md`](model/invariants.md). The four that matter most:

**Verify on served output, never on source.** An agent that edits some JSX and announces
"meta tags added" has proven nothing. It changed an intention. What matters is what comes
down the wire, and client-rendered content invisible to crawlers is still the single most
common failure of AI-built sites.

**Only established facts may be published.** Every fact about the business carries its
provenance: `established`, `inferred`, `unknown`, or `conflict`. Only an established fact
may reach published copy, schema, or a claim made to a customer. This is what turns
"never fabricate" from a refusal into a method.

**Work it out yourself, do not interrogate the user.** The person running this should not
need to know SEO or fill in a questionnaire. The agent reads the codebase and the served
pages, infers the context, acts on sensible defaults, and pauses only for the decisions a
human genuinely must make.

**On an existing site, first do no harm.** A `noindex`, a canonical, a redirect or a
blocked path that looks wrong may be load-bearing. Understand what is deliberate before
changing it, prefer additive and reversible fixes, and put risky changes in front of a
human.

## The boundary

This method fixes **build-time** problems on your **owned media**: the structural,
code-level decisions baked into how your own site is rendered, written, marked up, linked
and formatted. Two things sit outside that line, honestly.

**Earned media.** Backlinks, digital PR, brand mentions and third-party reviews genuinely
affect whether you rank and whether you get cited. Distribution has a named place in the
model, and the pack audits and strategises it, white-hat only. It never executes outreach
and never buys placement, because authority is earned through real work over time and
faking it is the behaviour this method refuses.

**Live measurement.** A build cannot tell you whether you actually rank, where, against
whom, or whether assistants are naming you over time. That is live data, treated here as
optional enrichment and never a requirement: connect your own tools with your own keys
and the work gets sharper. The free build-time capability never depends on it, and no
build-time capability is ever paywalled.
