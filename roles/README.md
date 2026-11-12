# Roles

A **role** is a bounded worker: what it owns, which workflows it may run, which tools it may
use, what it must ask before doing, what it may never do, what it may spend, and what
finishing means.

Roles exist so that autonomy can be granted precisely. "Let the agent do SEO" is not a
decision anyone can make safely. "Let the Technical Engineer fix broken internal links
unsupervised, and ask before touching a canonical" is, and that is the shape of every role
file here.

## The six roles

| Role | Owns | Default rung | Can it change the site? |
|---|---|---|---|
| [`demand-analyst`](demand-analyst.md) | Demand | 1 observe | No. There is nothing here to execute |
| [`identity-steward`](identity-steward.md) | Identity | 3 propose | Yes, under approval. Owns `.seo/context.md` |
| [`content-editor`](content-editor.md) | Substance | 2 recommend | Edits what exists. Never generates |
| [`technical-engineer`](technical-engineer.md) | Access, regression gates | 3 propose | Yes, under approval. Narrow fences |
| [`distribution-strategist`](distribution-strategist.md) | Distribution | 2 recommend | **Never.** Advisory by design |
| [`account-reporter`](account-reporter.md) | Reporting, prioritisation | 2 recommend | No. Writes for the human |

The rungs come from `contracts/work-item.schema.json`: 1 observe, 2 recommend, 3 propose,
4 execute within fences, 5 operate.

## The pattern in the default rungs

A role's rung tracks **what it can break**, and reading down the column tells you something
about the discipline.

The Demand Analyst sits at rung 1 not because the work is unimportant, but because it is the
observed system: there is no action, only a judgement that redirects everyone else. The
Distribution Strategist sits at 2 with an **empty** `fenceable` list, which is the only role
in the pack that can never act at any rung, because every mechanism for executing here is
either against platform rules or deceptive.

The two roles that can change the site, Identity Steward and Technical Engineer, both sit at
3 with narrow fences and long `must_ask` lists, because both can take a site out of the
index or publish a claim that cannot be retracted.

## What every role shares

Four rules apply to all of them, from [`model/invariants.md`](../model/invariants.md):

1. **Verify on served output, never on source.** A role may not mark work done on the
   strength of a diff. The patch is not the evidence; the response is.
2. **Only `established` facts may be published.** Provenance travels with every fact into
   copy, schema and reports.
3. **Some things are permanently human.** Anything needing a credential, an identity or a
   relationship. Any claim that cannot be sourced. Judgement calls on tone or risk.
4. **A role that did nothing must say why.** `skipped_reason` is required, because silence
   reads as broken.

## How roles work together

A job activates several, and they hand over rather than overlapping:

- Identity Steward writes `.seo/context.md` **first**, because the Content Editor cannot
  write an honest sentence without knowing which facts are established.
- Demand Analyst's map decides what the Content Editor works on, so reading demand wrongly
  wastes everyone downstream.
- Technical Engineer clears Access, because nothing the others do pays off on a page a
  machine cannot reach.
- Distribution Strategist says whether authority is the constraint, which frequently stops a
  content programme that would not have worked.
- Account Reporter is the only one that writes to the human, and the only one that may make
  a claim to a customer.

## Writing a new role

Match the frontmatter in the existing files: `role`, `title`, `owns`, `surfaces`,
`workflows`, `tools`, `data`, `autonomy` (with `default_rung`, `may_do`, `must_ask`,
`never`, `fenceable`), `budget`, `reports` and `done_when`.

Then prose that answers three questions a reader will actually have: how it works, **why its
fences are where they are**, and what it escalates. The second one is the part worth writing
carefully, because a fence without a stated reason gets widened by the next person who finds
it inconvenient.
